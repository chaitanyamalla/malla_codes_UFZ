
#!/bin/sh



# --------------------------------------------------
#  File:        producing_indicator_difference_DE.sh
#
#  Created:     Mi 23-06-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce difference of all METfiles indicators with time period 1971_2000  
#
#  Modified by: 
#  Modified date:
#
# --------------------------------------------------
set -x
set -e

path_out="/work/malla/meteo_germany/data_output/"


cd $path_out

mets=$(seq -f "%03g" 1 4)" "$(seq -f "%03g" 7 15)" "$(seq -f "%03g" 21 32)" "$(seq -f "%03g" 35 45)" "$(seq -f "%03g" 50 62)" "$(seq -f "%03g" 67 80)" "$(seq -f "%03g" 82 88) ###----recharge adjusted---### only rcp2.6 and 8.5

for t in $mets; do
    met="met_${t}/"
    echo "$met"


    cd $met

    PERIOD_start=("2021" "2036") #"2070")
    PERIOD_end=("2050" "2065") #"2099")
 
    i=0
    for p_start in "${PERIOD_start[@]}"; do
        p_end="${PERIOD_end[$i]}"
        echo "evaluate period ${p_start} - ${p_end}"
        i=$(($i + 1))

	cdo sub ${path_out}${met}pre_yearly_${p_start}_${p_end}_ysum_timmean_fldpctl.nc pre_yearly_1971_2000_ysum_timmean_fldpctl.nc ${path_out}${met}pre_yearly_${p_start}_${p_end}_ysum_timmean_fldpctl_difference.nc

	cdo sub ${path_out}${met}pre_winter_${p_start}_${p_end}_ysum_timmean_fldpctl.nc pre_winter_1971_2000_ysum_timmean_fldpctl.nc ${path_out}${met}pre_winter_${p_start}_${p_end}_ysum_timmean_fldpctl_difference.nc

	cdo sub ${path_out}${met}pre_summer_${p_start}_${p_end}_ysum_timmean_fldpctl.nc pre_summer_1971_2000_ysum_timmean_fldpctl.nc ${path_out}${met}pre_summer_${p_start}_${p_end}_ysum_timmean_fldpctl_difference.nc

	cdo sub ${path_out}${met}tmax25_${p_start}_${p_end}_ysum_timmean_fldpctl.nc tmax25_1971_2000_ysum_timmean_fldpctl.nc ${path_out}${met}tmax25_${p_start}_${p_end}_ysum_timmean_fldpctl_difference.nc

	cdo sub ${path_out}${met}tmax30_${p_start}_${p_end}_ysum_timmean_fldpctl.nc tmax30_1971_2000_ysum_timmean_fldpctl.nc ${path_out}${met}tmax30_${p_start}_${p_end}_ysum_timmean_fldpctl_difference.nc

	cdo sub ${path_out}${met}recharge_adjust_${p_start}_${p_end}_ysum_timmean_fldpctl.nc recharge_adjust_1971_2000_ysum_timmean_fldpctl.nc ${path_out}${met}recharge_adjust_${p_start}_${p_end}_ysum_timmean_fldpctl_difference.nc


    done
    cd ..
done
   
