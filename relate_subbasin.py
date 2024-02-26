import os
import shutil
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

basin_file = 'D:/Maskey/Project/NCAAR/AWRA/Spatial analysis/Watershed analysis/Shapefile/Delineated watershed_v2.shp'
weather_file = 'D:/Maskey/Data_analysis/PRISM/Spatial_data/Shapefile/Mississippi/Mississippi_weather_stations.shp'
df_file = 'D:/Maskey/Project/NCAAR/AWRA/Data/Subarea_info.csv'
gdf_basin = gpd.read_file(basin_file)
gdf_station = gpd.read_file(weather_file)
crs_basin = gdf_basin.crs.to_epsg()
crs_station = gdf_station.crs.to_epsg()
gdf_station = gdf_station.set_crs(crs_basin, allow_override=True)

gdf_basin_new = gpd.GeoDataFrame()
for i in range(gdf_basin.shape[0]):
    gdf_basin_i = gpd.GeoDataFrame(gdf_basin.iloc[i, :]).T
    stn1 = str(gdf_basin.Station[i])
    gdf_station_i = gdf_station[gdf_station.stnid==stn1]
    gdf_station_i = gdf_station_i.drop('geometry', axis=1)
    gdf_station_i.index = [i]
    gdf_i = pd.concat([gdf_basin_i, gdf_station_i], axis=1)
    gdf_basin_new = pd.concat([gdf_basin_new, gdf_i], axis=0)
df_basin_new = pd.DataFrame(gdf_basin_new)
df_basin_new = df_basin_new[['OBJECTID', 'GRIDCODE', 'Subbasin', 'Area', 'Slo1', 'Len1', 'Sll', 'Lat', 'Long_',
                         'Elev', 'ElevMin', 'ElevMax', 'Shape_Area', 'HydroID', 'OutletID', 'Station',
                         'Name', 'Longitude', 'Latitude', 'Elevation(', 'stnid']]

df_basin_new.to_csv(df_file, index=None)