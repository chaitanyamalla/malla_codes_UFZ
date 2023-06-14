#!/bin/bash

#SBATCH -J precip_anamolies
#SBATCH -o ./%x-%j.log
#SBATCH -t 0-1:00:00
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

# #####----------------------creation of monthly precipitation nc file ----------
# cdo mergetime ${inpath}pre_1947_2019.nc ${inpath}pre_2020_present.nc ${outpath}pre_1947_present.nc
# cdo selyear,1951/2022 ${outpath}pre_1947_present.nc ${outpath}pre_1951_2022.nc
# cdo monsum ${outpath}pre_1951_2022.nc ${outpath}pre_1951_2022_monsum.nc


# #####---------------------creating yearly precipitation sum nc file ----------
# cdo yearsum ${outpath}pre_1951_2022.nc ${outpath}pre_1951_2022_ysum.nc


# #####----------------------reference timeperiod files to calculate anomalies----------------------------------
# cdo -ymonmean -selyear,1981/2010 ${outpath}pre_1951_2022_monsum.nc ${outpath}pre_1981_2010_monsum_ymonmean.nc
# cdo -ymonmean -selyear,1991/2020 ${outpath}pre_1951_2022_monsum.nc ${outpath}pre_1991_2020_monsum_ymonmean.nc

# cdo -timmean -selyear,1981/2010 ${outpath}pre_1951_2022_ysum.nc ${outpath}pre_1981_2010_ysum_timmean.nc
# cdo -timmean -selyear,1991/2020 ${outpath}pre_1951_2022_ysum.nc ${outpath}pre_1991_2020_ysum_timmean.nc


# ####---------------------anamoly differences---------------------------------------
cdo ymonsub ${outpath}pre_1951_2022_monsum.nc ${outpath}pre_1981_2010_monsum_ymonmean.nc ${result}pre_monthly_anomaly_abs_change_1951_2022_wrt_1981_2010mean.nc
cdo ymonsub ${outpath}pre_1951_2022_monsum.nc ${outpath}pre_1991_2020_monsum_ymonmean.nc ${result}pre_monthly_anomaly_abs_change_1951_2022_wrt_1991_2020mean.nc

cdo sub ${outpath}pre_1951_2022_ysum.nc ${outpath}pre_1981_2010_ysum_timmean.nc ${result}pre_yearly_anomaly_abs_change_1951_2022_wrt_1981_2010mean.nc
cdo sub ${outpath}pre_1951_2022_ysum.nc ${outpath}pre_1991_2020_ysum_timmean.nc ${result}pre_yearly_anomaly_abs_change_1951_2022_wrt_1991_2020mean.nc


# ####-------------------anamoly percentage-----------------------------------------

# cdo -mulc,100 -ymondiv ${result}pre_monthly_anomaly_abs_1951_2022_wrt_1981_2010mean.nc ${outpath}pre_1981_2010_monsum_ymonmean.nc ${result}pre_monthly_anomaly_perc_1951_2022_wrt_1981_2010mean.nc
# cdo -mulc,100 -ymondiv ${result}pre_monthly_anomaly_abs_1951_2022_wrt_1991_2020mean.nc ${outpath}pre_1991_2020_monsum_ymonmean.nc ${result}pre_monthly_anomaly_perc_1951_2022_wrt_1991_2020mean.nc 

# cdo -mulc,100 -div ${result}pre_yearly_anomaly_abs_1951_2022_wrt_1981_2010mean.nc ${outpath}pre_1981_2010_ysum_timmean.nc ${result}pre_yearly_anomaly_perc_1951_2022_wrt_1981_2010mean.nc
# cdo -mulc,100 -div ${result}pre_yearly_anomaly_abs_1951_2022_wrt_1991_2020mean.nc ${outpath}pre_1991_2020_ysum_timmean.nc ${result}pre_yearly_anomaly_perc_1951_2022_wrt_1991_2020mean.nc

####---------------anamolies from 2018-------------------------------------------------
# cdo selyear,2018/2022 ${result}pre_monthly_anomaly_perc_1951_2022_wrt_1981_2010mean.nc ${result}pre_monthly_anomaly_perc_2018_2022_wrt_1981_2010mean.nc
# cdo selyear,2018/2022 ${result}pre_monthly_anomaly_perc_1951_2022_wrt_1991_2020mean.nc ${result}pre_monthly_anomaly_perc_2018_2022_wrt_1991_2020mean.nc

# cdo selyear,2018/2022 ${result}pre_yearly_anomaly_perc_1951_2022_wrt_1981_2010mean.nc ${result}pre_yearly_anomaly_perc_2018_2022_wrt_1981_2010mean.nc
# cdo selyear,2018/2022 ${result}pre_yearly_anomaly_perc_1951_2022_wrt_1991_2020mean.nc ${result}pre_yearly_anomaly_perc_2018_2022_wrt_1991_2020mean.nc


cdo selyear,2018/2022 ${result}pre_monthly_anomaly_abs_change_1951_2022_wrt_1981_2010mean.nc ${result}pre_monthly_anomaly_abs_change_2018_2022_wrt_1981_2010mean.nc
cdo selyear,2018/2022 ${result}pre_monthly_anomaly_abs_change_1951_2022_wrt_1991_2020mean.nc ${result}pre_monthly_anomaly_abs_change_2018_2022_wrt_1991_2020mean.nc

cdo selyear,2018/2022 ${result}pre_yearly_anomaly_abs_change_1951_2022_wrt_1981_2010mean.nc ${result}pre_yearly_anomaly_abs_change_2018_2022_wrt_1981_2010mean.nc
cdo selyear,2018/2022 ${result}pre_yearly_anomaly_abs_change_1951_2022_wrt_1991_2020mean.nc ${result}pre_yearly_anomaly_abs_change_2018_2022_wrt_1991_2020mean.nc
