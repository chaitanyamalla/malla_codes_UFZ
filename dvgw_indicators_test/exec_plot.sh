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

region="de_hicam"

echo "Note that do_main_catch_ger and grid (2x2) has to be set on in script!"


# VARTYPEs=("abs-abs_change" "abs_change")
# VARTYPEs=("abs_change")
# VARTYPEs=("abs-abs_change")
# for vartype in "${VARTYPEs[@]}"; do
#     for rcp_type in "${RCP_TYPEs[@]}"; do
#         python plot_indicators.py -g png -e "year" -t $vartype -i "n_heatdays" -r $rcp_type -m $region -l "German" -s "ensmedian"
#         python plot_indicators.py -g png -e "year" -t $vartype -i "n_summerdays" -r $rcp_type -m $region -l "German" -s "ensmedian"
#         python plot_indicators.py -g png -e "year" -t $vartype -i "n_consec_heatdays" -r $rcp_type -m $region -l "German" -s "ensmedian"
#         python plot_indicators.py -g png -e "year" -t $vartype -i "n_consec_summerdays" -r $rcp_type -m $region -l "German" -s "ensmedian"
#     done
#     python join_tables.py -i "n_heatdays" -e "year" -t $vartype
#     python join_tables.py -i "n_summerdays" -e "year" -t $vartype
#     python join_tables.py -i "n_consec_heatdays" -e "year" -t $vartype
#     python join_tables.py -i "n_consec_summerdays" -e "year" -t $vartype

# done
#     #  -- calculate seasonal and yearly ---------------------------
    
#VARTYPEs=("abs")
VARTYPEs=("abs_change" "rel_change") #"abs" 
#VARTYPEs=("abs-abs_change") # "abs-rel_change")
#VARTYPEs=("abs_change")
for vartype in "${VARTYPEs[@]}"; do
    #EVALPERIODs=("summer" "winter" "spring" "autumn" "year")
    EVALPERIODs=("year")
    #INDICATORs=("tavg_mean" "recharge_adjust_sum")
    #INDICATORs=("recharge_adjust_sum")
    #INDICATORs=("pre_gt0p1_R90p" "pre_gt0p1_R95p" "pre_gt0p1_R99p" "pre_gt1_R90p" "pre_gt1_R95p" "pre_gt1_R99p")
    INDICATORs=("pre_gt1_R95p" "pre_gt1_R99p") #"pre_gt1_R90p" 
    for indicator in "${INDICATORs[@]}"; do
        for evalperiod in "${EVALPERIODs[@]}"; do
            for rcp_type in "${RCP_TYPEs[@]}"; do
                python plot_indicators.py -g png -e $evalperiod -t $vartype -i $indicator -r $rcp_type -m $region -l "German" -s "ensmedian"
            done
            # python join_tables.py -i $indicator -e $evalperiod -t $vartype
        done
    done
done
# VARTYPEs=("abs-abs_change" "abs_change")
# VARTYPEs=("abs_change")
# VARTYPEs=("abs-abs_change")
# for vartype in "${VARTYPEs[@]}"; do
#     EVALPERIODs=("year")
#     INDICATORs=("recharge_adjust_20perc_avg")
#     for indicator in "${INDICATORs[@]}"; do
#         for evalperiod in "${EVALPERIODs[@]}"; do
#             for rcp_type in "${RCP_TYPEs[@]}"; do
#                 python plot_indicators.py -g png -e $evalperiod -t $vartype -i $indicator -r $rcp_type -m $region -l "German" -s "ensmedian"
#             done
#             python join_tables.py -i $indicator -e $evalperiod -t $vartype
#         done
#     done
# done

# VARTYPEs=("abs-rel_change" "rel_change")
# VARTYPEs=("rel_change")
# VARTYPEs=("abs-rel_change")
# for vartype in "${VARTYPEs[@]}"; do
#     EVALPERIODs=("summer" "winter" "spring" "autumn" "year")
#     INDICATORs=("pre_sum" "recharge_adjust_sum")
#     for indicator in "${INDICATORs[@]}"; do
#         for evalperiod in "${EVALPERIODs[@]}"; do
#             for rcp_type in "${RCP_TYPEs[@]}"; do
#                 python plot_indicators.py -g png -e $evalperiod -t $vartype -i $indicator -r $rcp_type -m $region -l "German" -s "ensmedian"
#             done
#             python join_tables.py -i $indicator -e $evalperiod -t $vartype
#         done
#     done
#     EVALPERIODs=("year")
#     INDICATORs=("recharge_adjust_20perc_avg")
#     for indicator in "${INDICATORs[@]}"; do
#         for evalperiod in "${EVALPERIODs[@]}"; do
#             for rcp_type in "${RCP_TYPEs[@]}"; do
#                 python plot_indicators.py -g png -e $evalperiod -t $vartype -i $indicator -r $rcp_type -m $region -l "German" -s "ensmedian"
#             done
#             python join_tables.py -i $indicator -e $evalperiod -t $vartype
#         done
#     done
# done

# # VARTYPEs=("abs-abs_change" "abs_change" "abs-rel_change")
# # # VARTYPEs=("abs_change")
# # VARTYPEs=("abs-abs_change")
# # VARTYPEs=("abs-rel_change")
# # VARTYPEs=("rel_change")
# # # VARTYPEs=("abs_change")
# # region="de_hicam"
# # for vartype in "${VARTYPEs[@]}"; do
# #     EVALPERIODs=("year" "veg4-6" "veg4-10" "veg7-9")
# #     INDICATORs=("n_droughtdays_0_30cm")
# #     for indicator in "${INDICATORs[@]}"; do
# #         for evalperiod in "${EVALPERIODs[@]}"; do
# #             for rcp_type in "${RCP_TYPEs[@]}"; do
# #                 python plot_indicators.py -g png -e $evalperiod -t $vartype -i $indicator -r $rcp_type -m $region -l "German"
# #             done
# #             # python join_tables.py -i $indicator -e $evalperiod -t $vartype
# #         done
# #     done
# # done
