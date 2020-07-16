import importlib.util

package_name = 'xesmf'

spec = importlib.util.find_spec(package_name)

if spec is None:
    print(package_name +" is not installed, using method `interp_like` for interpolation")
    def regrid(ds_in, target_ds):
        """
        regrid utility using the `interp_like` method of
        an xarray dataset 
        
        Parameters
        ==========
        
        ds_in : xarray dataset, the input dataset 
        target_ds : xarray dataset, the output grid definition 
        
        Return
        ======
        
        ds_out : xarray dataset, the output dataset, interpolated
        
        """
        ds_out = ds_in.interp_like(target_ds)
        return ds_out
else: 
    print("xesmf installed, ")
    def regrid(ds_in, target_ds,  method='bilinear'):
        """
        regrid utility using the `Regridder` method of
        the `xesmf` package (see https://xesmf.readthedocs.io/en/latest/index.html)
        
        Parameters
        ==========
        
        ds_in : xarray dataset, the input dataset 
        target_ds : xarray dataset, the output grid definition 
        
        Return
        ======
        
        ds_out : xarray dataset, the output dataset, interpolated
        
        """
        import xesmf as xe
        """Convenience function for one-time regridding"""
        regridder = xe.Regridder(ds_in, target_ds, method, periodic=True)
        ds_out = regridder(ds_in)
        regridder.clean_weight_file()
        return ds_out
