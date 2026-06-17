import os
import numpy as np
import argparse
import pandas as pd
from Utility import read_import_data
from Utility import create_save_folder
from Utility import print_progress_bar

# python concatenate_data.py --start-year 1981 --end-year 2023 --attribute ppt --state-name Mississippi --data-dir Spatial_data/Shapefile
def concatenate_data(start_year, end_year, state_name, data_dir, attribute):
    year_vec = np.arange(start_year, end_year)

    df = pd.DataFrame()
    m = 0
    print_progress_bar(m, len(year_vec), prefix='', suffix='', decimals=1, length=50, fill='█')
    for year in year_vec:
        df_ppt = read_import_data(data_dir, state_name, attribute, year)
        df = pd.concat([df, df_ppt], axis=1)
        print_progress_bar(m + 1, len(year_vec), prefix=f'{m}', suffix=f'{year}', decimals=1, length=50,
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

    # out_dir = create_save_folder(root_dir=os.getcwd(), sub_dir='Weather_Data')
    if state_name==None:
        out_dir = create_save_folder(root_dir=data_dir, sub_dir='Weather_Data')
        out_file = 'PRISM_station_info.csv'
    else:
        out_dir = create_save_folder(root_dir=os.getcwd(), sub_dir='Weather_Data')
        out_file = f'PRISM_{state_name}_station_info.csv'
    out_file_path = os.path.join(out_dir, out_file)
    df_list.to_csv(out_file_path)
    
    out_file = f'PRISM_{start_year}_{end_year}_daily_{attribute}.csv'
    out_file_path = os.path.join(out_dir, out_file)
    df_attribute.to_csv(out_file_path)
    print(f'\nCompleted importing {attribute} Prism data')
    print('\n------------------------------------------------------------')

import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Concatenate PRISM daily data by state and attribute."
    )

    parser.add_argument("--start-year", type=int, required=True)
    parser.add_argument("--end-year", type=int, required=True)
    parser.add_argument("--state-name", type=str, default=None)
    parser.add_argument("--data-dir", type=str, required=True)

    parser.add_argument("--attribute", type=str, required=True, 
        help="One PRISM attributes: ppt tmin tdmean tmax vpdmin vpdmax"
        )

    args = parser.parse_args()
    # Convert string NONE/None/null to Python None
    if args.state_name is not None:
        if args.state_name.lower() in ["none", "null"]:
            args.state_name = None

    concatenate_data(
        start_year=args.start_year,
        end_year=args.end_year,
        state_name=args.state_name,
        data_dir=args.data_dir,
        attribute=args.attribute
    )


if __name__ == "__main__":
    main()
