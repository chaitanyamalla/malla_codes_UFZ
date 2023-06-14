#!/bin/bash
# set -x
# set -e


path_int="/data/hydmet/projects/MA_chaitanya/malla/data_sachsen/"


mets=$(seq -f "%03g" 1 2)" "$(seq -f "%03g" 7 10)" "$(seq -f "%03g" 21 31)" "$(seq -f "%03g" 35 37)" "$(seq -f "%03g" 40 41)" "$(seq -f "%03g" 50 58)" "$(seq -f "%03g" 67 78)" "$(seq -f "%03g" 82 87)



cd $path_int

for k in $mets; do
    
    met="met_${k}"
    echo "$met"
    cd $met

    #rm -f *.err *.out


    cd ..

done
