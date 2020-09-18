def convert_rainfall(dset, varin='tprate', varout='precip', out_units='mm', time_var='time', drop_orig=True, clip=True): 
    """
    Converts rainfall that is in m.s**-1 (m/s) to mm in the CDS forecasts 
    
    Arguments
    -------- 
    
    dset : the xarray Dataset 
    varin : str, the name of the original variable ('tprate' is default)
    varout : str, the name of the variable after conversion ('precip' is default)
    out_units : str, the units after conversion, will be added to the attrs dict 
                of `varout`, mm is default
    time_var : str, the name of the time (init_time) variable, default 'time'
    drop_orig : Boolean, whether to drop the original variable (`varin`)
                default is True 
    clip : Boolean, whether or not to clip the results at 0
                default is True 
    
    Return
    ------ 
    
    dset : the converted xarray.Dataset 
    
    """

    # imports
    import pandas as pd
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    from calendar import monthrange
    
    # check that the rainfall is indeed in m.s-1
    in_units = dset[varin].attrs['units']
    
    if in_units != 'm s**-1': 
        
        print(f"! warning, expected units to be m.s**-1, but units {in_units}")
        
        pass
    
    else:
        # convert from m/s to mm/day 
        dset[varout] = (dset[varin] * 1000 * (24 * 60 * 60))
        
        # calculate the number of days per month, then multiply 
        init_dates = pd.to_datetime(dset[time_var].data).to_pydatetime()
        
        steps = dset.step.data
        
        ndays = []

        for date in init_dates: 
            n = [date + relativedelta(months=x) for x in steps]
            n = [monthrange(x.year, x.month)[1] for x in n]
            ndays.append(n)
        
        ndays = np.array(ndays)
        
        dset['ndays'] = ((time_var,'step'), ndays) 
        
        dset[varout] = dset[varout] * dset['ndays']
        dset[varout].attrs['units'] = 'mm'

        # clip 
        if clip: 
            dset[varout] = dset[varout].clip(min=0.0)
            
        # drop the original variable 
        if drop_orig:
            dset = dset.drop_vars(varin)
        
        return dset
