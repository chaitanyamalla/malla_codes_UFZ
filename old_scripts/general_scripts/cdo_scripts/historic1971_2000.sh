set -x
set -e

path_int="/work/malla/ww_leipzig/input/"
path_out="/work/malla/ww_leipzig/output_periods/"


met_START=3
met_END=88

cd $path_out

for t in $(seq -f "%03g" $met_START $met_END); do
    met="met_${t}/"
    echo "$met"
cd $met
   p_start=1971
   p_end=2000

     cdo selseason,djf ${path_int}${met}pre_ug.nc ${path_out}${met}tmp_pre_ug_djf.nc
     cdo selyear,$p_start/$p_end ${path_out}${met}tmp_pre_ug_djf.nc ${path_out}${met}tmp_pre_ug_djf_${p_start}_${p_end}.nc
     cdo yearsum ${path_out}${met}tmp_pre_ug_djf_${p_start}_${p_end}.nc ${path_out}${met}tmp_pre_ug_djf_${p_start}_${p_end}_ysum.nc
     cdo timmean ${path_out}${met}tmp_pre_ug_djf_${p_start}_${p_end}_ysum.nc ${path_out}${met}pre_ug_djf_${p_start}_${p_end}_ysum_timmean.nc
     cdo fldpctl,50 ${path_out}${met}pre_ug_djf_${p_start}_${p_end}_ysum_timmean.nc ${path_out}${met}pre_ug_djf_${p_start}_${p_end}_ysum_timmean_fldpctl.nc 
 
     cdo gtc,25 ${path_int}${met}tavg_ug.nc ${path_out}${met}tmp_tavg_ug_gtc25.nc
     cdo selyear,$p_start/$p_end ${path_out}${met}tmp_tavg_ug_gtc25.nc ${path_out}${met}tmp_tavg_ug_gtc25_${p_start}_${p_end}.nc
     cdo yearsum ${path_out}${met}tmp_tavg_ug_gtc25_${p_start}_${p_end}.nc ${path_out}${met}tmp_tavg_ug_gtc25_${p_start}_${p_end}_ysum.nc
     cdo timmean ${path_out}${met}tmp_tavg_ug_gtc25_${p_start}_${p_end}_ysum.nc ${path_out}${met}tavg_ug_gtc25_${p_start}_${p_end}_ysum_timmean.nc
     cdo fldpctl,50 ${path_out}${met}tavg_ug_gtc25_${p_start}_${p_end}_ysum_timmean.nc ${path_out}${met}tavg_ug_gtc25_${p_start}_${p_end}_ysum_timmean_fldpctl.nc
     rm tmp*
     cd ..
done
