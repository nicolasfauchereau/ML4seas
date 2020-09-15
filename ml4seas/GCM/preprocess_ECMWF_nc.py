def preprocess_ECMWF_nc(dset): 
    """
    small utility function to pre-process 
    the ECMWf netcdf files (1981 - 2019)
    """
    # 1: set the initial time 
    dset = dset.expand_dims('init_time')
    dset['init_time'] = (('init_time'), [dset.time.data[0]])
    # 2: rename the dimensions 
    d = {}
    d['latitude'] = 'lat'
    d['longitude'] = 'lon'
    d['number'] = 'member'
    d['time'] = 'step'
    dset = dset.rename(d)
    # 3: replace the step variable 
    dset['step'] = (('step'), np.arange(len(dset.step.data)))
    # 3: flip the latitudes 
    if (dset.lat.data[0] > dset.lat.data[-1]): 
        dset = dset.sortby('lat')
    return dset
