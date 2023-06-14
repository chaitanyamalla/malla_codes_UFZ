#!/bin/bash

#SBATCH -J wis-d_indicators
#SBATCH -o ./%x-%j.log
#SBATCH -t 0-5:00:00
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-user=chaitanya.malla@ufz.de
#SBATCH --mail-type=BEGIN,END
#SBATCH --output=./%x-%A-%a.out
#SBATCH --error=./%x-%A-%a.err

# -*- coding: utf-8 -*-

# ml purge # removes all activated modules
# ml Anaconda3 # loads Anaconda
# source activate /global/apps/klimabuero/conda_py3.9.2/

# --------------------------------------------------
#  File:        eval_periods.py
#
#  Created:     Mo 16.08.2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce fldpctl&timmean for global warming degree periods of 1.5,2,3 K for RCP 8.5 METs for saxony
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------

path_int="/work/malla/sachsen_input/"
path_out="/work/malla/sachsen_output/yearly/"


mets=$(seq -f "%03g" 1 2)" "$(seq -f "%03g" 7 10)" "$(seq -f "%03g" 21 31)" "$(seq -f "%03g" 35 37)" "$(seq -f "%03g" 40 41)" "$(seq -f "%03g" 50 58)" "$(seq -f "%03g" 67 78)" "$(seq -f "%03g" 82 87)

#mets=$(seq -f "%03g" 1 2)

cd $path_out



for k in $mets; do
    
    met="met_${k}"
    echo "$met"
    #mkdir $met
    cd $met

    #######-------------yearly-----------#######

    #------pre
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/pre_historic.nc ${path_out}${met}/pre_historic_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/pre_1_5K.nc ${path_out}${met}/pre_1_5K_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/pre_2K.nc ${path_out}${met}/pre_2K_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/pre_3K.nc ${path_out}${met}/pre_3K_ysum_timmean_fldpctl.nc
    #---------------
    #------recharge
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/recharge_historic.nc ${path_out}${met}/recharge_historic_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/recharge_1_5K.nc ${path_out}${met}/recharge_1_5K_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/recharge_2K.nc ${path_out}${met}/recharge_2K_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/recharge_3K.nc ${path_out}${met}/recharge_3K_ysum_timmean_fldpctl.nc
    #---------------
    #-------recharge_adjust
    cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/recharge_adjust_historic.nc ${path_out}${met}/recharge_adjust_historic_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/recharge_adjust_1_5K.nc ${path_out}${met}/recharge_adjust_1_5K_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/recharge_adjust_2K.nc ${path_out}${met}/recharge_adjust_2K_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/recharge_adjust_3K.nc ${path_out}${met}/recharge_adjust_3K_ysum_timmean_fldpctl.nc
    #------------------------
    #-------tmax25--------
    cdo -fldpctl,50 -timmean -yearsum -gtc,25 ${path_int}${met}/tmax_historic.nc ${path_out}${met}/tmax_historic_gtc25_ysum_timmean_fldpctl.nc

    # cdo -fldpctl,50 -timmean -yearsum -gtc,25 ${path_int}${met}/tmax_1_5K.nc ${path_out}${met}/tmax_1_5K_gtc25_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum -gtc,25 ${path_int}${met}/tmax_2K.nc ${path_out}${met}/tmax_2K_gtc25_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum -gtc,25 ${path_int}${met}/tmax_3K.nc ${path_out}${met}/tmax_3K_gtc25_ysum_timmean_fldpctl.nc
     #----------------------
     #-------tmax30--------
    # cdo -fldpctl,50 -timmean -yearsum -gtc,30 ${path_int}${met}/tmax_historic.nc ${path_out}${met}/tmax_historic_gtc30_ysum_timmean_fldpctl.nc

    # cdo -fldpctl,50 -timmean -yearsum -gtc,30 ${path_int}${met}/tmax_1_5K.nc ${path_out}${met}/tmax_1_5K_gtc30_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum -gtc,30 ${path_int}${met}/tmax_2K.nc ${path_out}${met}/tmax_2K_gtc30_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum -gtc,30 ${path_int}${met}/tmax_3K.nc ${path_out}${met}/tmax_3K_gtc30_ysum_timmean_fldpctl.nc
    #-------------------------

    #------aET
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/aET_historic.nc ${path_out}${met}/aET_historic_ysum_timmean_fldpctl.nc

    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/aET_1_5K.nc ${path_out}${met}/aET_1_5K_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/aET_2K.nc ${path_out}${met}/aET_2K_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/aET_3K.nc ${path_out}${met}/aET_3K_ysum_timmean_fldpctl.nc
    #--------------------



    #------pet
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/pet_historic.nc ${path_out}${met}/pet_historic_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/pet_1_5K.nc ${path_out}${met}/pet_1_5K_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/pet_2K.nc ${path_out}${met}/pet_2K_ysum_timmean_fldpctl.nc
    # cdo -fldpctl,50 -timmean -yearsum ${path_int}${met}/pet_3K.nc ${path_out}${met}/pet_3K_ysum_timmean_fldpctl.nc
    #--------------------
    cd ..

done
