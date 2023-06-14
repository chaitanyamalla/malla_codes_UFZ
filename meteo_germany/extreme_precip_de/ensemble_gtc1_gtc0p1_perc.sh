#!/bin/sh
#!/bin/bash
#SBATCH -J extreme_precip
#SBATCH -o ./%x-%j.log
#SBATCH -t 0-5:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --mail-user=chaitanya.malla@ufz.de
#SBATCH --mail-type=BEGIN,END
#SBATCH --output=./%x-%A-%a.out
#SBATCH --error=./%x-%A-%a.err

# -*- coding: utf-8 -*-
ml purge # removes all activated modules
ml Anaconda3 # loads Anaconda
source activate /global/apps/klimabuero/conda_py3.9.2/

# --------------------------------------------------
#  File:        ens_median.sh
#
#  Created:     Mi 08.03.2022
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce ensemble median of extreme precipitation indicators with different timeperiods for all METs for ${Region} for 2 rcps.
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------set -x
set -x
set -e

path_int="/work/malla/meteo_germany/extreme_precip/data1_with_intermediate/"
path_out="/work/malla/meteo_germany/extreme_precip/test1_pre_gt0p1_gt1_perc_rcp/"
path_end="/work/malla/meteo_germany/extreme_precip/ens_median_pre_gt0p1_gt1_perc_rcp/"
maskfile="/data/hicam/data/processed/dem_OR/mask_hicam_1km_ghw_inv.nc"
region="de_hicam"

cd $path_int

mets_rcp85=$(seq -f "%03g" 1 2)" "$(seq -f "%03g" 7 10)" "$(seq -f "%03g" 21 31)" "$(seq -f "%03g" 35 37)" "$(seq -f "%03g" 40 41)" "$(seq -f "%03g" 50 58)" "$(seq -f "%03g" 67 78)" "$(seq -f "%03g" 82 87)
n_rcp85=$(wc -w <<< "$mets_rcp85")
echo "number of rcp85 members: $n_rcp85"

mets_rcp26=$(seq -f "%03g" 3 4)" "$(seq -f "%03g" 11 15)" 032 "$(seq -f "%03g" 38 39)" "$(seq -f "%03g" 42 45)" "$(seq -f "%03g" 59 62)" "$(seq -f "%03g" 79 80)" 088"
n_rcp26=$(wc -w <<< "$mets_rcp26")
echo "number of rcp26 members: $n_rcp26"

RCPs=("rcp26" "rcp85")
constants=("gt0p1" "gt1")
percentiles=("R90p" "R95p" "R99p")

    
PERIOD_start=("1971" "2021" "2036" "2069")
PERIOD_end=("2000" "2050" "2065" "2098")

for c in "${constants[@]}"; do
    for k in "${percentiles[@]}"; do
	indicator="pre_${c}_${k}"
	indicator_longname="${k:1:2}th percentile of daily rain sums per 30 year period with days above (${c} mm) rain"
    	unit_abs="mm/day"
    	unit_abs_change="mm/day"
    	unit_absrelchange="mm/day[%]"
    	unit_rel_change="[%]"


	for rcp in "${RCPs[@]}"; do
            if [[ $rcp == "rcp26" ]]; then
            mets=$mets_rcp26
	    elif [[ $rcp == "rcp85" ]]; then
            mets=$mets_rcp85
	    fi

	    i=0
	    for p_start in "${PERIOD_start[@]}"; do
		p_end="${PERIOD_end[$i]}"
		echo "evaluate period ${p_start} - ${p_end}"
		i=$(($i + 1))

		file="pre_yearly_${p_start}_${p_end}_${c}_${k}"
		files_rcp=$(for met in $mets; do echo "met_${met}/${file}.nc ";done)
	    	cdo -O enspctl,50 $files_rcp "${path_out}${file}_abs_${rcp}.nc"
    	    	cdo -O merge "${path_out}${file}_abs_${rcp}.nc" ${maskfile} "${path_out}${file}_tmp.nc"
    	    	cdo_expr="pre=(mask==0)?-9999:pre" 
	    	cdo expr,$cdo_expr "${path_out}${file}_tmp.nc" "${path_out}${file}_abs_${rcp}_${region}.nc"
		hist="${path_out}pre_yearly_1971_2000_${c}_${k}_abs_${rcp}_${region}.nc" 
		cdo sub "${path_out}${file}_abs_${rcp}_${region}.nc" "${hist}" "${path_out}${file}_abs_change_${rcp}_${region}.nc"
		cdo -mulc,100 -div "${path_out}${file}_abs_change_${rcp}_${region}.nc" "${hist}" "${path_out}${file}_rel_change_${rcp}_${region}.nc"
		rm -rf *_tmp.nc
	    done
	    merge_file="pre_yearly_20*_${c}_${k}"
	    merge_file_hist="pre_yearly_1971_2000_${c}_${k}"
	    cdo -O mergetime "${path_out}${merge_file}_abs_change_${rcp}_${region}.nc" "${path_end}${indicator}_year_abs_change_${rcp}_ensmedian_${region}.nc"
	    cdo -O mergetime "${path_out}${merge_file}_rel_change_${rcp}_${region}.nc" "${path_end}${indicator}_year_rel_change_${rcp}_ensmedian_${region}.nc"
	    cdo -O mergetime "${path_out}${merge_file_hist}_abs_${rcp}_${region}.nc" "${path_out}${merge_file}_abs_${rcp}_${region}.nc" "${path_end}${indicator}_year_abs_${rcp}_ensmedian_${region}.nc"
	    cdo -O mergetime "${path_out}${merge_file_hist}_abs_${rcp}_${region}.nc" "${path_end}${indicator}_year_abs_change_${rcp}_ensmedian_${region}.nc" "${path_end}${indicator}_year_abs-abs_change_${rcp}_ensmedian_${region}.nc"
	    cdo -O mergetime "${path_out}${merge_file_hist}_abs_${rcp}_${region}.nc" "${path_end}${indicator}_year_rel_change_${rcp}_ensmedian_${region}.nc" "${path_end}${indicator}_year_abs-rel_change_${rcp}_ensmedian_${region}.nc"
	    	
	#---------ATTRIBUTES------------------------
        VAR_TYPEs=("abs" "abs_change" "rel_change" "abs-abs_change" "abs-rel_change")
        for var_type in "${VAR_TYPEs[@]}"; do
            file="${path_end}${indicator}_year_${var_type}_${rcp}_ensmedian_${region}.nc"
            if [[ $var_type == "abs" ]]; then
                unit="${unit_abs}"
            elif [[ $var_type == "abs_change" ]]; then
                unit="${unit_abs_change}"
            elif [[ $var_type == "rel_change" ]]; then
                unit="${unit_rel_change}"
	    elif [[ $var_type == "abs-abs_change" ]]; then
		unit="${unit_abs_change}"
	    elif [[ $var_type == "abs-rel_change" ]]; then
		unit="${unit_absrelchange}"
		
            fi
            ncrename -v "pre",${indicator} $file
            ncatted -a units,${indicator},m,c,$unit $file
            ncatted -a long_name,${indicator},m,c,"${var_type}: ${indicator_longname}" $file

	done
	
		
	done
    done
done
