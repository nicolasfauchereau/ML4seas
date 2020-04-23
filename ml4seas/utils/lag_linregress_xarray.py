def lag_linregress_xarray(x, y, lagx=0, lagy=0):
    """
    Calculates the regression metrics: 
    
    Covariance, correlation, regression slope and intercept, p-value, and standard error on regression
    
    between 2 xarray DataArrays along the time dimension 
    
    Arguments
    ---------
    
    x : xr.DataArray, the independant ND DataArray, must contain a time dimension 
    y : xr.DataArray, the dependant ND DataArray, must contain a time dimension 
    lagx : the time shift in x (signed integer)
    lagy : the time shift in y (signed integer)
    
    Return
    ------
    
    Covariance
    correlation
    regression
    slope
    intercept
    p-value
    standard error on regression
    
    """ 
    
    import numpy as np
    import xarray as xr
    from scipy.stats import t
    
    # Ensure that the data are properly alinged to each other. 
    x,y = xr.align(x,y)
    
    # Add lag information if any, and shift the data accordingly
    if lagx != 0:
        # If x lags y by 1, x must be shifted 1 step backwards. 
        # But as the 'zero-th' value is nonexistant, xr assigns it as invalid (nan). Hence it needs to be dropped
        x   = x.shift(time = -lagx).dropna(dim='time')
        # Next important step is to re-align the two datasets so that y adjusts to the changed coordinates of x
        x,y = xr.align(x,y)

    if lagy!=0:
        y   = y.shift(time = -lagy).dropna(dim='time')
        x,y = xr.align(x,y)
 
    # Compute data length, mean and standard deviation along time axis for further use: 
    n     = x.shape[0]
    xmean = x.mean(axis=0)
    ymean = y.mean(axis=0)
    xstd  = x.std(axis=0)
    ystd  = y.std(axis=0)
    
    # Compute covariance along time axis
    cov   =  np.sum((x - xmean)*(y - ymean), axis=0)/(n)
    
    # Compute correlation along time axis
    cor   = cov/(xstd*ystd)
    
    # Compute regression slope and intercept:
    slope     = cov/(xstd**2)
    intercept = ymean - xmean*slope  
    
    # Compute P-value and standard error
    # Compute t-statistics
    
    tstats = cor*np.sqrt(n-2)/np.sqrt(1-cor**2)
    
    stderr = slope/tstats
    
    pval   = t.sf(tstats, n-2)*2
    
    pval   = xr.DataArray(pval, dims=cor.dims, coords=cor.coords)

    return cov,cor,slope,intercept,pval,stderr
