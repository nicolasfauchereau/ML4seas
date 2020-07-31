def train_scaler(dset, varname=None, row_dim='time', transform=True): 
    """
    Train a Standard Scaler on a Dataset along the time dimension 
    and return the Standardised dataset (optionally)

    Parameters
    ----------

    Return 
    ------ 

    dset : the dataset with variable standardized 
            None if `transform` = False 

    scaler : the trained standard scaler

    Example
    ------- 

    dset, scaler = train_scaler(dset, varname = 't2m', transform=True)

    or 

    _, scaler = train_scaler(dset, varname='t2m, transform=False) 
    """
    
    try: 
        from dask_ml.preprocessing import StandardScaler
    except: 
        from sklearn.preprocessing import StandardScaler
        
    dset = dset[varname]
    space_dims = tuple(x for x in dset.dims if x != row_dim)
    dset_stack = dset.stack(z=space_dims) 
    scaler = StandardScaler()
    if transform: 
        data_std = scaler.fit_transform(dset_stack.data)
        dset_stack.data = data_std
        dset = dset_stack.unstack()
        return dset, scaler
    else:
        return None, scaler