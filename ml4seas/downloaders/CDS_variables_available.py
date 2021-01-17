from pprint import pprint

dvar = {}

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

def print(): 
    pprint(dvar)
