def shift_to_month_end(dset, name='time'): 
    """
    shift the time index of a dataset, dataarray, dataframe or series
    to the end of the month

    Parameters
    ----------
    dset : dataset, dataarray, dataframe or series  
        the input 
    name : str, optional
        the name of the time variable if a dataset or dataarray, 
        by default 'time'

    Returns
    -------
        dataset, dataarray, dataframe or series
        with the time shifted to the end of the month
    """
    import pandas as pd
    import xarray as xr 
    
    if isinstance(dset, xr.Dataset) or isinstance(dset, xr.DataArray): 
        dset[name] = dset['time'].to_index() + pd.offsets.MonthEnd(0)
        
    elif isinstance(dset, pd.DataFrame) or isinstance(dset, pd.Series): 
        dset.index = dset.index + pd.offsets.MonthEnd(0)
        
    return dset 