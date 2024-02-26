import os

import re
import pandas as pd
from Utility import create_save_folder
from Utility import convert2dly
from Utility import print_progress_bar
from datetime import datetime

# Read weather file imported
df_ppt = pd.read_csv('Weather_Data/Mississippi/PRISM_1981_2023_daily_ppt.csv', index_col=0)
df_ppt.index = pd.to_datetime(df_ppt.index)
df_tmin = pd.read_csv('Weather_Data/Mississippi/PRISM_1981_2023_daily_tmin.csv', index_col=0)
df_tmin.index = pd.to_datetime(df_tmin.index)
df_tdmean = pd.read_csv('Weather_Data/Mississippi/PRISM_1981_2023_daily_tdmean.csv', index_col=0)
df_tdmean.index = pd.to_datetime(df_tdmean.index)
df_tmax = pd.read_csv('Weather_Data/Mississippi/PRISM_1981_2023_daily_tmax.csv', index_col=0)
df_tmax.index = pd.to_datetime(df_tmax.index)
df_vpdmin = pd.read_csv('Weather_Data/Mississippi/PRISM_1981_2023_daily_vpdmin.csv', index_col=0)
df_vpdmin.index = pd.to_datetime(df_vpdmin.index)
df_vpdmax = pd.read_csv('Weather_Data/Mississippi/PRISM_1981_2023_daily_vpdmax.csv', index_col=0)
df_vpdmax.index = pd.to_datetime(df_vpdmax.index)
out_dir = create_save_folder('Weather_Data/Mississippi', 'Station')
stn_list = df_ppt.columns
t0 = datetime.now()
n_stn = len(stn_list)
m = 0
print_progress_bar(m, n_stn, prefix='', suffix='', decimals=1, length=50, fill='█')
# Build station wise longer form data
for stn in stn_list:
    file = ''.join(re.findall(r'[a-zA-Z]+', stn))
    # if '/' in stn:
    #     file = stn.split('/')
    #     file = file[0] + file[1]
    # else:
    #     file = stn
    df = pd.DataFrame({'ppt': df_ppt[stn].values, 'tmin': df_tmin[stn].values, 'tdmean': df_tdmean[stn].values,
                       'tmax': df_tmax[stn].values, 'vpdmin': df_vpdmin[stn].values, 'vpdmax': df_vpdmax[stn].values},
                      index=df_ppt.index)
    df.insert(0, 'Year', df.index.year)
    df.insert(1, 'Month', df.index.month)
    df.insert(2, 'Day', df.index.day)
    df.to_csv(os.path.join(out_dir, f'{file}.csv'))
    # convert weather file into fortran format
    ff_file = os.path.join(out_dir, f'{file}.dly')
    convert2dly(df, ff_file)
    m = m + 1
    print_progress_bar(m, n_stn, prefix=f'{m}/{n_stn}',
                       suffix=f'{stn} in {round((datetime.now() - t0).total_seconds(), 3)} seconds ', decimals=1,
                       length=50, fill='█')
