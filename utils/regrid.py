def regrid(ds_in, target_ds,  method='bilinear', reuse_weight=True):
    import xesmf as xe
    """Convenience function for one-time regridding"""
    if reuse_weight:
        regridder = xe.Regridder(ds_in, target_ds, method, periodic=True, reuse_weights=True)
    else: 
        regridder = xe.Regridder(ds_in, target_ds, method, periodic=True, reuse_weights=False)
    ds_out = regridder(ds_in)
    if not reuse_weight:
        regridder.clean_weight_file()
    return ds_out
