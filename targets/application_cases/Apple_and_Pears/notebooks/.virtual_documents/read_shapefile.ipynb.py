get_ipython().run_line_magic("matplotlib", " inline")


import pathlib


from matplotlib import pyplot as plt


import geopandas as gpd


import pandas as pd


HOME = pathlib.Path.home()


root_path = HOME.joinpath('research/Smart_Ideas/data/shapefiles/application_cases/Apple_and_Pears') 


shapes = gpd.read_file(root_path.joinpath('Hawkes_Bay_Orchard_Bubbles.shp'))


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


import xarray as xr


xr.Dataset(d)


dset = xr.Dataset(d)


dset.to_netcdf(root_path.joinpath('Apple_and_Pears_bounding_box.nc'))


df = shapes.to_crs(epsg=3857)


import contextily as ctx


ax = df.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
# ctx.add_basemap(ax, url=ctx.providers.Stamen.TonerLite)
ctx.add_basemap(ax, url=ctx.providers.Esri.WorldStreetMap)
ax.set_axis_off()


f, ax = plt.subplots(figsize=(6,10))
df.plot(alpha=0.5, edgecolor='k',ax=ax)
# ctx.add_basemap(ax, url=ctx.providers.Stamen.TonerLite)
ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerBackground)
ax.set_axis_off()


f, ax = plt.subplots(figsize=(6,10))
df.plot(alpha=0.5, edgecolor='k',ax=ax)
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
ax.set_axis_off()
f.savefig('./basemap_plot_contextily.png', dpi=200, bbox_inches='tight')



