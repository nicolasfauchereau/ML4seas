import warnings
warnings.filterwarnings("ignore")


get_ipython().run_line_magic("matplotlib", " inline")


import pathlib


from matplotlib import pyplot as plt


import geopandas as gpd
import regionmask


import numpy as np 
import pandas as pd
import xarray as xr


HOME = pathlib.Path.home()


root_path = HOME.joinpath('research/Smart_Ideas/data/shapefiles/application_cases/InnovationVineyards') 


shapes = gpd.read_file(root_path.joinpath('Innovationvineyardpolygon-polygon.shp'))


shapes.crs


shapes = shapes.to_crs('epsg:4272')


shapes.crs


shapes.plot()


bounds = shapes.bounds


bounds 


minx, maxx = bounds.minx.min(), bounds.maxx.max()


miny, maxy = bounds.miny.min(), bounds.maxy.max()


coords = [minx, maxx, miny, maxy]


coords


d = {}
d['lonmin'] = coords[0]
d['lonmax'] = coords[1]
d['latmin'] = coords[2]
d['latmax'] = coords[3]


xr.Dataset(d)


dset = xr.Dataset(d)


dset.to_netcdf(root_path.joinpath('Innovation_Vineyard_bounding_box.nc'))


df = shapes.to_crs(epsg=3857)


import contextily as ctx


f, ax = plt.subplots(figsize=(6,10))
df.plot(alpha=0.5, edgecolor='k',ax=ax)
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
ax.set_axis_off()
f.savefig('./basemap_plot_contextily.png', dpi=200, bbox_inches='tight')


dpath_vcsn = pathlib.Path('/home/nicolasf/operational/VCSN/data/NC/DAILY') 


variables_list = ['TMEAN_N', 'TMIN_N', 'TMAX_N', 'RAIN_BC', 'SOILM', 'RAD']


varnames_list  = ['Tmean_N', 'Tmin_N', 'Tmax_N', 'Rain_bc', 'SoilM', 'Rad']


var_dict = dict(zip(variables_list, varnames_list))


var_dict


for varname in variables_list: 
    
    print(f"extracting and processing {varname}")
    
    ### get the list of files 
    lfiles = list(dpath_vcsn.joinpath(varname).glob("VCSN_gridded_daily*_????-??.nc"))
    lfiles.sort()
    
    ### read 
    vcsn_dset = xr.open_mfdataset(lfiles, concat_dim='time', parallel=True)
    
    ### define the region 
    #     region_definition = regionmask.from_geopandas(shapes)
    
    ### select the point (centroid of the region)
    point = vcsn_dset.sel(lat = float(shapes.centroid.y), lon=float(shapes.centroid.x), method='nearest')
    
    ### casts into a DataFrame 
    df = point[var_dict[varname]].load().to_dataframe() 
    
    ### saves to disk 
    opath = HOME.joinpath(f"research/Smart_Ideas/outputs/targets/application_cases/Innovation_Vineyard/{varname}") 
    
    if not(opath.exists()): 
        opath.mkdir(parents=True)
        
    df.to_csv(opath.joinpath(f"Daily_{varname}.csv"))
    
    vcsn_dset.close() 
    
    point.close() 
