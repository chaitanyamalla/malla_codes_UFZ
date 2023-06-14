#!/bin/bash
#set -e
#set -x



path_in="/data/hicam/data/processed/mhm_output/de_hicam/v2_climproj/calib151/"
types="output_daily/"

path_out="/work/malla/GDM/mHM_output_daily/mets/"

met_START=1
met_END=1
#mets=$(seq -f "%03g" 1 2)  #" "$(seq -f "%03g" 7 15)
mets=$(seq -f "%03g" 1 4)" "$(seq -f "%03g" 7 15)" "$(seq -f "%03g" 21 32)" "$(seq -f "%03g" 35 45)" "$(seq -f "%03g" 50 62)" "$(seq -f "%03g" 67 80)" "$(seq -f "%03g" 82 88)

cordex_list="/work/malla/GDM/mHM_output_daily/88_main_LUT_WL.txt"


cd $path_out

for t in $mets; do

    met="met_${t}"
    echo "$met"
    if [ ! -d $met ]; then
	mkdir $met
    fi
    
    cd $met




    tar_file="${met}.tar.gz"
    tar_path="${path_in}${met}/${types}"
    result_path="${path_out}${met}/"
    #sbatch /global/submit-archive.sh ${tar_path} ${result_path}${tar_file}

    template_file="daily_mets.template"
    job_file="job_mHM_output_daily_${met}.import"
    cp /work/malla/GDM/mHM_output_daily/$template_file $result_path$job_file
    sed -i -e "s|@SOURCE_PATH@|${result_path}|g" $result_path$job_file
    sed -i -e "s|@SOURCE_FILE@|${tar_file}|g" $result_path$job_file
    #sed -i -e "s|@ENSNUM@|${t}|g" $result_path$job_file



    while IFS= read -r line; do
	if [[ $line == *"$met"* ]]; then
            GCM=$(echo "$line" | awk '{print $4}')
	    RCP=$(echo "$line" | awk '{print $5}')
	    realization=$(echo "$line" | awk '{print $6}')
	    inst_rcm=$(echo "$line" | awk '{print $7}')
	    
            break  # Uncomment this line if you want to exit after finding the first occurrence
	fi
done < "$cordex_list"

    echo "GCM: ${GCM} ${RCP} ${realization} ${inst_rcm}"

    sed -i -e "s|@ENSNUM@|${t} ${GCM} ${RCP} ${realization} ${inst_rcm}|g" $result_path$job_file

    
    cd ..



done





    
# cat > submit.sh <<EOF
# #!/bin/bash

# #SBATCH -J ${met}_daily_mHM_fluxes_zipped
# #SBATCH -o ./%x-%j.log
# #SBATCH -t 0-10:00:00
# #SBATCH --cpus-per-task=4
# #SBATCH --mem-per-cpu=8G
# #SBATCH --mail-user=chaitanya.malla@ufz.de
# #SBATCH --mail-type=BEGIN,END,FAIL
# #SBATCH --output=./%x-%A-%a.out
# #SBATCH --error=./%x-%A-%a.err

# #  -- load software --------------------------------
# ml purge
# ml foss/2019b texlive #load texlive for plotting    
# ml Anaconda3    
# source activate /global/apps/klimabuero/conda_py3.9.2/

# cdo -f nc4c -z zip_4 pack $path_in${met}/${types}${file_name} $path_out${met}/${file_name}

# EOF
#    
#echo "submitting job"
#sbatch submit.sh
