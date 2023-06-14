#!/bin/bash

# set -e
# set -x


#  -- load software --------------------------------

ml purge
ml foss/2019b texlive #load texlive for plotting
ml Anaconda3
source deactivate
source activate /global/apps/klimabuero/conda_py3.9.2/

##### -- define variables -----------------------------
VARTYPEs=("abs-rel_change") # "abs-rel_change")
RCPs=("rcp26" "rcp85")

for vartype in "${VARTYPEs[@]}"; do
    EVALPERIODs=("year")
    INDICATORs=("Qrouted_sum") # "Qrouted_sum")
    for indicator in "${INDICATORs[@]}"; do
        for evalperiod in "${EVALPERIODs[@]}"; do
	    for r in "${RCPs[@]}";do
		mv ./$indicator"_"$evalperiod"_"$vartype"_"$r"_ensp_25_germany_facc1.csv" $indicator"_"$evalperiod"_"$vartype"_"$r"_ensp25_germany_facc1.csv"
		mv ./$indicator"_"$evalperiod"_"$vartype"_"$r"_ensp_75_germany_facc1.csv" $indicator"_"$evalperiod"_"$vartype"_"$r"_ensp75_germany_facc1.csv"
            done
        done
    done
done
