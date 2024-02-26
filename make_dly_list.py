import pandas as pd
import re
import fortranformat as ff

df_stn_list = pd.read_csv('Spatial_data/Shapefile/Mississippi/Mississippi_weather_stations.csv')
file_list = 'Weather_Data/Mississippi/WDLYLIST.DAT'
stn_list = []
f_w = open(file_list, 'w')
f_w.close()
for i in range(df_stn_list.shape[0]):
    f_a = open(file_list, 'a')
    stn = df_stn_list.loc[df_stn_list.index[i], 'Name']
    file = ''.join(re.findall(r'[a-zA-Z]+', stn))
    # if '/' in stn:
    #     file = stn.split('/')
    #     file = file[0] + file[1]
    # else:
    #     file = stn
    file_name = f'{file}.dly'
    Longitude = df_stn_list.loc[df_stn_list.index[i], 'Longitude']
    Latitude = df_stn_list.loc[df_stn_list.index[i], 'Latitude']
    Elevation = df_stn_list.loc[df_stn_list.index[i], 'Elevation(m)']
    stnid = df_stn_list.loc[df_stn_list.index[i], 'stnid']
    network = df_stn_list.loc[df_stn_list.index[i], 'Network']
    comment = f'Station {stnid}: {stn} within {network} network'
    write_format = ff.FortranRecordWriter('(I5, A18, F6.2, F8.2, F8.1, A50)')
    write_line = [i+1, file_name, Latitude, Longitude, Elevation, comment]
    line_write = write_format.write(write_line)
    f_a.writelines(line_write + '\n')
    f_a.close()
    stn_list.append(write_line)

print('complete')



