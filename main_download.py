"""
    Program: Downloading spatial  weather variable
    Author: Mahesh Lal Maskey, Ph.D. in Hydrologic Sciences
    Affiliations: USDA-ARS, Sustainable Water Management Research Unit, Stoneville/Leland MS
                  University of California, Davis, Department of Land, Air, and Water Resources
    Date: September 25, 2023
    E-mail: mahesh.maskey@usda.gov/mmaskey@ucdavis.edu
"""

import argparse
import os
from pathlib import Path
from Utility import create_save_folder
from downloadPrismBill import download_prism_bill
# Syntax: python main_download --dir2Save='X:/Mahesh.Maskey/Data/Climate' --start_year=1981 --end_year=2023
# --scale=daily --attribute=ppt

parser = argparse.ArgumentParser()
parser.add_argument(
    '--dir2Save', type=str, required=True,
    help='Output location'
)

parser.add_argument(
    '--start_year', type=int, required=True,
    help='Beginning of year to download'
)

parser.add_argument(
    '--end_year', type=int, required=True,
    help='End of year to download'
)

parser.add_argument(
    '--scale', type=str, required=True,
    help='Time scale to download: daily or monthly'
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
output_dir = Path(args.dir2Save)

save_dir = create_save_folder(root_dir=output_dir, sub_dir='Prism')
# save_dir = create_save_folder(root_dir='X:/Mahesh.Maskey/Data/Climate', sub_dir='Prism')
for year in range(start_year, end_year + 1):
    download_prism_bill(scale, var_name, year, dir2save=save_dir)
