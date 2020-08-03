import numpy as np
from tensorflow.python.keras.backend import clear_session
import xarray as xr
from tensorflow import keras 
import tensorflow as tf 

class XrDataGenerator(keras.utils.Sequence):
    def __init__(self, Xds, Yds, X_var_dict, Y_var, norm=True, batch_size=32, shuffle=True, mean=None, std=None, load=True):
        """
        defines a Data Generator from xarrays datasets  

        Parameters
        ----------
        Xds : The xarray Dataset with the Feature maps (predictors)
            if several variables and / or levels, they will be concatenated  
            along a 'level' dimension and transposed to have the 'level' as 
            the last dimension (will correspond to the channel)
        Yds : xarray dataset
            The Xarray Dataset with the target variable (instance, lat, lon)
        X_var_dict : dict
            Dictionary of the form {'var': level} for building the inputs. 
            Use None for level if data is of single level
        Y_var : str
            The name of the variable to extract in Yds
        norm : bool, optional
            Whether or not to perform field normalisation of the inputs, by default True
        batch_size : int, optional
            The batch size, by default 32
        shuffle : bool, optional
            if True, data is shuffled, by default True
        mean : xarray dataarray, optional
            if None, computes the field mean, by default None
        std : xarray dataarray, optional
            if None, compute the field std, by default None
        load : bool, optional
            if True, dataset is loaded in memory, by default True
        """

        self.Xds = Xds
        self.Yds = Yds 
        self.X_var_dict = X_var_dict
        self.norm = norm
        self.batch_size = batch_size
        self.shuffle = shuffle

        # build X data 
        Xdata = []
        generic_level = xr.DataArray([1], coords={'level': [1]}, dims=['level'])
        
        for var, levels in X_var_dict.items():
            try:
                Xdata.append(Xds[var].sel(level=levels))
            except ValueError:
                Xdata.append(Xds[var].expand_dims({'level': generic_level}, 1))


        # build Ydata
        if not 'level' in Yds.dims: 
            Ydata = Yds[Y_var].expand_dims({'level': generic_level}, 1)
        
        self.Ydata = Ydata.transpose('instance', 'lat', 'lon', 'level')

        self.Xdata = xr.concat(Xdata, 'level').transpose('instance', 'lat', 'lon', 'level')
        
        # calculates the mean and std (field mean and std)
        self.mean = self.Xdata.mean(('instance','lat', 'lon')).compute() if mean is None else mean
        self.std = self.Xdata.std(('instance','lat', 'lon')).compute() if std is None else std
        # Normalize
        self.Xdata = (self.Xdata - self.mean) / self.std
        self.n_samples = self.Xdata.shape[0]

        self.on_epoch_end()

        # loading 
        if load: 
            print('Loading data into RAM'); 
            self.Xdata.load()
            self.Ydata.load() 

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.ceil(self.n_samples / self.batch_size))

    def __getitem__(self, i):
        'Generate one batch of data'
        idxs = self.idxs[i * self.batch_size:(i + 1) * self.batch_size]
        X = self.Xdata.isel(instance=idxs).values
        y = self.Ydata.isel(instance=idxs).values
        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.idxs = np.arange(self.n_samples)
        if self.shuffle == True:
            np.random.shuffle(self.idxs)

