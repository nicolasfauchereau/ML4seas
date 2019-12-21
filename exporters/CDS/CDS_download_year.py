import pathlib
import cdsapi

HOME = pathlib.Path.home()

centre = 'ecmwf'

var_dict = {}
var_dict['T2M'] = '2m_temperature'

var_name = 'T2M'

dpath = HOME / 'research' / 'Smart_Ideas' / 'data' / centre.upper() / var_name

if not dpath.exists():
    dpath.mkdir(parents=True)

c = cdsapi.Client()

for year in range(1993, 2019):

    print(f"downloading {centre.upper()} {var_name} hindcasts for year {year}")

    c.retrieve(
        'seasonal-monthly-single-levels',
        {
            'originating_centre':'ecmwf',
            'system':'5',
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
        f'{str(dpath)}/{centre.upper()}_{var_name}_{year}.grib')