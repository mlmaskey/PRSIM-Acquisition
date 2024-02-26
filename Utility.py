import os
import shutil
import pandas as pd
import zipfile
import geopandas as gpd
import rasterio
import fortranformat as ff
from osgeo import gdal  # include imports with the function definition (not where you call it)
from osgeo import osr
from osgeo import ogr


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            ref: https://gist.github.com/snakers4/91fa21b9dda9d055a02ecd23f24fbc3d
	"""

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def create_save_folder(root_dir, sub_dir):
    out_dir = os.path.join(root_dir, sub_dir)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    return out_dir


def do_zip(file_path, destination):
    with zipfile.ZipFile(file_path) as zf:
        zf.extractall(destination)
    output_file = file_path.split('/')[-1]
    # print(f'{output_file} is unzipped under {destination}')


def get_date_vec(year, scale):
    if scale == 'daily':
        date_vec = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq='D')
        date_vec_str = date_vec.astype(str)
        dates = []
        for d in date_vec_str:
            x = d.split('-')
            dates.append(f'{x[0]}{x[1]}{x[2]}')
    elif scale == 'monthly':
        date_vec = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq='M')
        date_vec_str = date_vec.astype(str)
        dates = []
        for m in date_vec_str:
            x = m.split('-')
            dates.append(f'{x[0]}{x[1]}')
    return dates, date_vec_str


def raster_info(raster):
    """
        Retrieves the authority codes for a compound coordinate system.
        GEOGCS gives you the geographic coordinate system (horizontal/angular: latitude and longitude in degrees).
        VERT_CS gives you the vertical coordinate system (vertical/linear: elevation or depth in linear units like meters or feet).
    """
    # Check the type of raster input
    if isinstance(raster, rasterio.io.DatasetReader):  # you can directly access the crs attribute of the raster dataset
        raster_detail = raster.crs.wkt
        meta = raster.meta
    elif isinstance(raster,
                    gdal.Dataset):  # there is no direct crs attribute. Instead, you retrieve the CRS information using the GetProjection() method.
        raster_detail = raster.GetProjection()
        meta = {
            'driver': raster.GetDriver().ShortName,
            'dtype': gdal.GetDataTypeName(raster.GetRasterBand(1).DataType),
            'nodata': raster.GetRasterBand(1).GetNoDataValue(),
            'width': raster.RasterXSize,
            'height': raster.RasterYSize,
            'count': raster.RasterCount,
            'crs': 'CRS.from_epsg(None)',
            'transform': raster.GetGeoTransform()
        }

    else:
        raise ValueError("Unsupported raster input type.")

    srs = osr.SpatialReference()
    srs.ImportFromWkt(raster_detail)
    crs_angular = srs.GetAuthorityCode("GEOGCS")  # 6318
    crs_linear = srs.GetAuthorityCode("PROJCS")  # 6350
    crs_vertical = srs.GetAuthorityCode("VERT_CS")  # 5703
    meta['crs'] = 'CRS.from_epsg(' + str(srs.GetAuthorityCode(None)) + ')'

    # Outputs (for rasterio case)
    print('Coordinate reference system:', srs.GetAuthorityCode(None))
    print('Linear units:', srs.GetLinearUnitsName())
    print('Meta data:', meta)
    print('Projection:', srs.GetName())
    print('----------------------------------------------------------------------------------------------')
    print('Detail information:', raster_detail)
    print('----------------------------------------------------------------------------------------------')
    print('Linear coordinate reference system:', crs_linear)
    print('Angular coordinate reference system:', crs_angular)

    return crs_linear, crs_angular


def get_station_list(main_path, station_file, var_name, year='1981', ymd='19810101'):
    if station_file is None:
        data_dir = os.path.join(main_path, 'Prism/Variables')
        # sub_dir = os.path.join(data_dir, var_name, year, ymd)
        sub_dir = os.path.join(data_dir, var_name, ymd)
        files = os.listdir(sub_dir)
        csv_file = None
        for file in files:
            if file.endswith('.csv'):
                csv_file = file
                break
        csv_file_path = os.path.join(sub_dir, csv_file)
    else:
        csv_file_path = os.path.join(main_path, station_file)
    try:
        df_stations = pd.read_csv(csv_file_path, index_col=0, skiprows=0)
    except:
        df_stations = pd.read_csv(csv_file_path, index_col=0, skiprows=1)
    df_stations.columns = ['Name', 'Longitude', 'Latitude', 'Elevation(m)', 'Network', 'stnid']
    return csv_file_path, df_stations


def read_bil_file(main_path, var_name, year, ymd, scale):
    data_dir = os.path.join(main_path, 'Prism/Variables')
    sub_dir = os.path.join(data_dir, scale)
    sub_dir = os.path.join(sub_dir, var_name)
    # sub_dir = os.path.join(sub_dir, year)
    sub_dir = os.path.join(sub_dir, ymd)
    files = os.listdir(sub_dir)
    bil_file = None
    for file in files:
        if file.endswith('.bil'):
            bil_file = file
            break
    bil_file_path = os.path.join(sub_dir, bil_file)
    raster = rasterio.open(bil_file_path)
    return raster


def get_lon_lat(df, station):
    df_station = df[df.Name == station]
    lon = df_station.Longitude.values[0]
    lat = df_station.Latitude.values[0]
    return lon, lat


def get_station_list_by_attribute(data_dir, save_dir, station_file, var_name):
    _, df_stations = get_station_list(data_dir, station_file, var_name)
    df_stations.to_csv(os.path.join(save_dir, f'US_Stations_{var_name}.csv'))
    return df_stations


def get_list_by_state(gdf, state_name, df_stations, save_dir, var_name):
    crs = gdf.crs.to_epsg()
    gdf_STATE = gdf[gdf.NAME == state_name]
    shapefile = os.path.join(save_dir, f'{state_name}.shp')
    gdf_STATE.to_file(shapefile)
    x1, y1, x2, y2 = gdf_STATE.geometry.total_bounds
    df_stations_state = df_stations[
        (df_stations.Longitude >= x1) & (df_stations.Longitude <= x2) & (df_stations.Latitude >= y1) & (
                df_stations.Latitude <= y2)]
    gdf_stations = gpd.GeoDataFrame(df_stations_state,
                                    geometry=gpd.points_from_xy(df_stations_state.Longitude,
                                                                df_stations_state.Latitude),
                                    crs=f"EPSG:{crs}")
    gdf_state = gpd.clip(gdf_stations, gdf_STATE, keep_geom_type=False)
    shapefile = os.path.join(save_dir, f'{state_name}_PRISM_{var_name}.shp')
    gdf_state.to_file(shapefile)
    df_state = pd.DataFrame(gdf_state.drop(columns='geometry'))
    df_state.to_csv(os.path.join(save_dir, f'{state_name}_Stations_{var_name}.csv'))
    return gdf_STATE, gdf_state, df_state


def get_list(gdf_US, data_dir, state_name, save_dir, station_file, var_name):
    df_stations = get_station_list_by_attribute(data_dir, save_dir, station_file, var_name)
    gdf_STATE, gdf_station, df_state = get_list_by_state(gdf_US, state_name, df_stations, save_dir, var_name)
    return df_stations, gdf_STATE, gdf_station, df_state


def read_import_data(data_dir, state_name, attribute, year):
    '''
    Reads imported annual time series
    :param data_dir:
    :param state_name:
    :param attribute:
    :param year:
    :return:
    '''
    data_dir = os.path.join(data_dir, state_name)
    file = f'Prism_{attribute}_{year}.csv'
    file_path = os.path.join(data_dir, file)
    df = pd.read_csv(file_path)
    return df


def write_line_ff(df, i):
    yr = int(df.iloc[i, 0])
    mm = int(df.iloc[i, 1])
    dd = int(df.iloc[i, 2])
    tmax = float(df.loc[df.index[i], 'tmax'])
    tmin = float(df.loc[df.index[i], 'tmin'])
    ppt = float(df.loc[df.index[i], 'ppt'])
    dt = str(df.index[i])
    write_format = ff.FortranRecordWriter('(I6, I4, I4, F6.1, F6.1, F6.1, F6.2, F6.1, F6.1, A25)')
    # Check if srad, rhum, and wind are available
    if 'srad' in df.columns:
        sr = float(df.loc[df.index[i], 'srad'])
    else:
        sr = None
        write_format = ff.FortranRecordWriter('(I6, I4, I4, A6, F6.1, F6.1, F6.2, F6.1, F6.1, A25)')
    if 'rhum' in df.columns:
        rhum = float(df.loc[df.index[i], 'rhum'])
    else:
        rhum = None
        write_format = ff.FortranRecordWriter('(I6, I4, I4, F6.1, F6.1, F6.1, F6.2, A6, F6.1, A25)')
    if 'wind' in df.columns:
        ws = float(df.loc[df.index[i], 'wind'])
    else:
        ws = None
        write_format = ff.FortranRecordWriter('(I6, I4, I4, F6.1, F6.1, F6.1, F6.2, F6.1, A6, A25)')

    if (sr is None) & (rhum is None) & (ws is None):
        write_format = ff.FortranRecordWriter('(I6, I4, I4, A6, F6.1, F6.1, F6.2, A6, A6, A25)')
    elif (rhum is None) & (ws is None):
        write_format = ff.FortranRecordWriter('(I6, I4, I4, F6.1, F6.1, F6.1, F6.2, A6, A6, A25)')
    elif (sr is None) & (ws is None):
        write_format = ff.FortranRecordWriter('(I6, I4, I4, A6, F6.1, F6.1, F6.2, F6.1, A6, A25)')
    elif (sr is None) & (rhum is None):
        write_format = ff.FortranRecordWriter('(I6, I4, I4, A6, F6.1, F6.1, F6.2, A6, F6.1, A25)')
    line_write = write_format.write([yr, mm, dd, sr, tmax, tmin, ppt, rhum, ws, dt])
    return line_write


def convert2dly(df, file):
    f_w = open(file, 'w')
    f_w.close()
    for i in range(df.shape[0]):
        f_a = open(file, 'a')
        line_write = write_line_ff(df, i)
        f_a.writelines(line_write + '\n')
        f_a.close()


def create_list_month_files(year):
    month_list = []
    for i in range(1, 13):
        month_list.append(f'{year}{i:02}')
    return month_list


def split_month_folder(root_dir, scale, var_name, year):
    # Detect and create read and save directory
    root_dir = os.path.join(root_dir, 'Prism/Variables')
    sub_dir = os.path.join(root_dir, scale)
    sub_dir1 = os.path.join(sub_dir, var_name)
    sub_dir2 = os.path.join(sub_dir1, str(year))
    files = os.listdir(sub_dir2)
    month_list = create_list_month_files(year)
    for ym in month_list:
        yr_files = []
        for file in files:
            if ym in file:
                yr_files.append(file)
            else:
                continue
        del file
        # Create folder to save split file
        copy_dir = create_save_folder(root_dir=sub_dir1, sub_dir=ym)
        # Copy monthly folder into  the  folder
        for file in yr_files:
            shutil.copyfile(f'{sub_dir2}/{file}', f'{copy_dir}/{file}')
            print(f'Copied {file} into {copy_dir}.')
        del file
    print(f'Done for {year}')

