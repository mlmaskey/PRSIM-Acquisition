"""
    Program: Downloading spatial  weather variable
    Author: Mahesh Lal Maskey, Ph.D. in Hydrologic Sciences
    Affiliations: USDA-ARS, Sustainable Water Management Research Unit, Stoneville/Leland MS
                  University of California, Davis, Department of Land, Air, and Water Resources
    Date: September 25, 2023
    E-mail: mahesh.maskey@usda.gov/mmaskey@ucdavis.edu
"""

from datetime import datetime
import os
import shutil
import urllib.request
from Utility import create_save_folder
from Utility import do_zip
from Utility import get_date_vec
from Utility import print_progress_bar


def download_prism_bill(scale, var_name, year, dir2save):
    dir2save_zip = create_save_folder(root_dir=dir2save, sub_dir='Zip_Folder')
    dir2save_zip = create_save_folder(root_dir=dir2save_zip, sub_dir=scale)
    dir2save_zip = create_save_folder(root_dir=dir2save_zip, sub_dir=var_name)
    dir2save_extract = create_save_folder(root_dir=dir2save, sub_dir='Variables')
    dir2save_extract = create_save_folder(root_dir=dir2save_extract, sub_dir=scale)
    dir2save_extract = create_save_folder(root_dir=dir2save_extract, sub_dir=var_name)
    t0 = datetime.now()
    print(f'PRISM {var_name} data is downloading for {year}')
    url_web = 'https://ftp.prism.oregonstate.edu'
    if scale == 'daily':
        date_series = get_date_vec(year, scale)
        n_days = len(date_series)
        k = 0
        print_progress_bar(k, n_days, prefix=f'{k}', suffix='', decimals=1, length=50, fill='█')
        for ymd in date_series:
            try:
                url = f'{url_web}/{scale}/{var_name}/{year}/PRISM_{var_name}_stable_4kmD2_{ymd}_bil.zip '
                req = urllib.request.Request(url)
                output_file = url.split('/')[-1]
                output_filepath = os.path.join(dir2save_zip, output_file)
                with urllib.request.urlopen(req) as response, open(output_filepath, 'wb') as f:
                    shutil.copyfileobj(response, f)
                # print(f'{output_file} is downloaded and saved under {dir2save}')
                # dir2save_extract = create_save_folder(root_dir=dir2save_extract, sub_dir=f'{year}')
                dir2save_extract_ = create_save_folder(root_dir=dir2save_extract, sub_dir=ymd)
                do_zip(file_path=output_filepath, destination=dir2save_extract_)
            except Exception as e:
                print(e)
                print('Date does not exist')
                break
            print_progress_bar(k + 1, n_days, prefix=f'{k + 1}',
                               suffix=f'{ymd} processed in {round((datetime.now() - t0).total_seconds(), 3)} seconds',
                               decimals=1, length=50, fill='█')
            k = k + 1
    elif scale == 'monthly':
        if year < 1981:
            try:
                url = f'{url_web}/{scale}/{var_name}/{year}/PRISM_{var_name}_stable_4kmM2_{year}_all_bil.zip'
                req = urllib.request.Request(url)
                output_file = url.split('/')[-1]
                output_filepath = os.path.join(dir2save_zip, output_file)
                with urllib.request.urlopen(req) as response, open(output_filepath, 'wb') as f:
                    shutil.copyfileobj(response, f)
                dir2save_extract_ = create_save_folder(root_dir=dir2save_extract, sub_dir=str(year))
                do_zip(file_path=output_filepath, destination=dir2save_extract_)
            except:
                url = f'{url_web}/{scale}/{var_name}/{year}/PRISM_{var_name}_stable_4kmM3_{year}_all_bil.zip'
                req = urllib.request.Request(url)
                output_file = url.split('/')[-1]
                output_filepath = os.path.join(dir2save_zip, output_file)
                with urllib.request.urlopen(req) as response, open(output_filepath, 'wb') as f:
                    shutil.copyfileobj(response, f)
                dir2save_extract_ = create_save_folder(root_dir=dir2save_extract, sub_dir=str(year))
                do_zip(file_path=output_filepath, destination=dir2save_extract_)
        else:
            date_series, _ = get_date_vec(year, scale)
            for ym in date_series:
                try:
                    url = f'{url_web}/{scale}/{var_name}/{year}/PRISM_{var_name}_stable_4kmM2_{ym}_bil.zip'
                    req = urllib.request.Request(url)
                    output_file = url.split('/')[-1]
                    output_filepath = os.path.join(dir2save_zip, output_file)
                    with urllib.request.urlopen(req) as response, open(output_filepath, 'wb') as f:
                        shutil.copyfileobj(response, f)
                    dir2save_extract_ = create_save_folder(root_dir=dir2save_extract, sub_dir=ym)
                    do_zip(file_path=output_filepath, destination=dir2save_extract_)
                except:
                    url = f'{url_web}/{scale}/{var_name}/{year}/PRISM_{var_name}_stable_4kmM3_{ym}_bil.zip'
                    req = urllib.request.Request(url)
                    output_file = url.split('/')[-1]
                    output_filepath = os.path.join(dir2save_zip, output_file)
                    with urllib.request.urlopen(req) as response, open(output_filepath, 'wb') as f:
                        shutil.copyfileobj(response, f)
                    dir2save_extract_ = create_save_folder(root_dir=dir2save_extract, sub_dir=ym)
                    do_zip(file_path=output_filepath, destination=dir2save_extract_)
                print(f'{output_file} is downloaded and saved under {dir2save}')
    print(f'\nPRISM  {var_name} data for year {year}  is completed, saved under {dir2save_zip} and  '
          f'unzipped under {dir2save_extract} in {round((datetime.now() - t0).total_seconds(), 3)} seconds\n')
    print('------------------------------------------------------------------------\n')
