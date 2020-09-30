get_ipython().getoutput("pwd")


get_ipython().run_line_magic("matplotlib", " inline")


import pathlib


from matplotlib import pyplot as plt


import geopandas as gpd


import pandas as pd


shapes_path = pathlib.Path()


shapes = gpd.read
