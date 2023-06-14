#!/bin/sh

#####  creating all the MET_00X files suitable to WW_leipzig with indicators into output_periods directory############


set -x
set -e

#path_int="/work/malla/ww_leipzig/input/"
path_int="/data/hydmet/WIS_D/ww_leipzig/data/"
path_out="/work/malla/ww_leipzig/output_periods/"


met_START=1
met_END=88

cd $path_out

for t in $(seq -f "%03g" $met_START $met_END); do
    met="met_${t}/"
    echo "$met"
    # if [ ! -d $met ]; then
    #     mkdir $met
    # fi

    cd $met

    PERIOD_start=("1971" "2021" "2036" "2070")
    PERIOD_end=("2000" "2050" "2065" "2099")
    #p_start=2070
    #p_end=2099
    i=0
    for p_start in "${PERIOD_start[@]}"; do
        p_end="${PERIOD_end[$i]}"
        echo "evaluate period ${p_start} - ${p_end}"
        i=$(($i + 1))
        

	# cdo selseason,ndjfma ${path_int}${met}pre_ug.nc ${path_out}${met}tmp_pre_ug_halfyear.nc
	# cdo selyear,$p_start/$p_end ${path_out}${met}tmp_pre_ug_halfyear.nc ${path_out}${met}tmp_pre_ug_halfyear_${p_start}_${p_end}.nc
	# cdo yearsum ${path_out}${met}tmp_pre_ug_halfyear_${p_start}_${p_end}.nc ${path_out}${met}tmp_pre_ug_halfyear_${p_start}_${p_end}_ysum.nc
	# cdo timmean ${path_out}${met}tmp_pre_ug_halfyear_${p_start}_${p_end}_ysum.nc ${path_out}${met}pre_ug_halfyear_${p_start}_${p_end}_ysum_timmean.nc
	# cdo fldpctl,50 ${path_out}${met}pre_ug_halfyear_${p_start}_${p_end}_ysum_timmean.nc ${path_out}${met}pre_ug_halfyear_${p_start}_${p_end}_ysum_timmean_fldpctl.nc

	# cdo selyear,$p_start/$p_end ${path_int}${met}recharge_ug.nc ${path_out}${met}tmp_recharge_ug_${p_start}_${p_end}.nc
	# cdo yearsum ${path_out}${met}tmp_recharge_ug_${p_start}_${p_end}.nc ${path_out}${met}tmp_recharge_ug_${p_start}_${p_end}_ysum.nc
	# cdo timmean ${path_out}${met}tmp_recharge_ug_${p_start}_${p_end}_ysum.nc ${path_out}${met}tmp_recharge_ug_${p_start}_${p_end}_ysum_timmean.nc
	# cdo fldpctl,50 ${path_out}${met}tmp_recharge_ug_${p_start}_${p_end}_ysum_timmean.nc ${path_out}${met}recharge_ug_${p_start}_${p_end}_ysum_timmean_fldpctl.nc 
 
	#  cdo gtc,25 ${path_int}${met}tavg_ug.nc ${path_out}${met}tmp_tavg_ug_gtc25.nc
	#  cdo selyear,$p_start/$p_end ${path_out}${met}tmp_tavg_ug_gtc25.nc ${path_out}${met}tmp_tavg_ug_gtc25_${p_start}_${p_end}.nc
	#  cdo yearsum ${path_out}${met}tmp_tavg_ug_gtc25_${p_start}_${p_end}.nc ${path_out}${met}tmp_tavg_ug_gtc25_${p_start}_${p_end}_ysum.nc
	#  cdo timmean ${path_out}${met}tmp_tavg_ug_gtc25_${p_start}_${p_end}_ysum.nc ${path_out}${met}tavg_ug_gtc25_${p_start}_${p_end}_ysum_timmean.nc
	#  cdo fldpctl,50 ${path_out}${met}tavg_ug_gtc25_${p_start}_${p_end}_ysum_timmean.nc ${path_out}${met}tavg_ug_gtc25_${p_start}_${p_end}_ysum_timmean_fldpctl.nc
	#rm tmp*

	############CDO to slect days with tmax>25 for various time periods and average of it overthe time period and median over the selected region##########
	#cdo -fldpctl,50 -timmean -yearsum -selyear,$p_start/$p_end -gtc,25 ${path_int}${met}tmax_ug.nc ${path_out}${met}tmax_ug_gtc25_${p_start}_${p_end}_ysum_timmean_fldpctl.nc
	############CDO to slect days with tmax>30 for various time periods and average of it overthe time period##########
	#cdo -fldpctl,50 -timmean -yearsum -selyear,$p_start/$p_end -gtc,30 ${path_int}${met}tmax_ug.nc ${path_out}${met}tmax_ug_gtc30_${p_start}_${p_end}_ysum_timmean_fldpctl.nc

	############CDO to select summer precipitation average for various time periods for various MET files in untersuchungsgebiet#######
	#cdo -fldpctl,50 -timmean -yearsum -selseason,mjjaso -selyear,$p_start/$p_end ${path_int}${met}pre_ug.nc ${path_out}${met}pre_ug_summer_${p_start}_${p_end}_ysum_timmean_fldpctl.nc

	############CDO to select yearly  precipitation average for various time periods for various MET files in untersuchungsgebiet#######
	cdo -fldpctl,50 -timmean -yearsum -selyear,$p_start/$p_end ${path_int}${met}pre_ug.nc ${path_out}${met}pre_ug_yearly_${p_start}_${p_end}_ysum_timmean_fldpctl.nc
        done
    cd ..	
done
