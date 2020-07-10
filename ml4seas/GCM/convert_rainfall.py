def convert_rainfall(dset, varin='tprate', varout='precip', out_units='mm', replace_step=True, drop_orig=True): 
    """
    Converts rainfall that is in m.s**-1 (m/s) to mm in the CDS forecasts 
    
    Arguments
    -------- 
    
    dset : the xarray Dataset 
    varin : str, the name of the original variable ('tprate' is default)
    varout : str, the name of the variable after conversion ('rain' is default)
    out_units : str, the units after conversion, will be added to the attrs dict 
                of `varout`, mm is default
    replace_step: Boolean, whether to replace the `step` variable by a integer list
                  default is True 
    drop_orig : Boolearn, whether to drop the original variable (`varin`)
                default is True 
    
    Return
    ------ 
    
    dset : the converted xarray.Dataset 
    
    """

    # imports
    import pandas as pd
    
    # check that the rainfall is indeed in m.s-1
    in_units = dset[varin].attrs['units']
    
    if in_units != 'm s**-1': 
        
        print(f"! warning, expected units to be m.s**-1, but units {in_units}")
        
        pass
    
    else:
        # convert from m/s to mm/day 
        dset[varout] = (dset[varin] * 1000 * (24 * 60 * 60))
        
        # calculate the number of days per month, then multiply 
        init_date = pd.to_datetime(dset.time.data)
        
        dset['forecast_horizon'] = (('step'), [init_date + (x-1) for x in dset.step.data])
        
        dset['ndays'] = (('step'), [pd.to_datetime(x).day for x in dset['forecast_horizon'].data])      
        
        dset[varout] = dset[varout] * dset['ndays']
        
        if replace_step: 
            dset['step'] = (('step'), list(range(1, len(dset['step'].data) + 1)))
        
        if drop_orig:
            dset = dset.drop_vars(varin)
        
        return dset
