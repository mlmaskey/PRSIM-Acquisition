## Utility functions for spatial analysis
# Author: Mahesh L Maskey, Ph.D. in Hydrologic Sciences
# Date: September 14, 2023
# Affiliations: USDA-ARS, SWMRU, UC Davis, LAWR, Hydrologic Sciences (2012-2019)

import requests
import os
import shutil
import pandas as pd
import geopandas as gpd
from datetime import datetime
from pyproj import Transformer, Proj, CRS
from shapely.geometry import Polygon
from osgeo import gdal  # include imports with the function definition (not where you call it)
from osgeo import osr
from osgeo import ogr
import rasterio
# import rioxarray
# from rioxarray.merge import merge_arrays


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


def copy_individual_rasters(root_dir, list_files, block, show_progress=False):
    out_dir = create_save_folder(root_dir=f'{root_dir}/{block}', sub_dir='Raster')
    if show_progress:
        t0 = datetime.now()
        k = 0
        nfiles = len(list_files)
        print_progress_bar(k, nfiles, prefix='', suffix='', decimals=1, length=50, fill='█')
    for file_path in list_files:
        file = file_path.split('/')[-1]
        file_path_new = os.path.join(out_dir, file)
        shutil.copyfile(file_path, file_path_new)
        if show_progress:
            k = k + 1
            print_progress_bar(k + 1, nfiles, prefix=f'{k}/{nfiles}',
                               suffix=f'{file}: {round((datetime.now() - t0).total_seconds(), 3)} seconds', decimals=1,
                               length=50, fill='█')
        else:
            print(f'Copied {file_path} to {file_path_new}')


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


def trans_lin2ang(crs_from, crs_to, x, y):
    transformer = Transformer.from_crs(crs_from, crs_to)
    x, y = transformer.transform(x, y)
    return x, y


def create_save_folder(root_dir, sub_dir):
    out_dir = os.path.join(root_dir, sub_dir)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    return out_dir


def request_save(url_path, out_dir, is_display=True):
    imfile = url_path.split('/')[-1]
    imfile = imfile[-14:].upper()
    file_path_2save = os.path.join(out_dir, imfile)
    if is_display:
        print(f'Requesting image {url_path}')
    response = requests.get(url_path)
    fp = open(file_path_2save, 'wb')
    if is_display:
        print(f'Saving image {imfile} under {out_dir}')
    fp.write(response.content)
    fp.close()
    if is_display:
        print(f'Saved\n')
    return imfile


def make_url_list(file):
    # Read the list of URL of DEM in the remote server
    file1 = open(file, 'r')
    Lines = file1.readlines()
    file1.close()
    # Get the list of python readable file with full paths in the remote server
    url_lists = []
    for line in Lines:
        url = line.split('\n')[0]
        url_lists.append(url)
    return url_lists


def download_dems(file_im_list, root_dir, sub_dir):
    # file_im_list: Text file containing url of  rasters for certain group
    # root_dir: Main directory where the files to be downloaded
    # sub_dir: Sub directory where the files to be downloaded

    # Get the list of url in python readable format
    url_lists = make_url_list(file_im_list)
    # Create the main and sub-directories if they do not exist
    out_dir = create_save_folder(root_dir, sub_dir)
    # Start downloading
    n_image = len(url_lists)  # Numbers of images to be downloaded
    print(f'Number of files to be downloaded per {file_im_list} is {n_image}.')
    t0 = datetime.now()
    k = 0
    print_progress_bar(k, n_image, prefix='', suffix='', decimals=1, length=50, fill='█')
    for URL in url_lists:
        img_file = request_save(URL, out_dir, is_display=False)
        print_progress_bar(k + 1, n_image, prefix='',
                           suffix=f'{img_file} is saved in {round((datetime.now() - t0).total_seconds(), 3)} seconds',
                           decimals=1, length=50, fill='█')
        k = k + 1
    print('------------------------------------------------------------------------------------------------\n')
    print(f'Completed in {round((datetime.now() - t0).total_seconds, 3)} seconds listed in {file_im_list}')
    print('------------------------------------------------------------------------------------------------\n')


def clip_buffer_shp(gdf, field, offset):
    # Clips the shape file to a specific field and buffer it based on the offset value
    if field is not None:
        field_shp = gdf[gdf.Producer == field]
    else:
        field_shp = gdf
    buffer_shp = field_shp.copy()
    buffer_shp['geometry'] = buffer_shp.geometry.buffer(offset)
    return field_shp, buffer_shp


def read_grid(dir_read, file):
    # Import grid information and relevant database
    shape_file = os.path.join(dir_read, f'{file}.shp')
    df_file = os.path.join(dir_read, f'{file}.csv')
    gdf = gpd.read_file(shape_file, index_col=0)
    df = pd.read_csv(df_file)
    df.columns = ['Tile', 'xLower (dd)', 'yLower (dd)', 'xUpper (dd)', 'yUpper (dd)', 'xLower', 'yLower', 'xUpper',
                  'yUpper', 'File', 'full_path']
    return gdf, df


def read_shape_project(dir_read, file):
    shape_file = os.path.join(dir_read, f'{file}.shp')
    gdf = gpd.read_file(shape_file, index_col=0)
    return gdf


def clip_DataFrame(shp, df_grid):
    # Clips the grid for specific shape file
    x1, y1, x2, y2 = shp.geometry.total_bounds
    print('Extent of buffered shape: ', x1, y1, x2, y2)
    df_farm = df_grid[(df_grid.xLower >= x1) & (df_grid.yLower >= y1) & (df_grid.xUpper <= x2) & (df_grid.yUpper <= y2)]
    print('Grid size', df_farm.shape)
    return df_farm


def clip_grid(df, grid_shp):
    list_tile, file_lists = df.Tile.values, df.full_path.values
    sub_grid = gpd.GeoDataFrame()
    for tile in list_tile:
        gdf_i = grid_shp[grid_shp.Tile == tile]
        sub_grid = pd.concat([sub_grid, gdf_i], axis=0)
    return sub_grid, list_tile, file_lists


# def raster_mosaic(file_lists):
#     src_files_to_mosaic = []
#     t0 = datetime.now()
#     k = 0
#     nfiles = len(file_lists)
#     print_progress_bar(k, nfiles, prefix='', suffix='', decimals=1, length=50, fill='█')
#     for fp in file_lists:
#         # src = rioxarray.open_rasterio(fp)
#         src_files_to_mosaic.append(src)
#         print_progress_bar(k + 1, nfiles, prefix=k + 1,
#                            suffix=f'{round((datetime.now() - t0).total_seconds(), 3)} seconds', decimals=1, length=50,
#                            fill='█')
#         k = k + 1
#     print(f'\nCombined {nfiles} rasters')
#     merged = merge_arrays(src_files_to_mosaic)
#     out_raster = merged.where(merged != merged.rio.nodata)
#     return out_raster


def read_raster(dir_path, imfile):
    imfilepath = os.path.join(dir_path, imfile)
    raster = rasterio.open(imfilepath)
    crs_linear, crs_angular = raster_info(raster)
    return raster, crs_linear, crs_angular


def make_rectangle(x1, y1, x2, y2, crs):
    lat_point_list = [y1, y1, y2, y2, y1]
    lon_point_list = [x1, x2, x2, x1, x1]
    polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
    polygon = gpd.GeoDataFrame(index=[0], crs=f'epsg:{crs}', geometry=[polygon_geom])
    return polygon


