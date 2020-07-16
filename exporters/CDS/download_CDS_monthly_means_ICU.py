#!/usr/bin/env python
# coding: utf-8

import cdsapi
import os
import urllib
import pathlib
import multiprocessing
from multiprocessing.pool import Pool

print("Number of cpu : ", multiprocessing.cpu_count())

HOME = pathlib.Path.home()

CWD = pathlib.Path.cwd()

provider = 'CDS'

opath = CWD.parents[2] / 'data' / 'GCMs' / 'downloads' / 'hindcasts' / provider

if not opath.exists(): 
    opath.mkdir(parents=True)

# dictionnary mapping the variable name (to be used in the downloaded filename) to the variable name in the CDS datasets
var_dict = {}
var_dict['T2M'] = '2m_temperature'
var_dict['PRECIP'] = 'total_precipitation'
var_dict['SST'] = 'sea_surface_temperature'
var_dict['Z850'] = 'geopotential'
var_dict['Z500'] = 'geopotential'

def fetch_CDS(args): 
    
    GCM = args[0]
    year = args[1]
    month = args[2]
    varname = args[3]
    opath = args[4]
    
    opath_gcm = opath / GCM / varname 
    
    if not opath_gcm.exists(): 
        opath_gcm.mkdir(parents=True)
        
    fname_out = pathlib.Path(opath_gcm / f"{provider}_{GCM}_{varname}_{year}_{month}.grib")
    
    varid = var_dict[varname]
    
    c = cdsapi.Client()
    
    if "Z" in varname:
        
        level = varname[-3:]
        
        try: 
    
            data = c.retrieve(
                'seasonal-monthly-pressure-levels',
                {
                    'originating_centre': GCM.lower(),
                    'variable': varid,
                    'pressure_level':level,
                    'product_type': 'monthly_mean',
                    'year': str(year),
                    'month': str(month).zfill(2),
                    'leadtime_month': [
                        '2', '3', '4',
                        '5', '6',
                    ],
                    'area': [80, -180, -80, 180],
                    'format': 'grib',
                },
                fname_out)
        except: 
            
            pass 
    
    else:
        
        try: 
        
            data = c.retrieve(
                'seasonal-monthly-single-levels',
                {
                    'originating_centre': GCM.lower(),
                    'variable': varid,
                    'product_type': 'monthly_mean',
                    'year': str(year),
                    'month': str(month).zfill(2),
                    'leadtime_month': [
                        '2', '3', '4',
                        '5', '6',
                    ],
                    'area': [80, -180, -80, 180],
                    'format': 'grib',
                },
                fname_out)
        except: 
            
            pass 
        
    if fname_out.exists(): 
        data.delete()
        print(f"{fname_out} downloaded OK")
    else: 
        print(f"failure to download or save {str(fname_out)}")

# ### list of GCMs 
list_GCMs = ['ECMWF','UKMO','METEO_FRANCE','CMCC','DWD']

# ### variable name 
varname = 'T2M'

# year = 2007
# months = list(range(8, 13))

# for month in months: 
#     # constructs the list of arguments for the function `fetch_CDS`
#     args = [(GCM, year, month, varname, opath) for GCM in list_GCMs]
#     # initialise the pool of workers
#     p = Pool(len(args))
#     # send the function to the workers 
#     p.map(fetch_CDS, args) 
 

### loop over the years and months 

for year in range(2007, 2016 + 1):
    for month in range(1, 12 + 1): 
        # constructs the list of arguments for the function `fetch_CDS`
        args = [(GCM, year, month, varname, opath) for GCM in list_GCMs]
        # initialise the pool of workers
        p = Pool(len(args))
        # send the function to the workers 
        p.map(fetch_CDS, args) 
