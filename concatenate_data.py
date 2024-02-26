import os
import numpy as np
import pandas as pd
from Utility import read_import_data
from Utility import create_save_folder
from Utility import print_progress_bar


def concatenate_data(start_year, end_year, state_name, data_dir, attribute):
    year_vec = np.arange(start_year, end_year)

    df = pd.DataFrame()
    m = 0
    print_progress_bar(m, len(year_vec), prefix='', suffix='', decimals=1, length=50, fill='█')
    for year in year_vec:
        df_ppt = read_import_data(data_dir, state_name, attribute, year)
        df = pd.concat([df, df_ppt], axis=1)
        print_progress_bar(m + 1, len(year_vec), prefix=f'{m / len(year_vec)}', suffix=f'{year}', decimals=1, length=50,
                           fill='█')
        m = m + 1
    print('\nCompleted concatenating')
    df = df.loc[:, ~df.columns.duplicated()].copy()
    df_list = df.iloc[:, 1:6]
    df_list.index = df.Station
    df_list = df_list.drop('stnid', axis=1)
    df_attribute = df.iloc[:, 6:]
    df_attribute.index = df_list.Name
    df_attribute = df_attribute.T

    out_dir = create_save_folder(root_dir=os.getcwd(), sub_dir='Weather_Data')
    out_file = f'PRISM_{state_name}_station_info.csv'
    out_file_path = os.path.join(out_dir, out_file)
    df_list.to_csv(out_file_path)

    out_dir = create_save_folder(out_dir, sub_dir=state_name)
    out_file = f'PRISM_{start_year}_{end_year}_daily_{attribute}.csv'
    out_file_path = os.path.join(out_dir, out_file)
    df_attribute.to_csv(out_file_path)
    print(f'\nCompleted importing {attribute} Prism data')
    print('\n------------------------------------------------------------')


concatenate_data(start_year=1981, end_year=2023, state_name='Mississippi', data_dir='Spatial_data/Shapefile',
                 attribute='ppt')
concatenate_data(start_year=1981, end_year=2023, state_name='Mississippi', data_dir='Spatial_data/Shapefile',
                 attribute='tmin')
concatenate_data(start_year=1981, end_year=2023, state_name='Mississippi', data_dir='Spatial_data/Shapefile',
                 attribute='tdmean')
concatenate_data(start_year=1981, end_year=2023, state_name='Mississippi', data_dir='Spatial_data/Shapefile',
                 attribute='tmax')
concatenate_data(start_year=1981, end_year=2023, state_name='Mississippi', data_dir='Spatial_data/Shapefile',
                 attribute='vpdmin')
concatenate_data(start_year=1981, end_year=2023, state_name='Mississippi', data_dir='Spatial_data/Shapefile',
                 attribute='vpdmax')
