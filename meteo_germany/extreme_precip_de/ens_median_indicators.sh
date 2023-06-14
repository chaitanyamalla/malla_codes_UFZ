#!/bin/sh
#!/bin/bash
#SBATCH -J extreme_precip
#SBATCH -o ./%x-%j.log
#SBATCH -t 1-24:00:00
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
#  Created:     Mi 27.01.2022
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce ensemble median of extreme precipitation indicators with different timeperiods for all METs for ${Region} for 2 rcps.
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------

set -x
set -e

path_int="/work/malla/meteo_germany/extreme_precip/data/"
path_out="/work/malla/meteo_germany/extreme_precip/test/"
path_end="/work/malla/meteo_germany/extreme_precip/ens_median/"
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
#RCPs=("rcp85")  
constants=("gtc10" "gtc20" "R90p" "R95p" "R99p")
constants=("gtc0p1" "gtc1")
    
PERIOD_start=("1971" "2021" "2036" "2069")
PERIOD_end=("2000" "2050" "2065" "2098")

for c in "${constants[@]}"; do
    if [[ $c == "gtc10" ]]; then
	indicator="pre_gt10"
	indicator_longname="average days above 10 mm rain per year"
	unit_abs="d/year"
	unit_abs_change="d/year"
	unit_rel_change="[%]"
	unit_absrelchange="d/year[%]"
    elif [[ $c == "gtc20" ]]; then
	unit_abs="d/year"
	unit_abs_change="d/year"
	unit_rel_change="[%]"
	unit_absrelchange="d/year[%]"
	indicator="pre_gt20"
	indicator_longname="average days above 20 mm rain per year"
    elif [[ $c == "R90p" ]]; then
	unit_abs="mm/day"
	unit_abs_change="mm/day"
	unit_rel_change="[%]"
	unit_absrelchange="mm/day[%]"
	indicator="pre_90p"
	indicator_longname="90th percentile of daily rain sums per 30 year period" 
    elif [[ $c == "R95p" ]]; then
	unit_abs="mm/day"
	unit_abs_change="mm/day"
	unit_rel_change="[%]"
	unit_absrelchange="mm/day[%]"
	indicator="pre_95p"
	indicator_longname="95th percentile of daily rain sums per 30 year period" 
    elif [[ $c == "R99p" ]]; then
	unit_abs="mm/day"
	unit_abs_change="mm/day"
	unit_absrelchange="mm/day[%]"
	unit_rel_change="[%]"
	indicator="pre_99p"
	indicator_longname="99th percentile of daily rain sums per 30 year period" 

    fi

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
	    
	    for c in "${constants[@]}"; do
	    	if [ $c == "gtc10" ] || [ $c == "gtc20" ] ; then
	    	    file="pre_yearly_${p_start}_${p_end}_${c}_ysum_timmean"
	    	elif [ $c == "R90p" ] || [ $c == "R95p" ] || [ $c == "R99p" ]; then
	    	    file="pre_yearly_${p_start}_${p_end}_${c}"
	    	fi

	    	files_rcp=$(for met in $mets; do echo "met_${met}/${file}.nc ";done)
	    	cdo -O enspctl,50 $files_rcp "${path_out}${file}_abs_${rcp}.nc"
		
    	    	cdo -O merge "${path_out}${file}_abs_${rcp}.nc" ${maskfile} "${path_out}${file}_tmp.nc"
    	    	cdo_expr="pre=(mask==0)?-9999:pre" 
	    	cdo expr,$cdo_expr "${path_out}${file}_tmp.nc" "${path_out}${file}_abs_${rcp}_${region}.nc"
        
	
	    	if [ $c == "gtc10" ] || [ $c == "gtc20" ]; then
	    	    hist="${path_out}pre_yearly_1971_2000_${c}_ysum_timmean_abs_${rcp}_${region}.nc"
	    	elif [ $c == "R90p" ] || [ $c == "R95p" ] || [ $c == "R99p" ]; then
	    	    hist="${path_out}pre_yearly_1971_2000_${c}_abs_${rcp}_${region}.nc" 
	    	fi
	    
 
		cdo sub "${path_out}${file}_abs_${rcp}_${region}.nc" "${hist}" "${path_out}${file}_abs_change_${rcp}_${region}.nc"
		cdo -mulc,100 -div "${path_out}${file}_abs_change_${rcp}_${region}.nc" "${hist}" "${path_out}${file}_rel_change_${rcp}_${region}.nc"
	    done
	done
	rm -rf *_tmp.nc
	if [ $c == "gtc10" ] || [ $c == "gtc20" ] ; then
	    merge_file="pre_yearly_20*_${c}_ysum_timmean"
	    merge_file_hist="pre_yearly_1971_2000_${c}_ysum_timmean"

	elif [ $c == "R90p" ] || [ $c == "R95p" ] || [ $c == "R99p" ]; then
	    merge_file="pre_yearly_20*_${c}"
	    merge_file_hist="pre_yearly_1971_2000_${c}"
	fi
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
