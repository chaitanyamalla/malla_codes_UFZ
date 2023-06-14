#!/bin/bash

#SBATCH -J wis-d_indicators
#SBATCH -o ./%x-%j.log
#SBATCH -t 0-1:00:00
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-user=chaitanya.malla@ufz.de
#SBATCH --mail-type=BEGIN,END
#SBATCH --output=./%x-%A-%a.out
#SBATCH --error=./%x-%A-%a.err

# -*- coding: utf-8 -*-

ml purge # removes all activated modules
ml Anaconda3 # loads Anaconda
source activate /global/apps/klimabuero/conda_py3.9.2/

python /data/hydmet/projects/MA_chaitanya/malla/malla_scripts/thesis_scripts/test.py
