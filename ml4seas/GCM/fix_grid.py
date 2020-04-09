def fix_grid(dset, rename=True): 
    
    """
    add attributes to lon and lat, after renaming dimensions 
    and sorting by latitude
    """
    if rename: 
        if 'latitude' in dset.dims: 
            dset = dset.rename({'latitude':'lat'})
        if 'longitude' in dset.dims:
            dset = dset.rename({'longitude':'lon'})
        if 'number' in dset.dims: 
            dset = dset.rename({'number':'member'})
        
    if dset['lat'].data[0] > dset['lat'].data[-1]: 
        dset = dset.sortby('lat')
    
    if (dset['lat'].data[0] == -90) and (dset['lat'].data[-1] != 90): 
        dset = dset.sel(lat=slice(-89.5, 89.5))    
    
    dset['lon'].attrs["long_name"] = "longitude"
    dset['lon'].attrs["units"] = "degrees_east"
    dset['lat'].attrs["long_name"] = "latitude"
    dset['lat'].attrs["units"] = "degrees_north"    
    
    return dset
