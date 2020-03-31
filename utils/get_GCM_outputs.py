def get_GCM_outputs(provider='CDS', GCM='ECMWF', var_name='T2M', period='hindcasts', rpath=None, domain=[90, 300, -65, 50], step=None, verbose=False, flatten=True):
    
    """
    Get the GCM outputs 
    
    Parameters
    ----------
    
    - provider: in ['CDS','IRI','JMA'] 
    - GCM: name of the GCM 
    - var_name: in ['T2M', 'PRECIP']
    - period: in ['hindcasts', 'forecasts']
    - rpath (root path, pathlib.Path object, see `set_root_dir` in the utils module)
    - domain [lon_min, lon_max, lat_min, lat_max]
    - step ( in [3, 4, 5] )
    - verbose: Boolean, whether to print names of files successfully opened
    - flatten: Boolean, whether of not to stack the dataset over the spatial (+ member if present) dimension
    to get 2D fields
    
    Return
    ------ 
    
    - dset: xarray.Dataset concatenated along the time dimension 

    """
    
    
    import pathlib
    import xarray as xr
    
    ipath = rpath /  'GCMs'/ 'processed' / period / provider / GCM / var_name
    
    lfiles_gcm = list(ipath.glob(f"{GCM}_{var_name}_seasonal_anomalies_interp_????_??.nc"))
    
    if (period == 'hindcasts') and (len(lfiles_gcm) ) < 200: 
        print(f"Something wrong with the number of files in the list for the {period} period, the length is {len(lfiles_gcm)}")
    if (period == 'forecasts') and (len(lfiles_gcm) ) < 20:
        print(f"Something wrong with the number of files in the list for the {period} period, the length is {len(lfiles_gcm)}")
    
    lfiles_gcm.sort()
    
    print(f"first file is {str(lfiles_gcm[0])}")
    print(f"last file is {str(lfiles_gcm[-1])}")

    dset_l = []
    
    for fname in lfiles_gcm: 
        
        dset = xr.open_dataset(fname)[[var_name.lower()]]

        
        # select the domain 
        
        if domain is not None: 
            dset = dset.sel(lon=slice(domain[0], domain[1]), lat=slice(domain[2], domain[3]))
        if step is not None: 
            dset = dset.sel(step=step)
         
                
        if verbose: 
            print(f"successfully opened and extracted {fname}")
    
        dset_l.append(dset)

    dset = xr.concat(dset_l, dim='time')

    if flatten: 
        
        if 'member' in dset.dims: 
            
            dset = dset.stack(z=('member','lat','lon'))
        
        else: 
            
            dset = dset.stack(z=('lat','lon'))
    
    return dset 
