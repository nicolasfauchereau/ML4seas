def make_forecast_valid_time(dset, nsteps=3, rdelta=3): 
    from dateutil.relativedelta import relativedelta
    import pandas as pd
    import numpy as np
    time = dset.time.to_series()
    tv = [x + relativedelta(months=m + (rdelta - 1)) for m in range(1, nsteps + 1) for x in time]
    tv = np.array(tv)
    tv = tv.reshape((len(tv) // nsteps,nsteps))
    dset['forecast_valid_time'] = (('time','step'), tv)
    return dset
