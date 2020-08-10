import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt 

import sys
import time
import os 
import pathlib
import pickle

CWD = pathlib.Path.cwd()

sys.path.append('../../ml4seas/')

# scipy 
import numpy as np 
import pandas as pd 
import xarray as xr

# tensorflow and keras 
import tensorflow as tf

tf.debugging.set_log_device_placement(True)

import tensorflow.keras as keras
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model
import tensorflow.keras.backend as K


# import NN utilities 
from NN import *

CWD = pathlib.Path.cwd()

# checks if the GPU is available 
if len(tf.config.list_physical_devices('GPU')) >= 1: 
    compute = 'GPU'
else: 
    compute = 'CPU'

print(f"using the {compute}")

# define parameters here 
batch_size=32
padd = 8
input_shape = (181, 360, 1) # last for the number of channels 
resize_shape = (176, 360) # to be evenly divided by the padd
n_epochs = 20 # number of epochs 
dpath = pathlib.Path('/downscaling/GCMs/processed/hindcasts/CDS/ECMWF/T2M/')

### list the files 
lfiles = list(dpath.glob("ECMWF_T2M_seasonal_anomalies_????_??.nc"))

lfiles.sort()

# opens the dataset 
dset = xr.open_mfdataset(lfiles, concat_dim='time', combine='nested', parallel=True)

### selects the training set 
dset_train = dset.sel(time=slice('1993','2010'))

### selects the validation set 
dset_val = dset.sel(time=slice('2011',None))

### select the correct lead time (3 = e.g. SON for A initialisation)
dset_train = dset_train[['t2m']].sel(step=3)
dset_val = dset_val[['t2m']].sel(step=3)

dset_train = dset_train.stack(instance=('time','member'))
dset_val = dset_val.stack(instance=('time','member'))


### get the repeated datetimes (will be useful to sample repeatedly in Yds)

rdatetimes_train = dset_train.indexes["instance"].get_level_values(0)
rdatetimes_val = dset_val.indexes["instance"].get_level_values(0)

# transpose  
dset_train = dset_train.transpose('instance','lat','lon')
dset_val = dset_val.transpose('instance','lat','lon')

### Generate data for tensorflow 
data_train = XrDataGenerator(dset_train, dset_train, {'t2m':None}, 't2m', norm=True, batch_size=batch_size, mean=None, std=None, shuffle=True, load=False)
data_val = XrDataGenerator(dset_val, dset_val, {'t2m':None}, 't2m', norm=True, batch_size=batch_size, mean=data_train.mean, std=data_train.std, shuffle=True, load=False)


# ### checks the shape (should be (batch_size, (input_shape), channels)) 

# ### build the model 

### encoder 

# Input placeholder
original = Input(shape=input_shape)

# Resize to have dimensions divisible by 8
resized = ResizeLayer(newsize=(176,360))(original)

# # Wrap-around in longitude for periodic boundary conditions

padded = PeriodicPadding2D(padd)(resized)

# Encoding layers
x = Conv2D(16, (3, 3), padding='same')(padded)
x = LeakyReLU()(x)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(8, (3, 3), padding='same')(x)
x = LeakyReLU()(x)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(8, (3, 3), padding='same')(x)
x = LeakyReLU()(x)

encoded = MaxPooling2D((2, 2), padding='same')(x)

### decoder 

# Decoding layers
x = Conv2D(8, (3, 3), padding='same')(encoded)
x = LeakyReLU()(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(8, (3, 3), padding='same')(x)
x = LeakyReLU()(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(16, (3, 3), padding='same')(x)
x = LeakyReLU()(x)
x = UpSampling2D((2, 2))(x)
decoded = Conv2D(1, (3, 3), padding='same')(x)

# Strip the longitude wrap-around
pruned = PrunePeriodicPadding2D(padd)(decoded)

outsize = ResizeLayer(newsize=input_shape[:2])(pruned)

autoencoder = Model(original,outsize)

### run ID 
run_id = time.strftime("run_%Y_%m_%d-%H_%M_%S")

### ---------------------------------------------------------------------------------------------------------------------
### callbacks 

# checkpoints 

checkpoint_cb = keras.callbacks.ModelCheckpoint(f"./autoencoder_checkpoint_{run_id}_{compute}.h5", save_best_only=True)

# early stopping 

early_stopping_cb = keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)

root_logdir = os.path.join(os.curdir, "my_logs")

def get_run_logdir(run_id):
    return os.path.join(root_logdir, run_id)

run_logdir = get_run_logdir(run_id)

keras.backend.clear_session()
np.random.seed(42)
tf.random.set_seed(42)

# tensorboard callback 
tensorboard_cb = keras.callbacks.TensorBoard(run_logdir, profile_batch=0)

### ---------------------------------------------------------------------------------------------------------------------
### compile 

autoencoder.compile(optimizer='adam', loss='mean_squared_error')

autoencoder.summary(line_length=120)

### ---------------------------------------------------------------------------------------------------------------------
### fit 

# ### Note: run tensorboard with: 
#         
# ```
# tensorboard --logdir=./my_logs  --port=6006
# ```


history = autoencoder.fit(data_train, validation_data=data_val, epochs=n_epochs, callbacks=[checkpoint_cb, early_stopping_cb, tensorboard_cb])

### ---------------------------------------------------------------------------------------------------------------------
### save model 

saved_model = CWD / f"saved_autoencoder_{run_id}_{n_epochs}_epochs_{compute}" 

keras.models.save_model(autoencoder, saved_model)

### save history 
saved_history = CWD / f"saved_history_{run_id}_{n_epochs}_epochs_{compute}.pkl" 

pickle.dump(autoencoder.history.history, open(saved_history, "wb"))

### ---------------------------------------------------------------------------------------------------------------------
### Some plots 

i = 10

X = data_val[0][0][i:i+1,:,:,:]

pred = autoencoder.predict(X)

pred = pred.squeeze()

f, axes = plt.subplots(nrows=2, figsize=(10,16))

axes = axes.flatten() 

ax = axes[0]

im = ax.imshow(data_val[0][0][i,::-1,:,0], vmin=-5, vmax=5, cmap=plt.cm.RdBu_r)

ax = axes[1]

im = ax.imshow(pred[::-1,:], vmin=-5, vmax=5, cmap=plt.cm.RdBu_r)  

f.savefig(f'./preds_vs_inputs_{run_id}.png', dpi=200, bbox_inches='tight')

f, ax = plt.subplots()
pd.DataFrame(history.history).plot(ax=ax, marker='o')
ax.grid(ls=':')

f.savefig(f'./history_{run_id}.png', dpi=200, bbox_inches='tight')
