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

data="/work/malla/meteo_germany/precipitation_anamolies/data/results/" 
var=("wrt_1981_2010mean" "wrt_1991_2020mean")
file="pre_yearly_anomaly_perc_1951_2022_"

lower_limit=1951
upper_limit=2023
range=10

for ((i=lower_limit; i<=upper_limit; i++)); do
    year=$i
    echo $year
    for bling in ${var[@]}; do
	echo $bling
       
	cdo selyear,${year} ${data}${file}${bling}.nc ./tmp/pre_${year}_anomaly_perc_${bling}.nc

    done

done
