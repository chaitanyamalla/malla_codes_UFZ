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

ml purge # removes all activated modules
ml Anaconda3 # loads Anaconda
source activate /global/apps/klimabuero/conda_py3.9.2/

# --------------------------------------------------
#  File:        warmingdegree_periods.py
#
#  Created:     Do 05.08.2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce indicators with different timeperiods which resembles global warming degree periods of 1.5,2,3,4 K for RCP 8.5 METs for saxony
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------

path_int="/data/hydmet/projects/MA_chaitanya/data_climproj/"
#path_out="/data/hydmet/projects/MA_chaitanya/data_climproj/"
path_out="/work/malla/sachsen_input/"

mets=$(seq -f "%03g" 1 2)" "$(seq -f "%03g" 7 10)" "$(seq -f "%03g" 21 31)" "$(seq -f "%03g" 35 37)" "$(seq -f "%03g" 40 41)" "$(seq -f "%03g" 50 58)" "$(seq -f "%03g" 67 78)" "$(seq -f "%03g" 82 87)

cd $path_int

# #--------------historic-------------------------------------------
# for k in $mets; do
#     echo $k
#     met="met_${k}"
#     echo "$met"
#     cd $met
#     p_start="1971"
#     p_end="2000"
#     echo "${p_start}_${p_end}"
#     w_level="historic"
    
   
#     cdo selyear,$p_start/$p_end ${path_int}${met}/pre_SN.nc ${path_out}${met}/pre_${w_level}.nc
#     cdo selyear,$p_start/$p_end ${path_int}${met}/tmax_SN.nc ${path_out}${met}/tmax_${w_level}.nc
#     cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_SN.nc ${path_out}${met}/recharge_${w_level}.nc
#     cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_adjust_SN.nc ${path_out}${met}/recharge_adjust_${w_level}.nc
#     cdo selyear,$p_start/$p_end ${path_int}${met}/pet_SN.nc ${path_out}${met}/pet_${w_level}.nc
#     cdo selyear,$p_start/$p_end ${path_int}${met}/aET_SN.nc ${path_out}${met}/aET_${w_level}.nc
#     cd ..
# done
# #~~~~~~CanESM2~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# for k in $(seq -f "%03g" 1 2); do
#     met="met_${k}"
#     echo "$met"
#     cd $met
#     PERIOD_start=("2001" "2014" "2036" "2055")
#     PERIOD_end=("2030" "2043" "2065" "2084")
#     warm=("1_5K" "2K" "3K" "4K")
#     i=0
#     for p_start in "${PERIOD_start[@]}"; do
#         p_end="${PERIOD_end[$i]}"
# 	w_level="${warm[$i]}"
#         echo "evaluate period ${p_start} - ${p_end} and global warming level ${w_level}"
#         i=$(($i + 1))

	# cdo selyear,$p_start/$p_end ${path_int}${met}/pre_SN.nc ${path_int}${met}/pre_${w_level}.nc
	# cdo selyear,$p_start/$p_end ${path_int}${met}/tmax_SN.nc ${path_int}${met}/tmax_${w_level}.nc
	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_SN.nc ${path_int}${met}/recharge_${w_level}.nc
	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_adjust_SN.nc ${path_int}${met}/recharge_adjust_${w_level}.nc
	# cdo selyear,$p_start/$p_end ${path_int}${met}/pet_SN.nc ${path_int}${met}/pet_${w_level}.nc
    # 	cdo selyear,$p_start/$p_end ${path_int}${met}/aET_SN.nc ${path_int}${met}/aET_${w_level}.nc
    # done
    # cd ..
    
    
# done
# #........................


# #~~~~~~~~CNRM-CM5~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# for k in $(seq -f "%03g" 7 10); do
#     met="met_${k}"
#     echo "$met"
#     cd $met
#     PERIOD_start=("2014" "2029" "2052")
#     PERIOD_end=("2043" "2058" "2081")
#     warm=("1_5K" "2K" "3K")
#     i=0
#     for p_start in "${PERIOD_start[@]}"; do
#         p_end="${PERIOD_end[$i]}"
# 	w_level="${warm[$i]}"
#         echo "evaluate period ${p_start} - ${p_end} and global warming level ${w_level}"
#         i=$(($i + 1))
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pre_SN.nc ${path_int}${met}/pre_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/tmax_SN.nc ${path_int}${met}/tmax_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_SN.nc ${path_int}${met}/recharge_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_adjust_SN.nc ${path_int}${met}/recharge_adjust_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pet_SN.nc ${path_int}${met}/pet_${w_level}.nc
# 	cdo selyear,$p_start/$p_end ${path_int}${met}/aET_SN.nc ${path_int}${met}/aET_${w_level}.nc
#     done
#     cd ..
    
    
# done
# #.........................



# ############################################################################
# #..........................................................................
# #                          EC-EARTH
# #...........................................................................


# for k in $(seq -f "%03g" 21 25); do
#     met="met_${k}"
#     echo "$met"
#     cd $met
#     PERIOD_start=("2011" "2026" "2051")
#     PERIOD_end=("2040" "2055" "2080")
#     warm=("1_5K" "2K" "3K")
#     i=0
#     for p_start in "${PERIOD_start[@]}"; do
#         p_end="${PERIOD_end[$i]}"
# 	w_level="${warm[$i]}"
#         echo "evaluate period ${p_start} - ${p_end} and global warming level ${w_level}"
#         i=$(($i + 1))
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pre_SN.nc ${path_int}${met}/pre_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/tmax_SN.nc ${path_int}${met}/tmax_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_SN.nc ${path_int}${met}/recharge_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_adjust_SN.nc ${path_int}${met}/recharge_adjust_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pet_SN.nc ${path_int}${met}/pet_${w_level}.nc
# 	cdo selyear,$p_start/$p_end ${path_int}${met}/aET_SN.nc ${path_int}${met}/aET_${w_level}.nc
#     done
#     cd ..
    
    
# done

# for k in $(seq -f "%03g" 26 28); do
#     met="met_${k}"
#     echo "$met"
#     cd $met
#     PERIOD_start=("2012" "2028" "2052")
#     PERIOD_end=("2041" "2057" "2081")
#     warm=("1_5K" "2K" "3K")
#     i=0
#     for p_start in "${PERIOD_start[@]}"; do
#         p_end="${PERIOD_end[$i]}"
# 	w_level="${warm[$i]}"
#         echo "evaluate period ${p_start} - ${p_end} and global warming level ${w_level}"
#         i=$(($i + 1))
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pre_SN.nc ${path_int}${met}/pre_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/tmax_SN.nc ${path_int}${met}/tmax_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_SN.nc ${path_int}${met}/recharge_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_adjust_SN.nc ${path_int}${met}/recharge_adjust_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pet_SN.nc ${path_int}${met}/pet_${w_level}.nc
# 	cdo selyear,$p_start/$p_end ${path_int}${met}/aET_SN.nc ${path_int}${met}/aET_${w_level}.nc
#     done
#     cd ..
    
    
# done

# for k in $(seq -f "%03g" 29 31); do
#     met="met_${k}"
#     echo "$met"
#     cd $met
#     PERIOD_start=("2014" "2029" "2051")
#     PERIOD_end=("2043" "2058" "2080")
#     warm=("1_5K" "2K" "3K")
#     i=0
#     for p_start in "${PERIOD_start[@]}"; do
#         p_end="${PERIOD_end[$i]}"
# 	w_level="${warm[$i]}"
#         echo "evaluate period ${p_start} - ${p_end} and global warming level ${w_level}"
#         i=$(($i + 1))
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pre_SN.nc ${path_int}${met}/pre_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/tmax_SN.nc ${path_int}${met}/tmax_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_SN.nc ${path_int}${met}/recharge_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_adjust_SN.nc ${path_int}${met}/recharge_adjust_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pet_SN.nc ${path_int}${met}/pet_${w_level}.nc
# 	cdo selyear,$p_start/$p_end ${path_int}${met}/aET_SN.nc ${path_int}${met}/aET_${w_level}.nc
#     done
#     cd ..
    
    
# done
# #..............................................................................................







# #~~~~~~~~IPSL-CM5A-MR~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# for k in $(seq -f "%03g" 35 37); do
#     met="met_${k}"
#     echo "$met"
#     cd $met
#     PERIOD_start=("2007" "2020" "2039" "2056")
#     PERIOD_end=("2036" "2049" "2068" "2085")
#     warm=("1_5K" "2K" "3K" "4K")
#     i=0
#     for p_start in "${PERIOD_start[@]}"; do
#         p_end="${PERIOD_end[$i]}"
# 	w_level="${warm[$i]}"
#         echo "evaluate period ${p_start} - ${p_end} and global warming level ${w_level}"
#         i=$(($i + 1))
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pre_SN.nc ${path_int}${met}/pre_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/tmax_SN.nc ${path_int}${met}/tmax_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_SN.nc ${path_int}${met}/recharge_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_adjust_SN.nc ${path_int}${met}/recharge_adjust_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pet_SN.nc ${path_int}${met}/pet_${w_level}.nc
# 	cdo selyear,$p_start/$p_end ${path_int}${met}/aET_SN.nc ${path_int}${met}/aET_${w_level}.nc
#     done
#     cd ..
    
    
# done
# #.........................



# #~~~~~~~~MIROC5~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# for k in $(seq -f "%03g" 40 41); do
#     met="met_${k}"
#     echo "$met"
#     cd $met
#     PERIOD_start=("2012" "2028" "2052")
#     PERIOD_end=("2041" "2057" "2081")
#     warm=("1_5K" "2K" "3K")
#     i=0
#     for p_start in "${PERIOD_start[@]}"; do
#         p_end="${PERIOD_end[$i]}"
# 	w_level="${warm[$i]}"
#         echo "evaluate period ${p_start} - ${p_end} and global warming level ${w_level}"
#         i=$(($i + 1))
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pre_SN.nc ${path_int}${met}/pre_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/tmax_SN.nc ${path_int}${met}/tmax_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_SN.nc ${path_int}${met}/recharge_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_adjust_SN.nc ${path_int}${met}/recharge_adjust_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pet_SN.nc ${path_int}${met}/pet_${w_level}.nc
# 	cdo selyear,$p_start/$p_end ${path_int}${met}/aET_SN.nc ${path_int}${met}/aET_${w_level}.nc
#     done
#     cd ..
    
    
# done
# #.........................


# #~~~~~~~~HadGEM2-ES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# for k in $(seq -f "%03g" 50 58); do
#     met="met_${k}"
#     echo "$met"
#     cd $met
#     PERIOD_start=("2004" "2016" "2037" "2054")
#     PERIOD_end=("2033" "2045" "2066" "2083")
#     warm=("1_5K" "2K" "3K" "4K")
#     i=0
#     for p_start in "${PERIOD_start[@]}"; do
#         p_end="${PERIOD_end[$i]}"
# 	w_level="${warm[$i]}"
#         echo "evaluate period ${p_start} - ${p_end} and global warming level ${w_level}"
#         i=$(($i + 1))
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pre_SN.nc ${path_int}${met}/pre_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/tmax_SN.nc ${path_int}${met}/tmax_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_SN.nc ${path_int}${met}/recharge_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_adjust_SN.nc ${path_int}${met}/recharge_adjust_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pet_SN.nc ${path_int}${met}/pet_${w_level}.nc
# 	cdo selyear,$p_start/$p_end ${path_int}${met}/aET_SN.nc ${path_int}${met}/aET_${w_level}.nc
#     done
#     cd ..
    
    
# done
# #.........................




# ############################################################################
# #..........................................................................

# #                        MPI-ESM-LR
  
# #...........................................................................
# for k in $(seq -f "%03g" 67 73); do
#     met="met_${k}"
#     echo "$met"
#     cd $met
#     PERIOD_start=("2013" "2029" "2052")
#     PERIOD_end=("2042" "2058" "2081")
#     warm=("1_5K" "2K" "3K")
#     i=0
#     for p_start in "${PERIOD_start[@]}"; do
#         p_end="${PERIOD_end[$i]}"
# 	w_level="${warm[$i]}"
#         echo "evaluate period ${p_start} - ${p_end} and global warming level ${w_level}"
#         i=$(($i + 1))
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pre_SN.nc ${path_int}${met}/pre_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/tmax_SN.nc ${path_int}${met}/tmax_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_SN.nc ${path_int}${met}/recharge_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_adjust_SN.nc ${path_int}${met}/recharge_adjust_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pet_SN.nc ${path_int}${met}/pet_${w_level}.nc
# 	cdo selyear,$p_start/$p_end ${path_int}${met}/aET_SN.nc ${path_int}${met}/aET_${w_level}.nc
#     done
#     cd ..
    
    
# done

# for k in $(seq -f "%03g" 74 76); do
#     met="met_${k}"
#     echo "$met"
#     cd $met
#     PERIOD_start=("2011" "2026" "2050")
#     PERIOD_end=("2040" "2055" "2079")
#     warm=("1_5K" "2K" "3K")
#     i=0
#     for p_start in "${PERIOD_start[@]}"; do
#         p_end="${PERIOD_end[$i]}"
# 	w_level="${warm[$i]}"
#         echo "evaluate period ${p_start} - ${p_end} and global warming level ${w_level}"
#         i=$(($i + 1))
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pre_SN.nc ${path_int}${met}/pre_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/tmax_SN.nc ${path_int}${met}/tmax_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_SN.nc ${path_int}${met}/recharge_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_adjust_SN.nc ${path_int}${met}/recharge_adjust_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pet_SN.nc ${path_int}${met}/pet_${w_level}.nc
# 	cdo selyear,$p_start/$p_end ${path_int}${met}/aET_SN.nc ${path_int}${met}/aET_${w_level}.nc
#     done
#     cd ..
    
    
# done

# for k in $(seq -f "%03g" 77 78); do
#     met="met_${k}"
#     echo "$met"
#     cd $met
#     PERIOD_start=("2011" "2025" "2049" "2069")
#     PERIOD_end=("2040" "2054" "2078" "2098")
#     warm=("1_5K" "2K" "3K" "4K")
#     i=0
#     for p_start in "${PERIOD_start[@]}"; do
#         p_end="${PERIOD_end[$i]}"
# 	w_level="${warm[$i]}"
#         echo "evaluate period ${p_start} - ${p_end} and global warming level ${w_level}"
#         i=$(($i + 1))
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pre_SN.nc ${path_int}${met}/pre_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/tmax_SN.nc ${path_int}${met}/tmax_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_SN.nc ${path_int}${met}/recharge_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_adjust_SN.nc ${path_int}${met}/recharge_adjust_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pet_SN.nc ${path_int}${met}/pet_${w_level}.nc
# 	cdo selyear,$p_start/$p_end ${path_int}${met}/aET_SN.nc ${path_int}${met}/aET_${w_level}.nc
#     done
#     cd ..
    
    
# done



# #.............................................................................................









# #~~~~~~~~~NorESM1-M~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# for k in $(seq -f "%03g" 82 87); do
#     met="met_${k}"
#     echo "$met"
#     cd $met
#     PERIOD_start=("2016" "2031" "2057")
#     PERIOD_end=("2045" "2060" "2086")
#     warm=("1_5K" "2K" "3K")
#     i=0
#     for p_start in "${PERIOD_start[@]}"; do
#         p_end="${PERIOD_end[$i]}"
# 	w_level="${warm[$i]}"
#         echo "evaluate period ${p_start} - ${p_end} and global warming level ${w_level}"
#         i=$(($i + 1))
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pre_SN.nc ${path_int}${met}/pre_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/tmax_SN.nc ${path_int}${met}/tmax_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_SN.nc ${path_int}${met}/recharge_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/recharge_adjust_SN.nc ${path_int}${met}/recharge_adjust_${w_level}.nc
# 	# cdo selyear,$p_start/$p_end ${path_int}${met}/pet_SN.nc ${path_int}${met}/pet_${w_level}.nc
# 	cdo selyear,$p_start/$p_end ${path_int}${met}/aET_SN.nc ${path_int}${met}/aET_${w_level}.nc
#     done
#     cd ..
    
    
# done
# #.........................




