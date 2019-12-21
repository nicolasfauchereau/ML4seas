def regrid(ds_in, target_ds,  method='bilinear'):
    import xesmf as xe
    """Convenience function for one-time regridding"""
    regridder = xe.Regridder(ds_in, target_ds, method, periodic=True)
    ds_out = regridder(ds_in)
    regridder.clean_weight_file()
    return ds_out
