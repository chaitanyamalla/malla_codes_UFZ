#!/bin/bash
# --------------------------------------------------
#  File:        send_files.sh
#
#  Created:     Mo 13-05-2022
#  Author:      Chaitanya Malla
#
# --------------------------------------------------
#
#  Description: script to upload files directly to nextcloud
#
#  Modified:
#
# --------------------------------------------------
#git clone https://github.com/tavinus/cloudsend.sh.git

#find ./  -maxdepth 1 -type f -exec ./cloudsend.sh/cloudsend.sh {} https://nc.ufz.de/f/137014242 -p  downscaling \;

#link_plots="https://nc.ufz.de/s/Sy4HF8yQkTG6CMH"
link_plots="https://nc.ufz.de/apps/files/?dir=/Shared%20with%20me/wis_d_dvgw_indicators/TP2/Plots_pre_percentiles/pre_gt_perc&fileid=137014242"


# find ./tables_periods/*ensmedian*germany*csv -type f -exec ./cloudsend {} "${link_tables}" -p wis-d_data \;
#find ./plots_periods/*aET* -type f -exec ./cloudsend {} "${link_plots}" -p wis-d_data \;
#find ./plots_periods/*PET* -type f -exec ./cloudsend {} "${link_plots}" -p wis-d_data \;
#find ./plots_periods/*pre* -type f -exec ./cloudsend {} "${link_plots}" -p wis-d_data \;
pass="9290A!()"

curl -X PUT -u malla:$pass $link_plots -T ./plots_periods/*pre*
