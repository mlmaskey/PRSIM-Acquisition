# Python-based Tool to Acquire [PRISM Climate data](https://prism.oregonstate.edu)
## *Extract data from spatial data*
The purpose of this tool is to download and compile daily and monthly weather data from PRISM Climate Data, maintained **[Origon State University](https://prism.oregonstate.edu/)** The PRISM model is *[Parameter-elevation Relationships on Independent Slopes Model](https://prism.oregonstate.edu/documents/pubs/2008intjclim_physiographicMapping_daly.pdf).* 

For daily and monthly weather data, the availavle variables are **Precipitation**, **Minimum temperature**, **Mean temperature**, **Maximum temperature**, **Minimum Vapor Pressure Deficit**, **Maximum Vapor Pressure Deficit**, and **Mean dewpoint temp.**
To download spatialy use [FTP portal](https://ftp.prism.oregonstate.edu). This portal includes spatial data either for each day or each month.

# Python Packages
* os
* pathlib
* pandas
* zipfile
* geopandas
* rasterio
* osgeo - gdal, osr, ogr
* fortran format
  
# Primary Steps
## Step 1: Download the spatial data 
Spatial data in bill format can be downloaded in daily or monthly scale as follows:

`python main_download.py --dir2Save='path/to/save_spatial_data' --start_year=START_YEAR --end_year=END_YEAR --scale=SCALE --attribute=VARIABLE`

This script allows the user to download the spatial climate data stored in the **PRISM FTP portal** either in daily or monthly scale. For this the user needs to specify:

`dir2Save`: Path to save the download PRISM spatial data saved under the [FTP portal](https://ftp.prism.oregonstate.edu) (string)

`start_year`: Begining of the year to download the data (integer)

`end_year`: End of the year to download the data  (integer)

`scale`: Temporal scale, monnthly or daily  (string)

 `attribute`: The weather variable to download the data, including  `ppt` for *precipitation*, `tmax` for *minimum temperature*, `tmean` for *mean temperature*, `tmax` for *maximum temperature*, `vpdmin` for *minimum Vapor pressure deficit*, and `vpdmax for *maximum vapor pressure deficit*, and `tdmean` for *mean dewpoint temperature*

 ## Step 2: Extract daily PRISM data
 
  `python main_extract_PRISM_daily.py --root_dir='path/to/downloaded_prism_data' --start_year=YEAR --end_year=YEAR --attribute=VARIABLE --station_file='STATION LIST FILE --output_dir=path/to/data_dir --scale=SCALE`
  
  Pror to this, the user needs to prepare a list of station in a csv file the includes in the following order:
  
  * `Station,`
  * `Name,`
  * `Longitude,`
  *  `Latitude,`
  *  `Elevation(m) [optional],`
  *  `Network [optional],` and
  *  `stnid [optional],`



