#!/bin/bash

#SBATCH -J Dams_facc
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


search_dir=/work/malla/meteo_germany/DE_indicatorsdata/facc/data_qrouted_daily

for entry in "$search_dir"/Qrouted_daily_sum_year_abs-rel_*
do
  #echo "working on $entry"
  filename="${entry##*/}"
  file="${filename%.*}"
  echo "$file"

  

  ifile=$entry #.nc4 file to read
  istnlst="/work/malla/meteo_germany/DE_indicatorsdata/facc/Dams_for_qrouted1_new.csv" #list of lat-lon for which to extract TS
  # istnlst="/work/malla/meteo_germany/DE_indicatorsdata/facc/Bodensee/Bodensee.csv"
  ofile="/work/malla/meteo_germany/DE_indicatorsdata/facc/data_tmp/"
  # ofile="/work/malla/meteo_germany/DE_indicatorsdata/facc/Bodensee/tmp/"
  while read p ; do
      str=$(echo $p | cut -d ',' -f 1)
      stn="${str// /_}"
      echo $stn

      
      echo $p; lon=$(echo $p | cut -d ',' -f 2); lat=$(echo $p | cut -d ',' -f 3);
      cdo -outputtab,date,lon,lat,value -remapnn,lon=${lon}_lat=${lat} $ifile > $ofile$stn".csv"
    
      sed -i -e '1c<php' $ofile$stn".csv"
      sed -i '1d' $ofile$stn".csv"
      sed -i -e 's/^/#/g' $ofile$stn".csv"
      sed -i -e "s/#/${stn}/g" $ofile$stn".csv" #replace value column name w/ stn name
      sed -i -e 's/  */ /g' $ofile$stn".csv"
      sed -i -e "s/\s/,/g" $ofile$stn".csv"

      echo
  done <$istnlst
######rm -f /work/malla/meteo_germany/DE_indicatorsdata/facc/test/all.csv
  cp /work/malla/meteo_germany/DE_indicatorsdata/facc/01_dam.csv ${ofile}01_dam.csv
  rm -rf ${ofile}Name.csv
  cat $ofile*.csv >> /work/malla/meteo_germany/DE_indicatorsdata/facc/dams_output_csv/daily/${file}.csv
  rm -f /work/malla/meteo_germany/DE_indicatorsdata/facc/data_tmp/*
  #####cat $ofile*.csv >> /work/malla/meteo_germany/DE_indicatorsdata/facc/${file}.csv

done


