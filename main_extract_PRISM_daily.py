"""
    Program: Extract climate variables from raster deposited in PRISM ftp
    Author: Mahesh Lal Maskey, Ph.D. in Hydrologic Sciences
    Affiliations: USDA-ARS, Sustainable Water Management Research Unit, Stoneville/Leland MS
                  University of California, Davis, Department of Land, Air, and Water Resources
    Date: September 27, 2023
    E-mail: mahesh.maskey@usda.gov/mmaskey@ucdavis.edu
"""
# Syntax: python main_extract_PRISM_daily.py --root_dir='path/to/downloaded_PRISM_data' --start_year=1981
# --end_year=2023 --attribute=ppt --station_file=''/<file.name.csv> ----output_dir='path/to/save_dir' --scale=daily

import argparse
import os
from pathlib import Path
from extract_daily_var import extract_daily_var


parser = argparse.ArgumentParser()
parser.add_argument(
    '--root_dir', type=str, required=True,
    help='Download folder'
)

parser.add_argument(
    '--start_year', type=int, required=True,
    help='Beginning of year to process'
)

parser.add_argument(
    '--end_year', type=int, required=True,
    help='End of year to process'
)

parser.add_argument(
    '--attribute', type=str, required=True,
    help='Parameter to download, e.g., ppt for precipitation, tdmain: mean temperature, tmax: maximum temperature,'
         'tmin: minimum temperature, vpdmax: maximum vapour pressure deficit, vpdmin: minimum vapour presser deficit'
)

parser.add_argument(
    '--station_file', type=str, required=True,
    help='Parameter to download, e.g., ppt for precipitation, tdmain: mean temperature, tmax: maximum temperature,'
         'tmin: minimum temperature, vpdmax: maximum vapour pressure deficit, vpdmin: minimum vapour presser deficit'
)

parser.add_argument(
    '--output_dir', type=str, required=True,
    help='Directory where extracted data is saved. Optional and comes when station_file is given'
)

parser.add_argument(
    '--scale', type=str, required=True,
    help='Directory where extracted data is saved. Optional and comes when station_file is given'
)

args = parser.parse_args()
start_year = int(args.start_year)
end_year = int(args.end_year)
var_name = str(args.attribute)
scale = str(args.scale)
station_file = str(args.station_file)
if station_file == 'None':
    station_file = None
output_dir = str(args.output_dir)
if output_dir == 'None':
    output_dir = None

src_dir = Path(os.path.dirname(os.path.realpath(__file__)))
root_dir = Path(args.root_dir)

for year in range(start_year, end_year + 1):
    extract_daily_var(root_dir, year, var_name, station_file=station_file, output_dir=output_dir, scale=scale)
