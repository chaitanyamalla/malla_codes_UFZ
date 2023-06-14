#!/bin/sh


# --------------------------------------------------
#  File:        exec_loop.sh
#
#  Created:     Fr 02-10-2020
#  Author:      Friedrich Boeing
#
# --------------------------------------------------
#
#  Description: creates bash script for latlon extraction
#
#  Modified:
#
# --------------------------------------------------
set -e
set -x


#  -- slurm job settings ---------------------------

rtime='05:00:00'
vmem='4G' 
mail='chaitanya.malla@ufz.de'
#mail='friedrich.boeing@ufz.de'
hmem='false'
OMP_NTHREAD='1'
interactive=false ## if true the script is executed in the command line, if false submitted to cluster
job_manual=false # if true the submit script is directly submitted to the cluster, if false not  


#  -- set data and paths ---------------------------

maindir=$(pwd)
nc_latlon="/data/hicam/data/processed/mhm_input/de_hicam/latlon/latlon_0p015625.nc"

#  -- location infile settings ---------------------

loc_outfile=""
loc_filetype=".csv"
loc_inpath="${maindir}/stations"
LOC_INFILEs=("wasserwerk")
#LOC_INFILEs=("Dahme_angepasst" "Spree_angepasst" "Plane_angepasst" "Havel_angepasst") # !!!! set to filename
write="T"

#  --  list of ensemble members --------------------
METs=("001" "025" "035" "057" "070" "083" "086") #rcp8.5
#METs=("011" "015" "032" "038" "044" "080" "088") #rcp2.6
rcp=["rcp26","rcp85"]


#METs=("001" "024" "050" "041" "075") # !!! set to core ensemble for ww leipzig

#  -- extract Qrouted or DEM -----------------------

do_dem=false



if [[ $do_dem == true ]]; then
    dem_dir="./dem"
    if [[ ! -d $dem_dir ]]; then
        mkdir $dem_dir
    fi
    cd $dem_dir

    nc_infile="/data/hicam/data/processed/dem_OR/dem_hicam_1km_g_inv.nc"
    for loc_infile in "${LOC_INFILEs[@]}"; do
        submit_script="sbatch_submit.sh"
        exec_script="exec_${loc_infile}.sh"
        cat > $submit_script <<EOF
#!/bin/bash

#SBATCH -J HICAM_data
#SBATCH -o ./%x-%j.log
#SBATCH -t $rtime
#SBATCH -c $OMP_NTHREAD
#SBATCH --mem-per-cpu=$vmem
#SBATCH --mail-user=$mail
#SBATCH --mail-type=BEGIN,END
#SBATCH --output=./%x-%A-%a.out
#SBATCH --error=./%x-%A-%a.err
./${exec_script}
EOF
        cat > $exec_script <<EOF
set -e
set -x
ml purge
ml Anaconda3
source deactivate
source activate /global/apps/klimabuero/conda_py3.9.2
python ${maindir}/00_extract_mHM_cell_ts.py -i "${nc_infile}" -o "${loc_outfile}" -c "${loc_inpath}/${loc_infile}${loc_filetype}" -w ${write} -v "" -l "${nc_latlon}"
EOF
        chmod 774 ${exec_script}
        if [[ $interactive = true ]]; then
            ./${exec_script}
        else
            if [[ $job_manual = false ]]; then
                sbatch ${submit_script}
            else
                echo "manual job submission"
            fi
        fi
    done


else
    #  -- extract Qrouted data points! -------------------------



    for met in "${METs[@]}"; do
	met_dir="met_$met"
	echo "$met_dir"
	if [[ ! -d $met_dir ]]; then
		mkdir $met_dir
	fi
	cd $met_dir
	nc_infile="/data/hicam/data/processed/mhm_output/de_hicam/v2_climproj/calib151/${met_dir}/output_daily/mRM_Fluxes_States.nc"
	for loc_infile in "${LOC_INFILEs[@]}"; do
    # for set in "${setups[@]}"; do
	    submit_script="sbatch_submit.sh"
	    exec_script="exec_${loc_infile}.sh"
	    cat > $submit_script <<EOF
#!/bin/bash

#SBATCH -J HICAM_data
#SBATCH -o ./%x-%j.log
#SBATCH -t $rtime
#SBATCH -c $OMP_NTHREAD
#SBATCH --mem-per-cpu=$vmem
#SBATCH --mail-user=$mail
#SBATCH --mail-type=BEGIN,END
#SBATCH --output=./%x-%A-%a.out
#SBATCH --error=./%x-%A-%a.err
./${exec_script}
EOF


    cat > $exec_script <<EOF
set -e
set -x
ml purge
ml Anaconda3
source deactivate
source activate /global/apps/klimabuero/conda_py3.9.2
python ${maindir}/00_extract_mHM_cell_ts.py -i "${nc_infile}" -o "${loc_outfile}" -c "${loc_inpath}/${loc_infile}${loc_filetype}" -w ${write} -v "" -l "${nc_latlon}"
EOF
    chmod 774 ${exec_script}
    if [[ $interactive = true ]]; then
        ./${exec_script}
    else
        if [[ $job_manual = false ]]; then
            sbatch ${submit_script}
        else
            echo "manual job submission"

        fi
    fi
    done
    cd ..


    done
fi
