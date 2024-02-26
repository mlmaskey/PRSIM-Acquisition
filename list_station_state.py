import geopandas as gpd
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from Utility import create_save_folder
from Utility import get_list

file_shp = '../../Spatial_dataset/US_State/tl_2021_us_state.shp'
out_dir = create_save_folder(root_dir='D:/Maskey/Data_analysis/PRISM', sub_dir='Spatial_data')
out_dir = create_save_folder(root_dir=out_dir, sub_dir='Shapefile')
gdf_US = gpd.read_file(file_shp)
shape_file = os.path.join(out_dir, f'US_Boundary.shp')
gdf_US.to_file(shape_file)
state_name = 'Mississippi'
out_dir = create_save_folder(root_dir=out_dir, sub_dir=state_name)
data_dir = 'X:/Mahesh.Maskey/Data/Climate/'

df_station_ppt, gdf_STATE_ppt, gdf_state_ppt, df_state_ppt = get_list(gdf_US, data_dir=data_dir, save_dir=out_dir,
                                                                      state_name=state_name, station_file=None,
                                                                      var_name='ppt')
df_station_tmin, gdf_STATE_tmin, gdf_state_tmin, df_state_tmin = get_list(gdf_US, data_dir=data_dir, save_dir=out_dir,
                                                                          state_name=state_name, station_file=None,
                                                                          var_name='tmin')
df_station_tdmean, gdf_STATE_tdmean, gdf_state_tdmean, df_state_tdmean = get_list(gdf_US, data_dir=data_dir,
                                                                                  save_dir=out_dir,
                                                                                  state_name=state_name,
                                                                                  station_file=None, var_name='tdmean')
df_station_tmax, gdf_STATE_tmax, gdf_state_tmax, df_state_tmax = get_list(gdf_US, data_dir=data_dir,
                                                                          save_dir=out_dir, state_name=state_name,
                                                                          station_file=None, var_name='tmax')
df_station_vpdmin, gdf_STATE_vpdmin, gdf_state_vpdmin, df_state_vpdmin = get_list(gdf_US, data_dir=data_dir,
                                                                                  save_dir=out_dir,
                                                                                  state_name=state_name,
                                                                                  station_file=None, var_name='vpdmin')
df_station_vpdmax, gdf_STATE_vpdmax, gdf_state_vpdmax, df_state_vpdmax = get_list(gdf_US,
                                                                                  data_dir=data_dir, save_dir=out_dir,
                                                                                  state_name=state_name,
                                                                                  station_file=None, var_name='ppt')
fig, ax = plt.subplots(figsize=(12, 8))
gdf_US.plot(ax=ax, facecolor='none', edgecolor='black')
gdf_STATE_ppt.plot(ax=ax, facecolor='none', edgecolor='red')

fig, ax = plt.subplots(figsize=(12, 12))
gdf_STATE_ppt.plot(ax=ax, facecolor='none', edgecolor='black')
gdf_state_ppt.plot(ax=ax, color='green', label='Precipitation')
gdf_state_tmin.plot(ax=ax, color='c', label='Temperature minimum')
gdf_state_tdmean.plot(ax=ax, color='orange',  label='Temperature mean')
gdf_state_tmax.plot(ax=ax, color='red',  label='Temperature maximum')
gdf_state_vpdmin.plot(ax=ax, color='y',  label='VPD minimum')
gdf_state_vpdmax.plot(ax=ax, color='b',  label='VPD maximum')
lines = [
    Line2D([0], [0], linestyle="none", marker="s", markersize=10, markerfacecolor=t.get_facecolor())
    for t in ax.collections[1:]
]
labels = [t.get_label() for t in ax.collections[1:]]
ax.legend(lines, labels)
plt.savefig(os.path.join(out_dir, f'{state_name}_combination.jpg'))
plt.show()

df_state = pd.concat([df_state_ppt, df_state_tmin, df_state_tdmean, df_state_tmax], axis=0)
df_state = df_state.drop_duplicates(subset=['Name',	'Longitude', 'Latitude', 'Elevation(m)'])

gdf_stations = gpd.GeoDataFrame(df_state, geometry=gpd.points_from_xy(df_state.Longitude, df_state.Latitude),
                                crs=f"EPSG:{gdf_US.crs.to_epsg()}")
gdf_stations.to_file(os.path.join(out_dir, f'{state_name}_weather_stations.shp'))
df_state.to_csv(os.path.join(out_dir, f'{state_name}_weather_stations.csv'))

fig, ax = plt.subplots(figsize=(12, 12))
gdf_STATE_ppt.plot(ax=ax, facecolor='none', edgecolor='black')
gdf_stations.plot(ax=ax, color='red')
plt.savefig(os.path.join(out_dir, f'{state_name}_weather_stations.jpg'))
plt.show()

