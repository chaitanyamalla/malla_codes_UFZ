#!/bin/bash

set -e
set -x


#  -- load software --------------------------------

ml purge
ml foss/2019b texlive #load texlive for plotting
ml Anaconda3
source deactivate
source activate /global/apps/klimabuero/conda_py3.9.2/
#  -- define variables -----------------------------

# VARs=("pre" "tmax")
#VARTYPEs=("abs" "rel_change" "abs_change")
RCP_TYPEs=("rcp26" "rcp85")
# RCP_TYPEs=("rcp85")
#INDICATORs=("n_heatdays" "n_summerdays" "pre_sum" "tavg_mean" "recharge_adjust_sum")
# INDICATORs=("n_heatdays")
# INDICATORs=("n_summerdays")

region="germany"
# region="ww_leipzig_ug"
# region="de_hicam"

echo "Note that do_main_catch_ger and grid (2x2) has to be set on in script!"


# VARTYPEs=("abs-abs_change" "abs_change")
# VARTYPEs=("abs_change")
# VARTYPEs=("abs-abs_change")
# for vartype in "${VARTYPEs[@]}"; do
#     # for rcp_type in "${RCP_TYPEs[@]}"; do
#     #     python plot_indicators.py -g png -e "year" -t $vartype -i "n_heatdays" -r $rcp_type -m $region -l "German" -s "ensmedian"
#     #     python plot_indicators.py -g png -e "year" -t $vartype -i "n_summerdays" -r $rcp_type -m $region -l "German" -s "ensmedian"
#     #     # python plot_indicators.py -g png -e "year" -t $vartype -i "n_consec_heatdays" -r $rcp_type -m $region -l "German" -s "ensmedian"
#     #     # python plot_indicators.py -g png -e "year" -t $vartype -i "n_consec_summerdays" -r $rcp_type -m $region -l "German" -s "ensmedian"
#     # done
#     python join_tables.py -i "n_heatdays" -e "year" -t $vartype -s "ensemble"
#     python join_tables.py -i "n_heatdays" -e "year" -t $vartype -s "spatial"
#     python join_tables.py -i "n_summerdays" -e "year" -t $vartype -s "ensemble"
#     python join_tables.py -i "n_summerdays" -e "year" -t $vartype -s "spatial"
#     # python join_tables.py -i "n_consec_heatdays" -e "year" -t $vartype
#     # python join_tables.py -i "n_consec_summerdays" -e "year" -t $vartype

# done
# #     #  -- calculate seasonal and yearly ---------------------------
    
# VARTYPEs=("abs_change")
# VARTYPEs=("abs")
# VARTYPEs=("abs" "abs-abs_change" "abs_change")
# VARTYPEs=("abs_change")
# for vartype in "${VARTYPEs[@]}"; do
#     EVALPERIODs=("summer" "winter" "spring" "autumn" "year")
# #     INDICATORs=("pre_sum" "tavg_mean" "recharge_adjust_sum")
# #     INDICATORs=("tavg_mean")
# #     # INDICATORs=("recharge_adjust_sum")
# #     # INDICATORs=("pre_sum")
#     INDICATORs=("aET_sum" "PET_sum")
#     INDICATORs=("PET_sum")

#     for indicator in "${INDICATORs[@]}"; do
#         for evalperiod in "${EVALPERIODs[@]}"; do
#             for rcp_type in "${RCP_TYPEs[@]}"; do
#                 python plot_indicators.py -g png -e $evalperiod -t $vartype -i $indicator -r $rcp_type -m $region -l "German" -s "ensmedian"
#             done
#             # python join_tables.py -i $indicator -e $evalperiod -t $vartype -s "ensemble"
#             # python join_tables.py -i $indicator -e $evalperiod -t $vartype -s "spatial"
#         done
#     done
# done

VARTYPEs=("rel_change")
#VARTYPEs=("abs-rel_change" "abs-abs_change")
for vartype in "${VARTYPEs[@]}"; do
    EVALPERIODs=("summer") #"shy" "why" "year" "winter" "spring" "autumn")
    INDICATORs=("Qrouted_sum") #"Qrouted_p50")
    #INDICATORs=("Qrouted_sum" "Qrouted_p10" "Qrouted_p50" "Qrouted_p90")

    for indicator in "${INDICATORs[@]}"; do
        for evalperiod in "${EVALPERIODs[@]}"; do
            for rcp_type in "${RCP_TYPEs[@]}"; do
                #python plot_indicators.py -g png -e $evalperiod -t $vartype -i $indicator -r $rcp_type -m $region -l "German" -s "ensmedian"
            
		python join_tables.py -i $indicator -e $evalperiod -t $vartype -s "ensemble"
	    done
            # python join_tables.py -i $indicator -e $evalperiod -t $vartype -s "spatial"
        done
    done
done
# VARTYPEs=("abs_change" "abs" "abs-rel_change" "abs-abs_change")
# VARTYPEs=("abs")
# for vartype in "${VARTYPEs[@]}"; do
#     EVALPERIODs=("summer")
#     EVALPERIODs=("year")
#     # INDICATORs=("pre_gt10" "pre_gt20" "pre_90p" "pre_99p")
#     #INDICATORs=("pre_sum" "aET_sum")
#     #INDICATORs=("aET_sum")
#     # INDICATORs=("recharge_sum")
#     INDICATORs=("pre_90p" "pre_99p")

#     for indicator in "${INDICATORs[@]}"; do
#         for evalperiod in "${EVALPERIODs[@]}"; do
#             for rcp_type in "${RCP_TYPEs[@]}"; do
#                 python plot_indicators.py -g "png" -e $evalperiod -t $vartype -i $indicator -r $rcp_type -m $region -l "German" -s "ensmedian"
#             done
#             # python join_tables.py -i $indicator -e $evalperiod -t $vartype -s "ensemble"
#             # python join_tables.py -i $indicator -e $evalperiod -t $vartype -s "spatial"
#         done
#     done
# done
