def download_CDS(GCM='ECMWF', varname='t2m', year=None, month=None, leadtimes=[1,2,3], opath=None, domain=[20, 120, -50, 180], file_format='grib', level='surface'): 
    """
    downloads a t2a or tpara forecast from the CDS for a given GCM, year and month 

    Parameters
    ----------
    GCM : str, optional
        The name of the GCM [in 'ECMWF','UKMO,'METEO_FRANCE','CMCC, 'DWD', 'NCEP'], by default 'ECMWF'
    varname : str, optional
        Variable name in ['t2a','tpara'], by default 't2a'
    year : int, optional
        The year, by default None
    month : int, optional
        The month, by default None
    leadtimes : list, optional
        The list of lead times in months (0 being the initial time), by default [1,2,3]
    opath : string or pathlib.Path, optional
        The path were to save the forecast files (grib), by default None
    domain : list, optional
        The geographical domain. WARNING !: must be [latN, lonW, latS, lonE], by default [20, 120, -50, 180]
    file_format : string, by default 'grib'
        The file format the file will be downloaded into
    level: str or int, default 'surface'
        The level, either 'surface' (a string) or an int in [950, 500, 200] or appropriate level
    """
    
    # imports -----------------------
    import pathlib
    from datetime import datetime
    import cdsapi
    from collections import OrderedDict
    # ------------------------------- 
    
    # defines a dictionnary that maps variable name 

    dvar = OrderedDict()

    if level == 'surface': 

        dvar = OrderedDict()

        # `raw` values, single levels 
        dvar['t2m'] = ['seasonal-monthly-single-levels', '2m_temperature']
        dvar['tprate'] = ['seasonal-monthly-single-levels','total_precipitation']
        dvar['sst'] = ['seasonal-monthly-single-levels','sea_surface_temperature']
        dvar['10m uwind'] = ['seasonal-monthly-single-levels','10m_u_component_of_wind']
        dvar['10m vwind'] = ['seasonal-monthly-single-levels','10m_v_component_of_wind']
        dvar['mslp'] = ['seasonal-monthly-single-levels','mean_sea_level_pressure']
        dvar['latent heat flux'] = ['seasonal-monthly-single-levels','surface_latent_heat_flux']
        dvar['solar radiation'] = ['seasonal-monthly-single-levels','surface_solar_radiation']

        # anomalies, single levels
        dvar['t2m anomaly'] = ['seasonal-postprocessed-single-levels', '2m_temperature_anomaly']
        dvar['tprate anomaly'] = ['seasonal-postprocessed-single-levels', 'total_precipitation_anomalous_rate_of_accumulation']
        dvar['sst anomaly'] = ['seasonal-postprocessed-single-levels', 'sea_surface_temperature_anomaly']
        dvar['10m uwind anomaly'] = ['seasonal-postprocessed-single-levels','10m_u_component_of_wind_anomaly']
        dvar['10m vwind anomaly'] = ['seasonal-postprocessed-single-levels','10m_v_component_of_wind_anomaly']
        dvar['mslp anomaly'] = ['seasonal-postprocessed-single-levels','mean_sea_level_pressure_anomaly']
        dvar['latent heat flux anomaly'] = ['seasonal-postprocessed-single-levels','surface_latent_heat_flux_anomalous_rate_of_accumulation']
        dvar['solar radiation anomaly'] = ['seasonal-postprocessed-single-levels', 'surface_solar_radiation_anomalous_rate_of_accumulation']

    else:
        
        dvar = OrderedDict()
        
        # `raw` values, pressure levels 
        dvar['geopotential'] = ['seasonal-monthly-pressure-levels', 'geopotential']
        dvar['temperature'] = ['seasonal-monthly-pressure-levels', 'temperature']
        dvar['uwind'] = ['seasonal-monthly-pressure-levels', 'u_component_of_wind']
        dvar['vwind'] = ['seasonal-monthly-pressure-levels', 'v_component_of_wind']
        dvar['specific humidity'] = ['seasonal-monthly-pressure-levels', 'specific_humidity']
        
        # anomalies, pressure levels 
        dvar['geopotential anomaly'] = ['seasonal-postprocessed-pressure-levels', 'geopotential']
        dvar['temperature anomaly'] = ['seasonal-postprocessed-pressure-levels', 'temperature']
        dvar['uwind anomaly'] = ['seasonal-postprocessed-pressure-levels', 'u_component_of_wind']
        dvar['vwind anomaly'] = ['seasonal-postprocessed-pressure-levels', 'v_component_of_wind']
        dvar['specific humidity anomaly'] = ['seasonal-postprocessed-pressure-levels', 'specific_humidity']


    # if year and month are not passed, take the current year and month 
    if year is None and month is None: 
        
        year = datetime.utcnow().year

        month = datetime.utcnow().month
    
    # if the output path is not defined, will create a folder
    # corresponding to the GCM in the CURRENT directory 
    
    if opath is None: 
        
        opath = pathlib.Path.cwd()
        
        opath = opath.joinpath(GCM)

    else:

    # if opath is defined, but is a string, we cast into pathlib.Path
        
        if not(isinstance(opath, pathlib.Path)): 
            
            opath = pathlib.Path(opath)
    
    # creates the path if not existing on disk
    if not(opath.exists()):
        
        opath.mkdir(parents=True)

    # build the filename for output 

    if level == 'surface': 

        # if surface level

        fname_out = opath.joinpath(f"ensemble_seas_forecasts_{varname.replace(' ','_')}_from_{year}_{month}_{GCM}.{file_format}")

        # if the filename has already been downloaded, skip and return the path 
        
        if fname_out.exists():
            
            print(f"{str(fname_out)} exists already on disk, skipping download") 

            return fname_out

        # else, connect to the CDS and retrieve file ...
        
        else: 
            
            while not(fname_out.exists()): 
            
                try: 

                    print(f"attempting to download {varname} for GCM {GCM}, for level {level}, year {year}, month {month}, in {file_format}\n")
                    
                    c = cdsapi.Client()

                    data = c.retrieve(
                    
                    dvar[varname][0],
                    {
                        'format':file_format,
                        'originating_centre':GCM.lower(),
                        'variable':dvar[varname][1],
                        'product_type':'monthly_mean',
                        'year':str(year),
                        'month':str(month).zfill(2),
                        'leadtime_month': list(map(str, [x+1 for x in leadtimes])), 
                        'area': domain,
                    },
                    fname_out)

                    if fname_out.exists(): 
                    
                        data.delete()

                        print(f"{fname_out} downloaded OK")

                        return fname_out

                except: 
                    
                    print(f"failure to download or save {str(fname_out)}")
        
    else: 
        
        fname_out = opath.joinpath(f"ensemble_seas_forecasts_{varname.replace(' ','_')}_Z{str(level)}_from_{year}_{month}_{GCM}.{file_format}")

        # if the filename has already been downloaded, skip, and return the path 
        
        if fname_out.exists():

            print(f"{str(fname_out)} exists already on disk, skipping download") 

            return fname_out

        # else, connect to the CDS and try retrieve file ...
        
        else: 
            
            while not(fname_out.exists()):
                        
                try: 
                    
                    print(f"attempting to download {varname} for GCM {GCM}, for level {level}, year {year}, month {month}, in {file_format}\n")

                    c = cdsapi.Client()

                    data = c.retrieve(
                    
                    dvar[varname][0],
                    {
                        'format':file_format,
                        'originating_centre':GCM.lower(),
                        'variable':dvar[varname][1],
                        'pressure_level': str(level), 
                        'product_type':'monthly_mean',
                        'year':str(year),
                        'month':str(month).zfill(2),
                        'leadtime_month': list(map(str, [x+1 for x in leadtimes])), 
                        'area': domain,
                    },
                    fname_out)

                    if fname_out.exists():
                    
                        data.delete()

                        print(f"{fname_out} downloaded OK")

                        return fname_out

                except: 

                    print(f"failure to download or save {str(fname_out)}") 