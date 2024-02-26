#!/bin/bash

#SBATCH --account=swmru_apex
#SBATCH --job-name="PRISM_data_download"
#SBATCH --partition atlas
#SBATCH --ntasks 1
#SBATCH --cpus-per-task=2
#SBATCH --time 20:00:00
##SBATCH --mail-user=emailAddress
##SBATCH --mail-type=BEGIN,END,FAIL

module load miniconda singularity
source activate
conda activate /project/swmru_apex/py_env

python main_download.py --dir2Save=/project/swmru_apex/PRISM/Data --start_year=1981 --end_year=2023 --scale=daily --attribute=tmax