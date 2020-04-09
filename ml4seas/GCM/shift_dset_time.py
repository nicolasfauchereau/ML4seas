def shift_dset_time(dset, name='time', step=3, end_month = True): 
    """
    Shift the time index of a xarray.Dataset by the specified number of steps (in month)
    
    Parameters
    ----------
    - name: str, the name of the time variable (usually 'time')
    - step: the number of steps (in months) by which to shift the time index 
    - end_month: Boolean, if True, the day of the month is set to be the last 
    day of the month. Note that if the xarray Dataset, the day or the month is not 
    equal to 1, it will return an error and fail 
    
    Returm
    ------ 
    
    - dset: the xarray.Dataset with the shifted time variable 
    
    """
    
    import numpy as np
    
    if end_month: 
        if not (np.alltrue(np.ones(len(dset[name].to_index())) == dset[name].to_index().day.values)): 
            print("""warning, the end_month argument is set to True,
            but the time variable does NOT start at the beinning of the month
            """)
        else: 
            dset[name] = dset.time.to_index().shift(periods = step + 1, freq='M')
    else: 
        dset[name] = dset.time.to_index().shift(periods = step, freq='MS')
    
    return dset 
