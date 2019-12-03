import sys
import pathlib
import cdsapi
from multiprocessing.pool import Pool

HOME = pathlib.Path.home()

var_dict = {}

# dictionnary mapping the variable name (to be used in the downloaded filename) to the variable name in the CDS datasets

var_dict['T2M'] = '2m_temperature'
var_dict['PRECIP'] = 'total_precipitation'
var_dict['Z850'] = 'geopotential'
var_dict['Z500'] = 'geopotential'

# var_name is passed as an unnamed argument to the script, e.g.:

# python download_CDS_year_multiprocessing.py T2M

var_name = sys.argv[1]

print(var_name)

# define the level from the var_name
if "Z" in var_name:
    level = var_name[-3:]

# list of tuple mapping centre to available system for the hindcasts
centre_system = [('ecmwf','5'), ('ukmo','13'), ('meteo_france','6'), ('dwd','2'), ('cmcc','3')]

# the number of threads needs to be set to the number of centres
workers = len(centre_system)

# define the function that fetches the hindcasts from the CDS
def fetch_hindcast(centre_no):

    centre = centre_system[centre_no][0]
    system = centre_system[centre_no][1]

    dpath = HOME / 'research' / 'Smart_Ideas' / 'data' / 'GRIB' / centre.upper() / var_name

    if not dpath.exists():
        dpath.mkdir(parents=True)

    if "Z" in var_name:

        c = cdsapi.Client()

        c.retrieve(
            'seasonal-monthly-pressure-levels',
            {
                'originating_centre':centre,
                'system':system,
                'variable':var_dict[var_name],
                'pressure_level':level,
                'product_type':'monthly_mean',
                'year':str(year),
                'month':[
                    '01','02','03',
                    '04','05','06',
                    '07','08','09',
                    '10','11','12'
                ],
                'leadtime_month':[
                    '2','3','4',
                    '5','6'
                ],
                'format':'grib'
            },
            f'{str(dpath)}/{centre.upper()}_system_{system}_{var_name}_{year}.grib'))

    else:

        c = cdsapi.Client()

        for year in range(1993, 2016 + 1):

            print(f"downloading {centre.upper()} {var_name} hindcasts for year {year}")

            c.retrieve(
                'seasonal-monthly-single-levels',
                {
                    'originating_centre':centre,
                    'system':system,
                    'variable':var_dict[var_name],
                    'product_type':'monthly_mean',
                    'year':str(year),
                    'month':[
                        '01','02','03',
                        '04','05','06',
                        '07','08','09',
                        '10','11','12'
                    ],
                    'leadtime_month':[
                        '2','3','4',
                        '5','6'
                    ],
                    'format':'grib'
                },
                f'{str(dpath)}/{centre.upper()}_system_{system}_{var_name}_{year}.grib')


# initialise a Pool with the

p = Pool(workers)

p.map(fetch_hindcast, list(range(workers)))