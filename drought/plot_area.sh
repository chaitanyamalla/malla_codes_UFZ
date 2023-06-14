#!/bin/bash

#SBATCH -J drought_area_germany
#SBATCH -o ./%x-%j.log
#SBATCH -t 0-1:00:00
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-user=chaitanya.malla@ufz.de
#SBATCH --mail-type=BEGIN,END
#SBATCH --output=./%x-%A-%a.out
#SBATCH --error=./%x-%A-%a.err

#  -- load software --------------------------------



ml purge
ml Anaconda3
source deactivate
source activate /global/apps/klimabuero/conda_py3.9.2/


cd /work/malla/GDM//droughtmaps/
var='SM_Lall SM_L02'


lower_limit=1951
upper_limit=2023
range=10

# for ((i=lower_limit; i<=upper_limit; i+=range)); do
    # start_range=$i
    # end_range=$((i+range-1))
    # echo "Range $start_range-$end_range"

for ((i=lower_limit; i<=upper_limit; i++)); do
    year=$i
    echo $year
    for bling in ${var}; do
	#echo $bling
	# cdo selyear,${start_range}/${end_range} ./data/${bling}_1951_202306_daily.nc ./tmp/${bling}_${start_range}_${end_range}_daily.nc

	cdo selyear,${year} ./data/${bling}_1951_202306_daily.nc ./tmp1/${bling}_${year}_daily.nc
	# python ./area_under_drought.py -i tmp/${bling}_${start_range}_${end_range}_daily.nc -g area_${bling}_${start_range}_${end_range}.png
	# python ./area_under_drought.py -i tmp/${bling}_${start_range}_${end_range}_daily.nc -p area_${bling}_${start_range}_${end_range}.pdf
    done

done


