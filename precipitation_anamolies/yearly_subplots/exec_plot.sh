#!/bin/bash

set -e
set -x


#  -- load software --------------------------------

ml purge
ml foss/2019b texlive #load texlive for plotting
ml Anaconda3
source deactivate
source activate /global/apps/klimabuero/conda_py3.9.2/

INDICATORs=("pre")
#VARTYPEs=("abs" "perc")
VARTYPEs=("perc")

EVALPERIODs=("yearly")
for indicator in "${INDICATORs[@]}"; do
    for evalperiod in "${EVALPERIODs[@]}"; do
        for vartype in "${VARTYPEs[@]}"; do

	    python plot_pre_anamolies.py -p $evalperiod -s $vartype

		
	done
    done
done



		
