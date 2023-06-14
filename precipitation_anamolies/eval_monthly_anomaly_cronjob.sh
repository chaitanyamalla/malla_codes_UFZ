#!/bin/bash

#SBATCH -J precip_anamolies_cronjob_result 
#SBATCH -o ./%x-%j.log
#SBATCH -t 0-5:00:00
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-user=chaitanya.malla@ufz.de
#SBATCH --mail-type=BEGIN,END
#SBATCH --output=./%x-%A-%a.out
#SBATCH --error=./%x-%A-%a.err

# -*- coding: utf-8 -*-
#set -x
#set -e


ml purge # removes all activated modules
ml Anaconda3 # loads Anaconda
source activate /global/apps/klimabuero/conda_py3.9.2/

inpath="./data/"
outpath="./data/processed/"
result="./data/results/"
end_result="./data/end_results/"


lastdayoflastmonth=$(date --date="$(date +'%Y-%m-01') - 1 day" +%Y-%m-%d)
echo "last day in last month is "$lastdayoflastmonth

var1=$(date +%Y%m%d)  # today date
echo "today is "$var1
var2=$(date +%Y%m02)  # 2 rd of every month
var3=$(date +%Y%m06)  # 6th of every month


if [ $var1 -ge $var2 ] && [ $var1 -le $var3 ];then
    
    echo "today's date is in script's date range";
    cdo showdate ${outpath}pre_2020_present_daily.nc > ${outpath}/months.txt
    data_last_date=`cat ${outpath}/months.txt | rev | cut -d' ' -f 1 | rev`
    echo "data_last_day = "$data_last_date

    if [ $lastdayoflastmonth == $data_last_date ];then 
    	echo "Starting cronjob of monthly anamolies";

	
	cdo monsum ${outpath}pre_2020_present_daily.nc ${outpath}pre_2020_present_monsum.nc

	# ####---------------------anamoly differences---------------------------------------
	cdo ymonsub ${outpath}pre_2020_present_monsum.nc ${outpath}pre_1981_2010_monsum_ymonmean.nc ${result}pre_monthly_anomaly_abs_change_2020_present_wrt_1981_2010mean.nc
	cdo ymonsub ${outpath}pre_2020_present_monsum.nc ${outpath}pre_1991_2020_monsum_ymonmean.nc ${result}pre_monthly_anomaly_abs_change_2020_present_wrt_1991_2020mean.nc

	# ####-------------------anamoly percentage-----------------------------------------

	cdo -mulc,100 -ymondiv ${result}pre_monthly_anomaly_abs_change_2020_present_wrt_1981_2010mean.nc ${outpath}pre_1981_2010_monsum_ymonmean.nc ${result}pre_monthly_anomaly_perc_2020_present_wrt_1981_2010mean.nc
	cdo -mulc,100 -ymondiv ${result}pre_monthly_anomaly_abs_change_2020_present_wrt_1991_2020mean.nc ${outpath}pre_1991_2020_monsum_ymonmean.nc ${result}pre_monthly_anomaly_perc_2020_present_wrt_1991_2020mean.nc 


	#### # ----------------- merging times from 1951 to present --------------------
	cdo -mergetime -selyear,1951/2019 ${result}pre_monthly_anomaly_abs_change_1951_2022_wrt_1981_2010mean.nc ${result}pre_monthly_anomaly_abs_change_2020_present_wrt_1981_2010mean.nc ${end_result}pre_monthly_anomaly_abs_change_1951_present_wrt_1981_2010mean.nc
	cdo -mergetime -selyear,1951/2019 ${result}pre_monthly_anomaly_abs_change_1951_2022_wrt_1991_2020mean.nc ${result}pre_monthly_anomaly_abs_change_2020_present_wrt_1991_2020mean.nc ${end_result}pre_monthly_anomaly_abs_change_1951_present_wrt_1991_2020mean.nc

	cdo -mergetime -selyear,1951/2019 ${result}pre_monthly_anomaly_perc_1951_2022_wrt_1981_2010mean.nc ${result}pre_monthly_anomaly_perc_2020_present_wrt_1981_2010mean.nc ${end_result}pre_monthly_anomaly_perc_1951_present_wrt_1981_2010mean.nc
	cdo -mergetime -selyear,1951/2019 ${result}pre_monthly_anomaly_perc_1951_2022_wrt_1991_2020mean.nc ${result}pre_monthly_anomaly_perc_2020_present_wrt_1991_2020mean.nc ${end_result}pre_monthly_anomaly_perc_1951_present_wrt_1991_2020mean.nc


    # elif [ $var1 -eq $var3 ] && [ $data_last_date -lt $lastdayoflastmonth ];then
    # 	echo "data of last month is not completely available"
   
    else 
	echo "Not starting cron job of Monthly Anomalies, because last day of last  month is not available";
    fi

else
    echo "today is out of the script's date range"
fi



