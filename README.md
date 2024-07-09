# Python-based Tool to Acquire [PRISM Climate data](https://prism.oregonstate.edu)
## *Extract data from spatial data*
The purpose of this tool is to download and compile daily and monthly weather data from PRISM Climate Data, maintained **[Origon State University](https://prism.oregonstate.edu/)** The PRISM model is *[Parameter-elevation Relationships on Independent Slopes Model](https://prism.oregonstate.edu/documents/pubs/2008intjclim_physiographicMapping_daly.pdf).* 

For daily and monthly weather data, the availavle variables are **Precipitation**, **Minimum temperature**, **Mean temperature**, **Maximum temperature**, **Minimum Vapor Pressure Deficit**, **Maximum Vapor Pressure Deficit**, and **Mean dewpoint temp.**
To download spatialy use [FTP portal](https://ftp.prism.oregonstate.edu). This portal includes spatial data either for each day or each month.

# Python Packages
* os
* pandas
* zipfile
* geopandas
* rasterio
* osgeo - gdal, osr, ogr
* fortran format
  
# Primary Steps
## Download the spatial data 
Spatial data in bill format can be downloaded in daily or monthly scale as follows:
`python main_download --dir2Save='path/to/save_spatial_data' --start_year=START_YEAR --end_year=END_YEAR --scale=SCALE --attribute=VARIABLE`

This script allows the user to download the spatial climate data stored in the **PRISM FTP portal** either in daily or monthly scale. For this the user needs to specify:

`dir2Save`: Path to save the download PRISM spatial data saved under the [FTP portal](https://ftp.prism.oregonstate.edu)

`start_year`: 

