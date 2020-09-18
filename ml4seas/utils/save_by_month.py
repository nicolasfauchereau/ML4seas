def save_by_month(dset, opath=None, provider=None, GCM=None, varname=None, append='monthly_anomalies', verbose=True): 
    """
    saves each month in a dataset in a separate netcdf file in {opath}
    """

    import pathlib
    import numpy as np 
    import pandas as pd 

    if opath is None:
        opath = pathlib.Path('.')
    
    for date in pd.to_datetime(dset.init_time.data): 
        sub = dset.sel(init_time=date)
        fname_out = f"{provider}_{GCM}_{varname}_{date.year}-{str(date.month).zfill(2)}_{append}.nc"
        sub.to_netcdf(opath.joinpath(fname_out)) 
        if verbose:
            if opath.joinpath(fname_out).exists(): 
                print(f"successfully saved {fname_out}")
        sub.close() 
