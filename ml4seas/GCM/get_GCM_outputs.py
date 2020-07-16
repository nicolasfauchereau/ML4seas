def get_GCM_outputs(provider='CDS', GCM='ECMWF', var_name='T2M', period='hindcasts', rpath=None, domain=[90, 300, -65, 50], step=None, verbose=False, flatten=True, nmembers=None, ensmean=False):

    """
    Get the GCM outputs for one GCM and one variable 

    added a test to see if the len of the time index is consistent ... 

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
    - nmembers: int, number of members to keep, necessary because some of the forecast datasets have more members than
    the hindcast datasets
    - ensmean: Boolean, whether to calculate the ensemble mean or not

    Return
    ------

    - dset: xarray.Dataset concatenated along the time dimension

    """


    import pathlib
    import numpy as np
    import pandas as pd
    import xarray as xr

    ipath = rpath / 'GCMs' / 'processed' / period / provider / GCM / var_name

    print(f"reading files from {str(ipath)}")

    if GCM  == 'JMA': 
        lfiles_gcm = list(ipath.glob(f"{GCM}_{var_name}_seasonal_anomalies_????_??.nc"))
    else: 
        lfiles_gcm = list(ipath.glob(f"{GCM}_{var_name}_seasonal_anomalies_interp_????_??.nc"))

    print(f"number of files in the archive: {len(lfiles_gcm)}")

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

        if 'surface' in dset.coords:
            dset = dset.drop('surface')
        if 'month' in dset.coords:
            dset = dset.drop('month')

        # remove singleton dimension
        dset = dset.squeeze()

        # select the domain

        if domain is not None:
            dset = dset.sel(lon=slice(domain[0], domain[1]), lat=slice(domain[2], domain[3]))
        if (step is not None) and ('step' in dset.coords):
            dset = dset.sel(step=step)

        if (nmembers is not None) and ('members' in dset.coords):
            dset = dset.isel(member=slice(0, nmembers))

        # calculate the ensemble mean if `ensmean` is defined
        if (ensmean) and ('member' in dset.coords):
            dset = dset.mean('member')

        if verbose:
            print(f"successfully opened and extracted {fname}")

        dset_l.append(dset)

    dset = xr.concat(dset_l, dim='time', coords='minimal', compat='override')

    # check whether the time dimension is consistent with a monotonic time index 

    tindex = dset.time.to_index()

    tmonotonic = pd.date_range(tindex[0], tindex[-1], freq='MS') 

    if not (len(tmonotonic) == len(tindex)): 
        
        print(f"\nWARNING: the length of the time index is {len(tindex)}, expected {len(tmonotonic)}\n")

        for y in np.unique(tindex.year):

            m_missing = list(set(list(range(1, 13))) - set(tindex[tindex.year == y].month.tolist())) 
            m_missing = ", ".join(map(str, m_missing))
            print(f"months missing for year {y}: {m_missing}")

    # now get the coordinates, will be returned along with the dataset itself,
    # regarding of whether the dataset is flattened

    #dims_tuple = (dset.dims, dset[var_name.lower()].dims

    if flatten:

        if 'member' in dset.dims:

            dset = dset.stack(z=('member','lat','lon'))

        else:

            dset = dset.stack(z=('lat','lon'))

    coords = dset.coords

    return dset, coords
