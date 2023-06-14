#!/bin/bash

set -e
set -x



#  -- load software --------------------------------

# ml purge
# ml foss/2019b texlive #load texlive for plotting
# ml Anaconda3
# source deactivate
# source activate /global/apps/klimabuero/conda_py3.9.2/
# #  -- define variables -----------------------------

eval="ensemble"

VARTYPEs=("abs-rel_change")

# VARTYPEs=("rel_change")
# VARTYPEs=("abs-rel_change")
for vartype in "${VARTYPEs[@]}"; do
    EVALPERIODs=("year")
    INDICATORs=("Qrouted_daily_sum")
    for indicator in "${INDICATORs[@]}"; do
        for evalperiod in "${EVALPERIODs[@]}"; do

	    python write_latex.py -i $indicator -e $evalperiod -t $vartype
	done

        
    done
done
