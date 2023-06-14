#!/bin/bash

#SBATCH -J ensembles
#SBATCH -o ./%x-%j.log
#SBATCH -t 0-3:00:00
#SBATCH -c 1
#SBATCH --mem-per-cpu=32G
#SBATCH --mail-user=chaitanya.malla@ufz.de
#SBATCH --mail-type=BEGIN,END
#SBATCH --output=./%x-%A-%a.out
#SBATCH --error=./%x-%A-%a.err

# -*- coding: utf-8 -*-

ml purge # removes all activated modules
ml Anaconda3 # loads Anaconda
source activate /global/apps/klimabuero/conda_py3.9.2/



python /data/hydmet/projects/MA_chaitanya/malla/malla_scripts/thesis_scripts/pre/pre_allMets_monthly_warming_toCSV.py 
# python /data/hydmet/projects/MA_chaitanya/malla/malla_scripts/thesis_scripts/tmax/tmax_25_allMets_monthly_warming_toCSV.py
# python /data/hydmet/projects/MA_chaitanya/malla/malla_scripts/thesis_scripts/tmax/tmax_30_allMets_monthly_warming_toCSV.py
python /data/hydmet/projects/MA_chaitanya/malla/malla_scripts/thesis_scripts//aET_pet/aET_allMets_monthly_warming_toCSV.py 

python /data/hydmet/projects/MA_chaitanya/malla/malla_scripts/thesis_scripts//aET_pet/pet_allMets_monthly_warming_toCSV.py 

python /data/hydmet/projects/MA_chaitanya/malla/malla_scripts/thesis_scripts/recharge/recharge_adjust_allMets_monthly_warming_toCSV.py
