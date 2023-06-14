#!/bin/bash

#SBATCH -J wis-d_indicators
#SBATCH -o ./%x-%j.log
#SBATCH -t 1-24:00:00
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-user=chaitanya.malla@ufz.de
#SBATCH --mail-type=BEGIN,END
#SBATCH --output=./%x-%A-%a.out
#SBATCH --error=./%x-%A-%a.err

# -*- coding: utf-8 -*-

ml purge # removes all activated modules
ml Anaconda3 # loads Anaconda
source activate /global/apps/klimabuero/conda_py3.9.2/

# --------------------------------------------------
#  File:        plot_data.py
#
#  Created:     Di 20.07.2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce indicators with different timeperiods  for all METs for Germany
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------


set -x
set -e

path_int="/data/hicam/data/processed/meteo/germany/climproj/euro-cordex/88realizations_mhm/"
path_out="/work/malla/meteo_germany/data_output/"
path_rech="/data/hicam/data/processed/wis_d/climproj/recharge_adjust/"
maskfile="/data/hicam/data/processed/dem_OR/mask_hicam_1km_g_inv.nc"


#met_START=1
#met_END=1
mets=$(seq -f "%03g" 1 4)" "$(seq -f "%03g" 7 15)" "$(seq -f "%03g" 21 32)" "$(seq -f "%03g" 35 45)" "$(seq -f "%03g" 50 62)" "$(seq -f "%03g" 67 80)" "$(seq -f "%03g" 82 88)

cd $path_out


#for k in $(seq -f "%03g" $met_START $met_END); do
for t in $mets;do
    met="met_${t}"
    echo "$met"
    	
    

    #mkdir $met

    cd $met

    
    # #PERIOD_start=("1971" "2070")
    # #PERIOD_end=("2000" "2099")
    # PERIOD_start=("2021" "2036")
    # PERIOD_end=("2050" "2065")
    # #PERIOD_start=("1971")
    # #PERIOD_end=("2000")
    # i=0
    # for p_start in "${PERIOD_start[@]}"; do
    #     p_end="${PERIOD_end[$i]}"
    #     echo "evaluate period ${p_start} - ${p_end}"
    #     i=$(($i + 1))

    # 	###-------pre_winter--------###
    # 	cdo -timmean -yearsum -selseason,ndjfma -selyear,$p_start/$p_end ${path_int}${met}/pre.nc ${path_out}${met}/tmp1_pre_winter.nc
    # 	maskfile="/data/hicam/data/processed/dem_OR/mask_hicam_1km_g_inv.nc"
    # 	cdo -O merge ${path_out}${met}/tmp1_pre_winter.nc ${maskfile} ${path_out}${met}/tmp2_pre_winter.nc
    # 	cdo_expr="pre=(mask==0)?-9999:pre" 
    #     cdo expr,$cdo_expr ${path_out}${met}/tmp2_pre_winter.nc ${path_out}${met}/tmp3_pre_winter.nc
    # 	cdo fldpctl,50 ${path_out}${met}/tmp3_pre_winter.nc ${path_out}${met}/pre_winter_${p_start}_${p_end}_ysum_timmean_fldpctl.nc


    # 	###-------pre_summer--------###
    # 	cdo -timmean -yearsum -selseason,mjjaso -selyear,$p_start/$p_end ${path_int}${met}/pre.nc ${path_out}${met}/tmp1_pre_summer.nc
    # 	maskfile="/data/hicam/data/processed/dem_OR/mask_hicam_1km_g_inv.nc"
    # 	cdo -O merge ${path_out}${met}/tmp1_pre_summer.nc ${maskfile} ${path_out}${met}/tmp2_pre_summer.nc
    # 	cdo_expr="pre=(mask==0)?-9999:pre" 
    #     cdo expr,$cdo_expr ${path_out}${met}/tmp2_pre_summer.nc ${path_out}${met}/tmp3_pre_summer.nc
    # 	cdo fldpctl,50 ${path_out}${met}/tmp3_pre_summer.nc ${path_out}${met}/pre_summer_${p_start}_${p_end}_ysum_timmean_fldpctl.nc

    # 	###-------pre_yearly--------###
    # 	cdo -timmean -yearsum -selyear,$p_start/$p_end ${path_int}${met}/pre.nc ${path_out}${met}/tmp1_pre_yearly.nc
    # 	maskfile="/data/hicam/data/processed/dem_OR/mask_hicam_1km_g_inv.nc"
    # 	cdo -O merge ${path_out}${met}/tmp1_pre_yearly.nc ${maskfile} ${path_out}${met}/tmp2_pre_yearly.nc
    # 	cdo_expr="pre=(mask==0)?-9999:pre" 
    #     cdo expr,$cdo_expr ${path_out}${met}/tmp2_pre_yearly.nc ${path_out}${met}/tmp3_pre_yearly.nc
    # 	cdo fldpctl,50 ${path_out}${met}/tmp3_pre_yearly.nc ${path_out}${met}/pre_yearly_${p_start}_${p_end}_ysum_timmean_fldpctl.nc


    # 	###-------tmax 25--------###
    # 	cdo -timmean -yearsum -gtc,25 -selyear,$p_start/$p_end ${path_int}${met}/tmax.nc ${path_out}${met}/tmp1_tmax25.nc
    # 	maskfile="/data/hicam/data/processed/dem_OR/mask_hicam_1km_g_inv.nc"
    # 	cdo -O merge ${path_out}${met}/tmp1_tmax25.nc ${maskfile} ${path_out}${met}/tmp2_tmax25.nc
    # 	cdo_expr_tmax="tmax=(mask==0)?-9999:tmax" 
    #     cdo expr,$cdo_expr_tmax ${path_out}${met}/tmp2_tmax25.nc ${path_out}${met}/tmp3_tmax25.nc
    # 	cdo fldpctl,50 ${path_out}${met}/tmp3_tmax25.nc ${path_out}${met}/tmax25_${p_start}_${p_end}_ysum_timmean_fldpctl.nc


    # 	###-------tmax 30--------###
    # 	cdo -timmean -yearsum -gtc,30 -selyear,$p_start/$p_end ${path_int}${met}/tmax.nc ${path_out}${met}/tmp1_tmax30.nc
    # 	maskfile="/data/hicam/data/processed/dem_OR/mask_hicam_1km_g_inv.nc"
    # 	cdo -O merge ${path_out}${met}/tmp1_tmax30.nc ${maskfile} ${path_out}${met}/tmp2_tmax30.nc
    # 	cdo_expr_tmax="tmax=(mask==0)?-9999:tmax" 
    #     cdo expr,$cdo_expr_tmax ${path_out}${met}/tmp2_tmax30.nc ${path_out}${met}/tmp3_tmax30.nc
    # 	cdo fldpctl,50 ${path_out}${met}/tmp3_tmax30.nc ${path_out}${met}/tmax30_${p_start}_${p_end}_ysum_timmean_fldpctl.nc


    # 	# ###-----recharge_adjust-----###
    # 	cdo -timmean -yearsum -selyear,$p_start/$p_end ${path_rech}recharge_adjust_${met}.nc ${path_out}${met}/tmp1_recharge_adjust.nc
    # 	maskfile="/data/hicam/data/processed/dem_OR/mask_hicam_1km_g_inv.nc"
    # 	cdo -O merge ${path_out}${met}/tmp1_recharge_adjust.nc ${maskfile} ${path_out}${met}/tmp2_recharge_adjust.nc
    # 	cdo_expr_rech="recharge=(mask==0)?-9999:recharge"
    # 	cdo expr,$cdo_expr_rech ${path_out}${met}/tmp2_recharge_adjust.nc ${path_out}${met}/tmp3_recharge_adjust.nc
    # 	cdo fldpctl,50 ${path_out}${met}/tmp3_recharge_adjust.nc ${path_out}${met}/recharge_adjust_${p_start}_${p_end}_ysum_timmean_fldpctl.nc

	
    rm -f tmp*


    #done
    cd ..	
done





