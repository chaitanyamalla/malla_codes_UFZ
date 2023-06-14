#!/bin/bash

#SBATCH -J pre_ext_perc
#SBATCH -o ./%x-%j.log
#SBATCH -t 0-1:00:00
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-user=chaitanya.malla@ufz.de
#SBATCH --mail-type=BEGIN,END
#SBATCH --output=./%x-%A-%a.out
#SBATCH --error=./%x-%A-%a.err

# -*- coding: utf-8 -*-

ml purge # removes all activated modules
ml Anaconda3 # loads Anaconda
source activate /global/apps/klimabuero/conda_py3.9.2/

# --------------------------------------------------
#  File:        producing_indicator.sh
#
#  Created:     Mi 12.01.2022
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce indicators with different timeperiods  for all METs for Germany
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------


set -x
set -e
# set type of processing (either as cluster job with manual or automatic job submission or directly on terminal) 
interactive=false # execute processing directly in script
manual=false # submit sbatch jobs manually

slurm_runtime="0-15:00:00"
slurm_mail="chaitanya.malla@ufz.de"

slurm_mem_per_cpu="4G"

##########---------------------path variables--------------------------------------------------------
path_int="/data/hicam/data/processed/meteo/germany/climproj/euro-cordex/88realizations_mhm/"
path_out="/work/malla/meteo_germany/extreme_precip/data1_with_intermediate/"

maskfile="/data/hicam/data/processed/dem_OR/mask_hicam_1km_g_inv.nc"


met_START=1
met_END=88

#mets=$(seq -f "%03g" 1 4)" "$(seq -f "%03g" 7 15)" "$(seq -f "%03g" 21 32)" "$(seq -f "%03g" 35 45)" "$(seq -f "%03g" 50 62)" "$(seq -f "%03g" 67 80)" "$(seq -f "%03g" 82 88)

cd $path_out



for t in $(seq -f "%03g" $met_START $met_END); do
#for t in $mets;do
    met="met_${t}/"
    echo "$met"

    if [[ ! -d $met ]]; then
        mkdir $met
    fi


    cd $met

    cat > execute.sh <<EOF
    set -e
    set -x

    perc=("90" "95" "99")
    PERIOD_start=("1971" "2021" "2036" "2069")    ##
    PERIOD_end=("2000" "2050" "2065" "2098")      ## 

    i=0
    for p_start in "\${PERIOD_start[@]}"; do
        p_end="\${PERIOD_end[\$i]}"
        echo "evaluate period \${p_start} - \${p_end}"
        i=\$((\$i + 1))

    	###-------pre_yearly--------###
    	# cdo -timmean -yearsum -gtc,10 -selyear,$p_start/$p_end ${path_int}${met}/pre.nc ${path_out}${met}/pre_yearly_${p_start}_${p_end}_gtc10_ysum_timmean.nc
    	# maskfile="/data/hicam/data/processed/dem_OR/mask_hicam_1km_g_inv.nc"
    	# cdo -O merge ${path_out}${met}/tmp1_pre_yearly.nc ${maskfile} ${path_out}${met}/tmp2_pre_yearly.nc
    	# cdo_expr="pre=(mask==0)?-9999:pre" 
        # cdo expr,$cdo_expr ${path_out}${met}/tmp2_pre_yearly.nc ${path_out}${met}/pre_yearly_${p_start}_${p_end}_gtc10_ysum_timmean.nc
    	# cdo fldpctl,50 ${path_out}${met}/pre_yearly_${p_start}_${p_end}_gtc10_ysum_timmean.nc ${path_out}${met}/pre_yearly_${p_start}_${p_end}_gtc10_ysum_timmean_fldpctl.nc
	# cdo -timmean -yearsum -gtc,20 -selyear,$p_start/$p_end ${path_int}${met}/pre.nc ${path_out}${met}/pre_yearly_${p_start}_${p_end}_gtc20_ysum_timmean.nc
		
	# cdo -timpctl,90 -setmissval,-9999.9 -selyear,$p_start/$p_end ${path_int}${met}/pre.nc -timmin -setmissval,-9999.9 -selyear,$p_start/$p_end ${path_int}${met}/pre.nc -timmax -setmissval,-9999.9 -selyear,$p_start/$p_end ${path_int}${met}/pre.nc ${path_out}${met}/pre_yearly_${p_start}_${p_end}_R90p.nc

	# cdo -timpctl,95 -setmissval,-9999.9 -selyear,$p_start/$p_end ${path_int}${met}/pre.nc -timmin -setmissval,-9999.9 -selyear,$p_start/$p_end ${path_int}${met}/pre.nc -timmax -setmissval,-9999.9 -selyear,$p_start/$p_end ${path_int}${met}/pre.nc ${path_out}${met}/pre_yearly_${p_start}_${p_end}_R95p.nc

	# cdo -timpctl,99 -setmissval,-9999.9 -selyear,$p_start/$p_end ${path_int}${met}/pre.nc -timmin -setmissval,-9999.9 -selyear,$p_start/$p_end ${path_int}${met}/pre.nc -timmax -setmissval,-9999.9 -selyear,$p_start/$p_end ${path_int}${met}/pre.nc ${path_out}${met}/pre_yearly_${p_start}_${p_end}_R99p.nc


   
    # rm -f tmp*

	for p in \${perc[@]}; do

            cdo -setrtomiss,0,0.1 -selyear,\$p_start/\$p_end ${path_int}${met}pre.nc temp1_\${p_start}_\${p_end}_\${p}.nc
            cdo -timpctl,\$p temp1_\${p_start}_\${p_end}_\${p}.nc -timmin temp1_\${p_start}_\${p_end}_\${p}.nc -timmax temp1_\${p_start}_\${p_end}_\${p}.nc ${path_out}${met}pre_yearly_\${p_start}_\${p_end}_gt0p1_R\${p}p.nc

            cdo -setrtomiss,0,1 -selyear,\$p_start/\$p_end ${path_int}${met}pre.nc temp2_\${p_start}_\${p_end}_\${p}.nc
            cdo -timpctl,\$p temp2_\${p_start}_\${p_end}_\${p}.nc -timmin temp2_\${p_start}_\${p_end}_\${p}.nc -timmax temp2_\${p_start}_\${p_end}_\${p}.nc ${path_out}${met}pre_yearly_\${p_start}_\${p_end}_gt1_R\${p}p.nc
 
	done
	    
	

    done
EOF
    chmod 774 execute.sh
    cat > submit_slurm.sh <<EOF
#!/bin/bash
#SBATCH -J producing_pre_extremepercentiles
#SBATCH -o ./%x-%j.log
#SBATCH -t ${slurm_runtime}
#SBATCH --mem-per-cpu=${slurm_mem_per_cpu}
##SBATCH --mail-user=${slurm_mail}
##SBATCH --mail-type=BEGIN,END
#SBATCH --output=./%x-%A-%a.out
#SBATCH --error=./%x-%A-%a.err
# ml purge # removes all activated modules
ml Anaconda3 # loads Anaconda
# activates conda environment including cdo, nco imagemagick etc
source activate /global/apps/klimabuero/conda_py3.9.2/

./execute.sh
EOF
    if [[ $interactive = true ]]; then
        ./execute.sh
    else
        # submit job with sbatch
        if [[ $manual = false ]]; then
            sbatch submit_slurm.sh
            echo "submit sbatch job!"
        else
            echo "submit sbatch manually!"
        fi
    fi


    cd ..	
done





