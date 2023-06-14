#!/bin/bash
set -x
set -e


path_int="/data/hydmet/projects/MA_chaitanya/data_climproj/"
path_out="/work/malla/sachsen_files/"

# mets=$(seq -f "%03g" 1 2)" "$(seq -f "%03g" 7 10)" "$(seq -f "%03g" 21 31)" "$(seq -f "%03g" 35 37)" "$(seq -f "%03g" 40 41)" "$(seq -f "%03g" 50 58)" "$(seq -f "%03g" 67 78)" "$(seq -f "%03g" 82 87)




###only 4K warming files--------------
mets=$(seq -f "%03g" 1 2)" "$(seq -f "%03g" 35 37)" "$(seq -f "%03g" 50 58)" "$(seq -f "%03g" 77 78)

cd $path_int

for k in $mets; do
    
    met="met_${k}"
    echo "$met"
    
    cd $met

    #mv *_1_5K.nc ${path_out}${met}/
    #mv *_2K.nc ${path_out}${met}/
    #mv *_3K.nc ${path_out}${met}/
    mv *_4K.nc ${path_out}${met}/


    cd ..

done



### 1 2 35-37  50-58 77-78
