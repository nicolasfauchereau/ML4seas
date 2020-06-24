def convert_rainfall(dset, varin='tprate', varout='rain', out_units='mm', replace_step=True, drop_orig=True): 
    # check that the rainfall is indeed in m.s-1
    in_units = dset[varin].attrs['units']
    if in_units != 'm s**-1': 
        print(f"! warning, expected units to be m.s**-1, but units {in_units}")
        pass
    else:
        dset[varout] = (dset[varin] * 1000 * (24 * 60 * 60))
        init_date = pd.to_datetime(dset.time.data)
        dset['forecast_horizon'] = (('step'), [init_date + (x-1) for x in dset.step.data])
        dset['ndays'] = (('step'), [pd.to_datetime(x).day for x in dset['forecast_horizon'].data])      
        dset[varout] = dset[varout] * dset['ndays']
        
        if replace_step: 
            dset['step'] = (('step'), list(range(1, len(dset['step'].data) + 1)))
        
        if drop_orig:
            dset = dset.drop_vars(varin)
        
        return dset
