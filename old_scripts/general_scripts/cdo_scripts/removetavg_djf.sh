set -x
set -e
path_out="/work/malla/ww_leipzig/output_periods/"


met_START=3
met_END=88

cd $path_out

for t in $(seq -f "%03g" $met_START $met_END); do
    met="met_${t}/"
    echo "$met"
    cd $met
    rm tavg_ug_djf*
    cd ..   
 done 



