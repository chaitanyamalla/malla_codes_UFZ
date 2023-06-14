ml Anaconda3
source activate /global/apps/klimabuero/conda_py3.9.2/

set -e
set -x


# follow steps under:
# https://wiki.ufz.de/eve/index.php/Archiving


#  -- tar data -------------------------------------



# tar_file="pre.tar.gz"
# tar_path="\/data\/duerre\/GDM_v2_statbase\/01_interpolation\/1947-2019\/pre\/"
# sbatch /global/submit-archive.sh /work/$USER/data [/path/to/archive.tar.gz]
# template_file="job_edk_pre.template"
# job_file="job_edk_pre.import"
# cp $template_file $job_file
# sed -i -e "s|@SOURCE_PATH@|${tar_path}|g" $job_file
# sed -i -e "s|@SOURCE_FILE@|${tar_file}|g" $job_file


# tar_file="tavg.tar.gz"
# tar_path="/data/duerre/GDM_v2_statbase/01_interpolation/1947-2019/tavg/"
# sbatch /global/submit-archive.sh ${tar_path} ${tar_path}/${tar_file}
# template_file="job_edk_tavg.template"
# job_file="job_edk_tavg.import"
# cp $template_file $job_file
# sed -i -e "s|@SOURCE_PATH@|${tar_path}|g" $job_file
# sed -i -e "s|@SOURCE_FILE@|${tar_file}|g" $job_file



# tar_file="tmin.tar.gz"
# tar_path="/data/duerre/GDM_v2_statbase/01_interpolation/1947-2019/tmin/"
# sbatch /global/submit-archive.sh ${tar_path} ${tar_path}/${tar_file}
# template_file="job_edk_tmin.template"
# job_file="job_edk_tmin.import"
# cp $template_file $job_file
# sed -i -e "s|@SOURCE_PATH@|${tar_path}|g" $job_file
# sed -i -e "s|@SOURCE_FILE@|${tar_file}|g" $job_file



# tar_file="tmax.tar.gz"
# tar_path="/data/duerre/GDM_v2_statbase/01_interpolation/1947-2019/tmax/"
# sbatch /global/submit-archive.sh ${tar_path} ${tar_path}/${tar_file}
# template_file="job_edk_tmax.template"
# job_file="job_edk_tmax.import"
# cp $template_file $job_file
# sed -i -e "s|@SOURCE_PATH@|${tar_path}|g" $job_file
# sed -i -e "s|@SOURCE_FILE@|${tar_file}|g" $job_file


# files=("mHM_run_GDM_DE1") # "mHM_run_GDM_DE2"  "mHM_run_GDM_DE3") # 

# for c in "${files[@]}"; do
#     tar_file="${c}.tar.gz"
#     tar_path="/data/duerre/GDM_v2_statbase/02_mHM_runs/02_daily_runs/${c}/"
#     #result_path="/data/duerre/GDM_v2_statbase/backup/${c}"
#     result_path="/work/malla/GDM/GDM_v2_statbase/backup/${c}"

#     sbatch /global/submit-archive.sh ${tar_path} ${result_path}/${tar_file}
#     template_file="job_mhm.template"
#     job_file="job_${c}.import"
#     cp $template_file $result_path/$job_file
#     sed -i -e "s|@SOURCE_PATH@|${result_path}|g" $result_path/$job_file
#     sed -i -e "s|@SOURCE_FILE@|${tar_file}|g" $result_path/$job_file
# done


# tar_file="pet.tar.gz"
# tar_path="/data/duerre/GDM_v2_statbase/01_interpolation/1947-2019/pet_fao56/pet/"
# result_path="/work/malla/GDM/GDM_v2_statbase/backup/pet"
# sbatch /global/submit-archive.sh ${tar_path} ${result_path}/${tar_file}
# template_file="job_edk.template"
# job_file="job_edk_pet.import"
# cp $template_file $result_path/$job_file
# sed -i -e "s|@SOURCE_PATH@|${result_path}|g" $result_path/$job_file
# sed -i -e "s|@SOURCE_FILE@|${tar_file}|g" $result_path/$job_file




#####################-------------- SMI_GDM_DE1 ---------------------
# tail="GDM_DE1"
# files=("SM_0_25cm_runmean14" "SM_0_60cm_runmean14" "SM_25_60cm_runmean14" "SM_5_25cm_runmean14" "SM_Lall_runmean14" "SM_0_25cm_runmean30" "SM_0_60cm_runmean30" "SM_25_60cm_runmean30" "SM_5_25cm_runmean30" "SM_Lall_runmean30")
# for c in "${files[@]}"; do
#     tar_file="${c}_${tail}.tar.gz"
#     tar_path="/data/duerre/GDM_v2_statbase/03_SMI/SMI_GDM_DE1/output_cropped/${c}/"
#     result_path="/work/malla/GDM/GDM_v2_statbase/backup/03_SMI/SMI_GDM_DE1/${c}/"
#     sbatch /global/submit-archive.sh ${tar_path} ${result_path}${tar_file}
#     template_file="job_smi.template"
#     job_file="job_${c}.import"
#     cp $template_file $result_path/$job_file
#     sed -i -e "s|@SOURCE_PATH@|${result_path}|g" $result_path/$job_file
#     sed -i -e "s|@SOURCE_FILE@|${tar_file}|g" $result_path/$job_file
# done
# ### --------------------------------------------------------------------



#####################-------------- SMI_GDM_DE2 ---------------------
# tail="GDM_DE2"
# files=("SM_0_30cm_runmean30" "SM_Lall_runmean30")
# for c in "${files[@]}"; do
#     tar_file="${c}_${tail}.tar.gz"
#     tar_path="/data/duerre/GDM_v2_statbase/03_SMI/SMI_GDM_DE2/output_cropped/${c}/"
#     result_path="/work/malla/GDM/GDM_v2_statbase/backup/03_SMI/SMI_GDM_DE2/${c}/"
#     sbatch /global/submit-archive.sh ${tar_path} ${result_path}${tar_file}
#     template_file="job_smi.template"
#     job_file="job_${c}.import"
#     cp $template_file $result_path/$job_file
#     sed -i -e "s|@SOURCE_PATH@|${result_path}|g" $result_path$job_file
#     sed -i -e "s|@SOURCE_FILE@|${tar_file}|g" $result_path$job_file
# done
# ### --------------------------------------------------------------------


#####################-------------- SMI_GDM_DE3 ---------------------
tail="GDM_DE3"
files=("SM_0_30cm_runmean30" "SM_Lall_runmean30")
for c in "${files[@]}"; do
    tar_file="${c}_${tail}.tar.gz"
    tar_path="/data/duerre/GDM_v2_statbase/03_SMI/SMI_${tail}/output_cropped/${c}/"
    result_path="/work/malla/GDM/GDM_v2_statbase/backup/03_SMI/SMI_${tail}/${c}/"
    sbatch /global/submit-archive.sh ${tar_path} ${result_path}${tar_file}
    template_file="job_smi.template"
    job_file="job_${c}_${tail}.import"
    cp $template_file $result_path/$job_file
    sed -i -e "s|@SOURCE_PATH@|${result_path}|g" $result_path$job_file
    sed -i -e "s|@SOURCE_FILE@|${tar_file}|g" $result_path$job_file
done
### --------------------------------------------------------------------
