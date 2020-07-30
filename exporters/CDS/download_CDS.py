#!/usr/bin/env python
# coding: utf-8

import cdsapi
import os
import urllib
import pathlib
import argparse
from datetime import datetime
import multiprocessing
from multiprocessing.pool import Pool

print("Number of cpu : ", multiprocessing.cpu_count())

today = datetime.utcnow() 

HOME = pathlib.Path.home()

CWD = pathlib.Path.cwd()

provider = 'CDS'

parser = argparse.ArgumentParser()

parser.add_argument("--gcm", dest='gcm', 
                    help="gcm, can also be 'All'", 
                    type=str, required=False, default='All')

parser.add_argument("--datastream", dest='datastream', 
                    help="'hindcasts' (start --> 2016) or 'forecasts' (2017 --> now)", 
                    type=str, required=True, default=None)

parser.add_argument("--varname", dest='varname', 
                    help="variable names (in or all in [T2M, PRECIP, Z500, Z850, SST]",
					type=str,required=True, default=None)

parser.add_argument("--year", dest='year', 
                    help="year or list of years, or 'All'", 
                    type=str,required=False, default='All')

parser.add_argument("--month", dest='month', 
                    help="month or list of month, or 'All'",
					type=str,required=False, default='All')

parser.add_argument("--domain", dest='domain', 
                    help="domain: latmin,latmax,lonmin,lonmax", 
                    type=str, required=False, default="-90.,90.,-180.,180.")

parser.add_argument("--opath", dest='opath', 
                    help="the output path, can also be defined from the os.getenv", 
                    type=str, required=False, default=None)


args = parser.parse_args()

### parse the arguments 
gcms = args.gcm 
varname = args.varname 
year = args.year 
month = args.month
datastream = args.datastream
domain = args.domain
opath = args.opath

# type check, munging and casting into proper types 

# GCM(s)
if gcms == 'All': 
    gcms = ['ECMWF','UKMO','METEO_FRANCE','CMCC','DWD'] 
elif "," in gcms: 
    gcms = gcms.replace(" ","").split(",")

# puts into a list 
if not(isinstance(gcms, list)): gcms = [gcms]

# variable name(s)
if "," in varname: 
    varname = varname.replace(" ","").split(",")

if not(isinstance(varname, list)): varname = [varname]

# year or list of years 
if year == 'All' and datastream == 'hindcasts': 
    year = list(range(1993, 2016 + 1)) 
elif year == 'All' and datastream == 'forecasts': 
    year = list(range(2017, today.year))
elif ',' in year: 
    year = list(map(int, year.replace(' ','').split(',')))
else: 
    year = [year]

# month or list of months 
if month == 'All': 
    month = list(range(1, 12 + 1)) 
elif ',' in month: 
    month = list(map(int, month.replace(' ','').split(',')))
else: 
    month = [month]

print(month)

# Domain, casts into a tuple then unpack, and reorder 
domain = tuple(map(float, domain.replace(" ","").split(",")))

latmin, latmax, lonmin, lonmax = domain 

domain = [latmax, lonmin, latmin, lonmax]

# output path, can be taken (in that order) the environment or passed as a parameter
try: 
    opath = pathlib.Path(os.getenv('OPATH'))
    if args.opath is not None: 
        opath = pathlib.Path(args.opath) 
except: 
    print("opath was not defined, defaulting to '.'")
    opath = pathlib.Path('.')

# dictionnary mapping the variable name (to be used in the downloaded filename) to the variable name in the CDS datasets
var_dict = {}
var_dict['T2M'] = '2m_temperature'
var_dict['PRECIP'] = 'total_precipitation'
var_dict['SST'] = 'sea_surface_temperature'
var_dict['Z850'] = 'geopotential'
var_dict['Z500'] = 'geopotential'

# define the function to fetch the CDS forecasts or hindcasts 

def fetch_CDS(args): 
    
    GCM = args[0]
    year = args[1]
    month = args[2]
    varname = args[3][0]
    domain = args[4]
    opath = args[5]
    
    print(GCM)

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
                    'area': domain,
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
                    'area': domain,
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


## loop over the years and months 

print(gcms)

for y in year:
    for m in month: 
        # constructs the list of arguments for the function `fetch_CDS`
        args = [(gcm, y, m, varname, domain, opath) for gcm in gcms]

        print(args)

        # initialise the pool of workers
        p = Pool(len(args))
        # send the function to the workers 
        p.map(fetch_CDS, args) 