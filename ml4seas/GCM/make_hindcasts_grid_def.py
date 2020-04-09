def make_hindcasts_grid_def(provider='CDS', GCM='ECMWF', var_name='T2M', rpath='gdata', year=2016, month=12): 
    """
    make a grid definition from the hindcasts, for e.g. regridding of the forecasts 
    if they are on a inconsistent grid .. 
    
    also adds a `n_members` global attribute to the grid, to be used to select the 
    same number of members in the ensemble in the forecasts 
    
    
    Parameters
    ----------
    
    - provider : str, default 'CDS'
    - GCM : str, default 'ECMWF'
    - var_name: str, should be in ['T2M','PRECIP'] for now, default to 'T2M'
    - rpath : the root path to the `data` folder, in ['gdata','local','network']
    - year : int, the year for the file that will be read as a template, default to 2016 
        (last year of the hindcast period)
    - month : int, the month for the file that will be read as a template, default to 12 
        (last month of the hindcast period)

    Returns
    -------
    
    - grid : xarray Dataset, with lat and lon coordinates and variables only, 
        and the `n_members` attribute

    """
    
    import pathlib 
    import xarray as xr
    from ..utils import set_root_dir
    if var_name is None:
        var_name = 'T2M'
        dpath = pathlib.Path(set_root_dir(root=rpath) / 'GCMs' / 'processed' / 'hindcasts' / provider / GCM / var_name)
    if year is None: 
        year = 2016
    if month is None: 
        month = 12
    
    dset = xr.open_dataset(dpath / f"{GCM}_{var_name}_monthly_anomalies_{year}_{month}.nc")
    
    if member in dset.dims: 
        n_members = dset.dims['member']

    grid = dset[['lat','lon']]
    
    if 'surface' in grid.coords: 
        grid = grid.drop('surface')
    if 'month' in grid.coords: 
        grid = grid.drop('month')
        
    grid.attrs['n_members'] = n_members 
    
    return grid 
