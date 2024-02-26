import argparse
import os
from pathlib import Path
from Utility import split_month_folder
# syntax python split_monthly_folders.py --root_dir=X:/Mahesh.Maskey/Data/Climate --start_year=1895
# --end_year=1981 --scale=monthly --attribute=tmax
parser = argparse.ArgumentParser()
parser.add_argument(
    '--root_dir', type=str, required=True,
    help='Location of data folder'
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
    '--scale', type=str, required=True,
    help='Scale to split folder'
)

parser.add_argument(
    '--attribute', type=str, required=True,
    help='Parameter to download, e.g., ppt for precipitation, tdmain: mean temperature, tmax: maximum temperature,'
         'tmin: minimum temperature, vpdmax: maximum vapour pressure deficit, vpdmin: minimum vapour presser deficit'
)

args = parser.parse_args()
start_year = int(args.start_year)
end_year = int(args.end_year)
scale = str(args.scale)
var_name = str(args.attribute)
src_dir = Path(os.path.dirname(os.path.realpath(__file__)))
root_dir = Path(args.root_dir)

for year in range(start_year, end_year):
    split_month_folder(root_dir, scale, var_name, year)
