#!/usr/bin/env python
# coding: utf-8

# In[166]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[167]:


from matplotlib import pyplot as plt 


# In[168]:


get_ipython().run_line_magic('load_ext', 'autoreload')


# In[169]:


get_ipython().run_line_magic('autoreload', '2')


# In[170]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[171]:


import pathlib


# In[172]:


CWD = pathlib.Path.cwd()


# In[173]:


import sys


# In[174]:


import time


# In[175]:


sys.path.append('../../ml4seas/')


# In[176]:


import numpy as np 
import pandas as pd 
import xarray as xr


# In[177]:


import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model
import tensorflow.keras.backend as K


# In[178]:


tf.config.list_physical_devices('GPU')


# In[179]:


from NN import *


# ### some parameters for the model and the logs 

# In[180]:


if len(tf.config.list_physical_devices('GPU')) >= 1: 
    compute = 'GPU'
else: 
    compute = 'CPU'


# In[181]:


print(f"using the {compute}")


# In[182]:


batch_size=32


# In[183]:


padd = 8


# In[184]:


input_shape = (257, 241, 1) # last for the number of channels 


# In[185]:


resize_shape = (256, 240) # to be evenly divided by the padd (8)


# In[186]:


n_epochs = 20 # number of epochs 


# ### list the files 

# In[187]:


var_name = "RAIN_BC"


# In[188]:


if "TMEAN" in var_name:
    dpath = pathlib.Path(f"/media/nicolasf/END19101/data/VCSN/{var_name.replace('_N','')}/seasonal_anomalies_VCSN_{var_name}.nc")
elif "RAIN" in var_name:
    dpath = pathlib.Path(f"/media/nicolasf/END19101/data/VCSN/{var_name.replace('_BC','')}/seasonal_anomalies_VCSN_{var_name}.nc")


# In[189]:


dset = xr.open_dataset(dpath) 


# In[190]:


dset


# In[194]:


dset['Rain_bc_interp'][0,:,:].plot()


# ### selects the training set 

# In[ ]:





# In[ ]:





# In[ ]:





# In[191]:


dset_train = dset.sel(time=slice('1979','2010'))


# In[192]:


dset_val = dset.sel(time=slice('2011',None))


# In[125]:


dset_train = dset_train.rename({'time':'instance'})


# In[126]:


dset_val = dset_val.rename({'time':'instance'})


# ### Generate data for tensorflow 

# In[127]:


data_train = XrDataGenerator(dset_train, dset_train, {f'{var_name.lower().capitalize()}_interp':None}, f'{var_name.lower().capitalize()}_interp', norm=True, batch_size=batch_size, mean=None, std=None, shuffle=True, load=False)


# In[128]:


data_val = XrDataGenerator(dset_val, dset_val, {f'{var_name.lower().capitalize()}_interp':None}, f'{var_name.lower().capitalize()}_interp', norm=True, batch_size=batch_size, mean=data_train.mean, std=data_train.std, shuffle=True, load=False)


# ### checks the shape (should be (batch_size, (input_shape), channels)) 

# In[129]:


data_train[0][0].shape


# In[130]:


data_val[0][0].shape


# ### build the model 

# #### encoder 

# In[131]:


# Input placeholder
original = Input(shape=input_shape)

# Resize to have dimensions divisible by 8
resized = ResizeLayer(newsize=resize_shape)(original)

# Encoding layers
x = Conv2D(16, (3, 3), padding='same')(resized)
x = LeakyReLU()(x)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(8, (3, 3), padding='same')(x)
x = LeakyReLU()(x)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(8, (3, 3), padding='same')(x)
x = LeakyReLU()(x)


# In[132]:


encoded = MaxPooling2D((2, 2), padding='same')(x)


# #### decoder 

# In[133]:


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


# In[134]:


outsize = ResizeLayer(newsize=input_shape[:2])(decoded)


# In[135]:


autoencoder = Model(original,outsize)


# In[136]:


autoencoder.summary(line_length=120)


# In[137]:


# tf.keras.utils.plot_model(autoencoder, to_file="model.png", show_layer_names=True, show_shapes=True)


# ### build the callbacks 

# In[138]:


run_id = time.strftime("run_%Y_%m_%d-%H_%M_%S_VCSN")


# ### checkpoint 

# In[139]:


checkpoint_cb = keras.callbacks.ModelCheckpoint(f"./autoencoder_VCSN_checkpoint_{run_id}_{compute}.h5", save_best_only=True)


# ### early stopping 

# In[140]:


early_stopping_cb = keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)


# In[141]:


import os


# In[142]:


root_logdir = os.path.join(os.curdir, "my_logs")


# In[143]:


def get_run_logdir(run_id):
    return os.path.join(root_logdir, run_id)

run_logdir = get_run_logdir(run_id)
run_logdir


# In[144]:


keras.backend.clear_session()
np.random.seed(42)
tf.random.set_seed(42)


# In[145]:


tensorboard_cb = keras.callbacks.TensorBoard(run_logdir, profile_batch=0)


# ### compile 

# In[146]:


autoencoder.compile(optimizer='adam', loss='mean_squared_error')


# In[147]:


autoencoder.summary(line_length=120)


# ### fit 

# ### Note: run tensorboard with: 
#         
# ```
# tensorboard --logdir=./my_logs  --port=6006
# ```
# <hr>

# In[148]:


# autoencoder.fit_generator(generator=data_train,
#                     validation_data=data_val,
#                     use_multiprocessing=True,
#                     workers=6,epochs=n_epochs, 
#                     callbacks=[checkpoint_cb, early_stopping_cb, tensorboard_cb])


# In[149]:


history = autoencoder.fit(data_train, validation_data=data_val, epochs=n_epochs, callbacks=[checkpoint_cb, early_stopping_cb, tensorboard_cb])


# ### save model 

# In[150]:


saved_model = CWD / f"saved_autoencoder_{run_id}_{n_epochs}_epochs_{compute}_VCSN" 


# In[151]:


keras.models.save_model(autoencoder, saved_model)


# ### save history file 

# In[152]:


import pickle


# In[153]:


saved_history = CWD / f"saved_history_{run_id}_{n_epochs}_epochs_{compute}_VCSN.pkl" 


# In[154]:


pickle.dump(autoencoder.history.history, open(saved_history, "wb"))


# ### Some plots 

# ### validation data first batch 

# In[155]:


data_val[0][0].shape


# ### take one from the batch 

# In[156]:


i = 10


# In[157]:


X = data_val[0][0][i:i+1,:,:,:]


# In[158]:


X.shape


# In[159]:


pred = autoencoder.predict(X)


# In[160]:


pred.shape


# In[161]:


pred = pred.squeeze()


# In[196]:


f, ax = plt.subplots(figsize=(10,10))
im = ax.imshow((data_val[0][0][i,:,:,0] * dset['mask'].data)[::-1,:], cmap=plt.cm.RdBu_r)
plt.colorbar(im, shrink=0.4)


# In[195]:


f, ax = plt.subplots(figsize=(10,10))
im = ax.imshow((pred * dset['mask'].data)[::-1,:], cmap=plt.cm.RdBu_r)  
plt.colorbar(im, shrink=0.4)


# ### Plots the training and validation loss 

# In[164]:


f, ax = plt.subplots()
pd.DataFrame(history.history).plot(ax=ax, marker='o')
ax.grid(ls=':')


# In[118]:


pd.DataFrame(history.history)


# In[107]:


data_train.mean.data[0]


# In[108]:


data_train.std.data[0]


# In[165]:


run_id


# In[ ]:




