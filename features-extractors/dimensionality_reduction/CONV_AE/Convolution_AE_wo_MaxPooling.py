# %% 
import matplotlib
from tensorflow.python import data 

from matplotlib import pyplot as plt 

### sys imports 

import pathlib
import sys
import os 
import time 
import pickle

### get current directory 
CWD = pathlib.Path.cwd()

### add local library and import 
sys.path.append('/home/nicolasf/research/Smart_Ideas/code/ml4seas/')
from NN import * 

### Scientific stack 
import numpy as np 
import pandas as pd 
import xarray as xr

### Tensorflow and Keras 
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model
import tensorflow.keras.backend as K

### check if GPU available 
if len(tf.config.list_physical_devices('GPU')) >= 1: 
    compute = 'GPU'
else: 
    compute = 'CPU'

print(f"using the {compute}")

### defines parameters 

# %% 
batch_size=32

padd = 8

input_shape = (181, 360, 1) # last for the number of channels 

resize_shape = (padd * round(input_shape[0]/padd), padd * round(input_shape[1]/padd)) # to be evenly divided by the padd

n_epochs = 20 # number of epochs 

### list the files 

# %%
dpath = pathlib.Path('/media/nicolasf/END19101/data/GCMs/processed/hindcasts/CDS/ECMWF/T2M/')


# %%
lfiles = list(dpath.glob("ECMWF_T2M_seasonal_anomalies_????_??.nc"))


# %%
lfiles.sort()


# %%
dset = xr.open_mfdataset(lfiles, concat_dim='time', combine='nested', parallel=True)

# ### selects the training set 

# %%
dset_train = dset.sel(time=slice('1993','2010'))


# %%
dset_val = dset.sel(time=slice('2011',None))

# ### select one step (leadtime = 3 months), and only t2m 

# %% 
dset_train = dset_train[['t2m']].sel(step=3)
dset_val = dset_val[['t2m']].sel(step=3)

### concatenate all the members long the first dimension, to increase number of instances 

# %%
dset_train = dset_train.stack(instance=('time','member'))


# %%
dset_val = dset_val.stack(instance=('time','member'))

### get the repeated datetimes (will be useful to sample repeatedly in Yds)

# %%
rdatetimes_train = dset_train.indexes["instance"].get_level_values(0)


# %%
rdatetimes_val = dset_val.indexes["instance"].get_level_values(0)

### transpose to have the instances as the first dimension 

# %%
dset_train = dset_train.transpose('instance','lat','lon')
dset_val = dset_val.transpose('instance','lat','lon')

### Generate data for tensorflow 

# %%
data_train = XrDataGenerator(dset_train, dset_train, {'t2m':None}, 't2m', norm=True, batch_size=batch_size, mean=None, std=None, shuffle=True, load=False)


# %%
data_val = XrDataGenerator(dset_val, dset_val, {'t2m':None}, 't2m', norm=True, batch_size=batch_size, mean=data_train.mean, std=data_train.std, shuffle=True, load=False)

### checks the shape (should be (batch_size, (input_shape), channels)) 

# %%
data_train[0][0].shape


# %%
data_val[0][0].shape

### build the model 

# %%
from numba import cuda
device = cuda.get_current_device(); 
device.reset()


# %%
# Input placeholder
original = Input(shape=input_shape)

# Resize to have dimensions divisible by 8
resized = ResizeLayer(newsize=resize_shape)(original)

# # Wrap-around in longitude for periodic boundary conditions

padded = PeriodicPadding2D(padd)(resized)

# Encoding layers
x = Conv2D(16, (3, 3), padding='same')(padded)
x = LeakyReLU()(x)
x = Conv2D(8, (3, 3), strides= (2,2), padding='valid')(x)
x = LeakyReLU()(x)
x = Conv2D(8, (3, 3), strides= (2,2), padding='valid')(x)
x = LeakyReLU()(x)
x = Conv2D(8, (3, 3), strides= (2,2), padding='valid')(x)
x = LeakyReLU()(x)

encoded = x

# Decoding layers
x = Conv2DTranspose(8, (3, 3),  strides= (2,2), padding='valid')(encoded)
x = LeakyReLU()(x)
x = Conv2DTranspose(8, (3, 3),  strides= (2,2), padding='valid')(x)
x = LeakyReLU()(x)
x = Conv2DTranspose(8, (3, 3),  strides= (2,2), padding='valid')(x)
x = LeakyReLU()(x)
decoded = Conv2D(1, (3, 3), padding='same')(x)

# Strip the longitude wrap-around
pruned = PrunePeriodicPadding2D(padd)(decoded)

outsize = ResizeLayer(newsize=input_shape[:2])(pruned)


# %%
autoencoder = Model(original,outsize)

### build the callbacks 

# %%
run_id = time.strftime("ConvAE_wo_MaxPooling_ECMWF_T2M_run_%Y_%m_%d-%H_%M_%S")

### checkpoint 

# %%
checkpoint_cb = keras.callbacks.ModelCheckpoint(f"./autoencoder_checkpoint_{run_id}_{compute}_fullCNN.h5", save_best_only=True)

### early stopping 

# %%
early_stopping_cb = keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)


# %%
root_logdir = os.path.join(os.curdir, "LOGS")

# %%
def get_run_logdir(run_id):
    return os.path.join(root_logdir, run_id)

run_logdir = get_run_logdir(run_id)

print(f"logging in {run_logdir}")

# %% reset session and set random seed 
keras.backend.clear_session()
np.random.seed(42)
tf.random.set_seed(42)

# %% set up tensorboard callback 
tensorboard_cb = keras.callbacks.TensorBoard(run_logdir)

# %% compile 
autoencoder.compile(optimizer='adam', loss='mean_squared_error')
 
# %% print the summary 
autoencoder.summary(line_length=120)

### fit 
# ### Note: run tensorboard with: 
#         
# ```
# tensorboard --logdir=./my_logs  --port=6006
# ```

# %%
# autoencoder.fit_generator(generator=data_train,
#                     validation_data=data_val,
#                     use_multiprocessing=True,
#                     workers=6,epochs=n_epochs, 
#                     callbacks=[checkpoint_cb, early_stopping_cb, tensorboard_cb])


# %% now fit 
history = autoencoder.fit(data_train, validation_data=data_val, epochs=n_epochs, callbacks=[checkpoint_cb, early_stopping_cb, tensorboard_cb])

# %% save model 
saved_model = CWD / f"saved_autoencoder_{run_id}_{n_epochs}_epochs_{compute}_fullCNN" 

keras.models.save_model(autoencoder, saved_model)

# %% save history file 
saved_history = CWD / f"saved_history_{run_id}_{n_epochs}_epochs_{compute}.pkl" 
pickle.dump(autoencoder.history.history, open(saved_history, "wb"))


# %% first original and reconstructed fields for one time step 
preds = []
for i in range(data_val.batch_size):  
    X = data_val[0][0][i:i+1,:,:,:]
    pred = autoencoder.predict(X)
    preds.append(pred)

# %% plots 

# choose the instance here 
i = 0

f, axes = plt.subplots(nrows=2, figsize=(10,10))

ax = axes[0]

im = ax.imshow(data_val[0][0][i,::-1,:,0].squeeze(), vmin=-5, vmax=5, cmap=plt.cm.RdBu_r)

plt.colorbar(im, shrink=0.6, ax=ax, label='T2M anomalies')

ax.set_title(f"orginal for instance N = {i}")

ax = axes[1]

im = ax.imshow(preds[i].squeeze()[::-1,:], vmin=-5, vmax=5, cmap=plt.cm.RdBu_r)

plt.colorbar(im, shrink=0.6, ax=ax, label='T2M anomalies')

ax.set_title(f"reconstruction for instance N = {i}")

f.savefig(f'./ConvAE_wo_max_pooling_ECMWF_T2M_{i}th_instance.png', dpi=200, bbox_inches='tight')

# %% Plots the training and validation loss 
f, ax = plt.subplots()
ax.set_title(f'Training and validation Loss for ConvAE wo Max Pooling\nrun {run_logdir}')
pd.DataFrame(history.history).plot(ax=ax, marker='o')
ax.grid(ls=':')
f.savefig(f'./History_ConvAE_wo_Max_Pooling_run_{run_id}.png', dpi=200, bbox_inches='tight')

# %% transform the prediction in an xarray dataset 

preds = [x.squeeze() for x in preds]
preds = np.array(preds)

d = {}
d['lat'] = (('lat'), dset.lat.data)
d['lon'] = (('lon'), dset.lon.data)
d['instance'] = (('instance'), np.arange(batch_size))

ds_preds = xr.Dataset(d)

ds_preds['preds'] = (('instance','lat','lon'), preds)

# %% and now plot 

# ds_preds.isel(instance=0)['preds'].plot()
