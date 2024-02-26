"""
    Program: Extract climate variables from raster deposited in PRISM ftp
    Author: Mahesh Lal Maskey, Ph.D. in Hydrologic Sciences
    Affiliations: USDA-ARS, Sustainable Water Management Research Unit, Stoneville/Leland MS
                  University of California, Davis, Department of Land, Air, and Water Resources
    Date: September 27, 2023
    E-mail: mahesh.maskey@usda.gov/mmaskey@ucdavis.edu
"""

import pandas as pd
import os
from pyproj import Transformer
from datetime import datetime
from Utility import get_station_list
from Utility import read_bil_file
from Utility import get_date_vec
from Utility import print_progress_bar
from Utility import get_lon_lat
from Utility import create_save_folder


def extract_daily_var(root_dir, year, var_name, station_file=None, output_dir=None, scale='daily'):
    """
    Extract daily attribute value based on the coordinates listed in `station_file`
    :param output_dir: Directory where extracted data is saved. Optional and comes when station_file is given
    :param root_dir: Directory where the Prism data were downloaded
    :param year: Year for which variables to be extracted
    :param var_name: Variable of choice:
                ppt: precipitation,
                tdmean: mean temperature,
                tmax: maximum temperature,
                tmin: minimum temperature,
                vpdmax: maximum vapour pressure deficit,
                vpdmin: minimum vapour presser deficit'
    :param station_file: Optional. If specify, use user defined file with list of stations
    :return: Saves daily values of attribute chosen ove a year
    """
    # Get list of station based on the hard coded year
    csv_file, df_stations = get_station_list(main_path=root_dir, station_file=station_file, var_name=var_name)
    station_list = df_stations.Name.values
    # Define  dataframe with geographic information
    df_day = df_stations[['stnid', 'Name', 'Longitude', 'Latitude', 'Elevation(m)']]
    # Define where to save extracted data and define file name
    if output_dir is None:
        output_dir = create_save_folder(root_dir, f'Prism/Variables/{var_name}')
    output_file = os.path.join(output_dir, f'Prism_{var_name}_{year}.csv')
    # Get series of date formatted in PRISM repository
    num_dates, date_vec = get_date_vec(year, scale)
    # number of days in a year and stations
    n_days, n_stations = len(date_vec), len(station_list)
    total_loops = n_stations * n_days
    t0 = datetime.now()
    m = 0
    print('-------------------------------------------------------------------------------')
    print_progress_bar(m, total_loops, prefix='', suffix='', decimals=1, length=100, fill='█')
    for k in range(n_days):
        raster_data = read_bil_file(main_path=root_dir, var_name=var_name, year=str(year),
                                    ymd=num_dates[k], scale=scale)
        # raster_info(raster_data)
        # show(raster_data)
        # convert coordinate to raster projection
        transformer = Transformer.from_crs("EPSG:4326", raster_data.crs, always_xy=True)
        lat_list, lon_list, value_list = [], [], []
        for stn in station_list:
            lon, lat = get_lon_lat(df=df_stations, station=stn)
            lon_list.append(lon)
            lat_list.append(lat)
            xx, yy = transformer.transform(lon, lat)
            # get value from grid
            value = list(raster_data.sample([(xx, yy)]))[0]
            value_list.append(value[0])
            # print(f'{date_vec[k]} ppt for {stn}: {value[0]}')
            print_progress_bar(m+1, total_loops, prefix=f'{m}/{total_loops}',
                               suffix= f'{round((datetime.now() - t0).total_seconds(), 3)} '
                                       f'seconds ({date_vec[k]}, {stn})', decimals=1, length=100, fill='█')
            m +=1
            # print_progress_bar(m, total_loops, prefix=f'{m}/{total_loops}',
            #                    suffix=f'For {stn}: {date_vec[k]} took  '
            #                           f'{round((datetime.now() - t0).total_seconds(), 3)} seconds',
            #                    decimals=1, length=100, fill='█')
        print('-------------------------------------------------------------------------------')
        df_day_values = pd.DataFrame({f'{date_vec[k]}': value_list}, index=df_day.index)
        df_day = pd.concat([df_day, df_day_values], axis=1)
    df_day.to_csv(output_file)
    print(f'Extraction of {var_name} for {year} is completed and saved in {output_file}')
    print('-------------------------------------------------------------------------------')