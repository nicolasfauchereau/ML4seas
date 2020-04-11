def concat_GCMs(provider, GCMs, var_name='T2M', period='hindcasts', rpath=None, domain='ext_regional', standardize=True, flatten=True, ensmean=True, step=3): 
    """
    Returns many GCM outputs concatenated along the time dimension
    
    Parameters
    ----------
    
    - provider : str, the provider in ['CDS','IRI','JMA'], no default 
    - GCMs : list, a list of GCMs in the provider 
    - period : the period to extract, in ['hindcasts','forecasts']
    - rpath : str or pathlib.Path, the path to the 'data' folder 
    - domain : the domain, in ['local','regional','ext_regional', 'global', 'tropics']
    - standardize : Boolean, must be True for 'hindcasts', False for 'forecasts'
    - flatten : Boolean, whether or not to flatten the outputs along the spatial (and optionally members) dimension, default to True
    - ensmean : Boolean, whether or not to calculate the ensemble mean, default to True
    - step : the number of step by which to shift the time index, to align with observed target, default to 3 (assumes seasonal anomalies)
    
    Return
    ------
    
    - X_data_l : numpy.array containing the data concatenated along the time dimension (axis=0)
    - X_data_l_std : if standardized=True, numpy.array containing the standardized data concatenated along the time dimension (axis=0)
    - X_index_l :  numpy.array of Python datatimes, containing the index (note that repeated values will be present)
    - GCM_records : numpy.array of len(X_index_l) containing the string for the corresponding GCM
    - scalers_dict : if standardized=True, dictionnary, with each item (key = GCM) corresponding to fitted scikit-learn StandardScaler() object
    
    
    """
    
    import sys
    import pathlib
    import itertools
    import numpy as np
    
    HOME = pathlib.Path.home()
    
    sys.path.append(HOME / 'research' / 'Smart_Ideas' / 'code' / 'ml4seas')
    
    from utils import set_root_dir
    from GCM import get_GCM_outputs, shift_dset_time
    
    GCM_records = []
    X_index_l = []
    X_data_l = []
    X_data_l_std = []

    domain_def = {}
    domain_def['local'] = [150, 200, -50, -10]
    domain_def['regional'] = [90, 300, -65, 50]
    domain_def['ext_regional'] = [70, 300, -70, 60]
    # domain_def['ext_regional'] = [50, 300, -75, 60]
    domain_def['global'] = [0, 360, -70, 70]
    domain_def['tropics'] = [0, 360, -40, 40]    

    if standardize: 
        
        scalers_dict = {}
    
    if isinstance(rpath, str): 
        rpath = pathlib.Path(rpath)
    
    for GCM in GCMs: 
    
        print(f"getting {GCM}")
    
        dset, coords = get_GCM_outputs(provider=provider, GCM=GCM, var_name=var_name, period=period, rpath=rpath, domain=domain_def[domain], step=step, flatten=flatten, ensmean=ensmean)
        
        if 'valid_time' in dset.coords: 
            dset = dset.drop('valid_time')        
            
        dset = shift_dset_time(dset, step=step)
        
        X_data = dset['t2m'].data
        
        X_index = dset['time'].to_index().to_pydatetime()
        
        if standardize: 
        
            scaler = StandardScaler() 

            scaler = scaler.fit(X_data)

            scalers_dict[GCM] = scaler

            X_data_std = scaler.transform(X_data)

        # append and records 
        
        GCM_records.append(np.repeat([GCM], len(X_index)))
        
        X_index_l.append(X_index)
        
        X_data_l.append(X_data)

        if standardize: 
        
            X_data_l_std.append(X_data_std)
        
    GCM_records = np.array(list(itertools.chain(*GCM_records)))

    X_index_l = np.array(list(itertools.chain(*X_index_l)))

    X_data_l = np.array(list(itertools.chain(*X_data_l)))

    if standardize: 
    
        X_data_l_std = np.array(list(itertools.chain(*X_data_l_std)))

        return X_data_l, X_data_l_std, X_index_l, GCM_records, scalers_dict
    
    else: 
        
        return X_data_l, X_index_l, GCM_records