import geopandas as gpd
import matplotlib.pyplot as plt

shp_file_county = '../../Spatial Analysis/Shapefiles/MS_Counties_2021.shp'
attribute_relate = 'NAMELSAD'
gdf_county = gpd.read_file(shp_file_county)
shp_file_station = 'Spatial_data/Shapefile/Mississippi/Mississippi_weather_stations.shp'
gdf_station = gpd.read_file(shp_file_station)

gdf_station_w_counties = gpd.overlay(gdf_station, gdf_county, how='intersection')
gdf_station_w_counties = gdf_station_w_counties[['Station', 'Name', 'Longitude', 'Latitude', 'Elevation(', 'Network',
                                                 'stnid', 'NAME', 'NAMELSAD', 'ALAND', 'AWATER', 'geometry']]

gdf_station_w_counties.to_file('Spatial_data/Shapefile/Mississippi/Mississippi_weather_stations_wcounties.shp')

fig, ax = plt.subplots(figsize=(12,12))
gdf_county.plot(ax=ax, facecolor='none')
gdf_station_w_counties.plot(ax=ax)

plt.show()