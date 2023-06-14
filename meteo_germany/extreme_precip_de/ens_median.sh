#!/bin/sh
#!/bin/bash
#SBATCH -J ensemblemedian
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
#  File:        ens_median.sh
#
#  Created:     Mi 27.01.2022
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce ensemble median of extreme precipitation indicators with different timeperiods for all METs for Germany for 2 rcps.
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------

set -x
set -e

path_int="/work/malla/meteo_germany/extreme_precip/data/"
path_out="/work/malla/meteo_germany/extreme_precip/ens_median/"
maskfile="/data/hicam/data/processed/dem_OR/mask_hicam_1km_g_inv.nc"

cd $path_int

mets_rcp85=$(seq -f "%03g" 1 2)" "$(seq -f "%03g" 7 10)" "$(seq -f "%03g" 21 31)" "$(seq -f "%03g" 35 37)" "$(seq -f "%03g" 40 41)" "$(seq -f "%03g" 50 58)" "$(seq -f "%03g" 67 78)" "$(seq -f "%03g" 82 87)
n_rcp85=$(wc -w <<< "$mets_rcp85")
echo "number of rcp85 members: $n_rcp85"

mets_rcp26=$(seq -f "%03g" 3 4)" "$(seq -f "%03g" 11 15)" 032 "$(seq -f "%03g" 38 39)" "$(seq -f "%03g" 42 45)" "$(seq -f "%03g" 59 62)" "$(seq -f "%03g" 79 80)" 088"
n_rcp26=$(wc -w <<< "$mets_rcp26")
echo "number of rcp26 members: $n_rcp26"

RCPs=("rcp26" "rcp85")

constants=("10" "20" "R90p" "R95p" "R99p")
    
PERIOD_start=("1971" "2021" "2036" "2069")
PERIOD_end=("2000" "2050" "2065" "2098")


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
		if [[ $c == "10" ]]; then
		    indicator="pre_gtc10mm"
		    indicator_longname="yearly precipitation greater than 10mm"
		elif [[ $c == "20" ]]; then
		    indicator="pre_gtc20mm"
		    indicator_longname="yearly precipitation greater than 10mm"

		fi

		file="pre_yearly_${p_start}_${p_end}_gtc${c}_ysum_timmean"
		files_rcp=$(for met in $mets; do echo "met_${met}/${file}.nc ";done)
		# cdo -O enspctl,50 $files_rcp "${path_out}${file}_abs_${rcp}.nc"



		cdo sub "${path_out}${file}_abs_${rcp}.nc" "${path_out}pre_yearly_1971_2000_gtc${c}_ysum_timmean_abs_${rcp}.nc"  "${path_out}${file}_abs_change_${rcp}.nc"
		cdo -mulc,100 -div "${path_out}${file}_abs_change_${rcp}.nc" "${path_out}pre_yearly_1971_2000_gtc${c}_ysum_timmean_abs_${rcp}.nc"  "${path_out}${file}_rel_change_${rcp}.nc"
            

	done
    done
done  
