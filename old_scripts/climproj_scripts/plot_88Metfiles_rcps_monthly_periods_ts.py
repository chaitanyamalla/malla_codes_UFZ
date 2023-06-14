#! /usr/bin/env python
# -*- coding: utf-8 -*-




# --------------------------------------------------
#  File:        plot_88Metfiles_rcps_monthly_periods_ts.py
#
#  Created:     Fr 04-06-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: plotting  Monthly Timeseries for different climate periods 1971-2000, 2021-2050, 2071-2099 for all 88 MET files with RCPS with pet/aET
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------
import os
import ufz
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import matplotlib.patches as patches

inpath= "/work/malla/ww_leipzig/data_1971_2099/output_1971_2099/88_METfiles_csv/88MetfilesMonthly_clim_periods_csv/"


time1 = "_1971_2000_"
time2 = "_2021_2050_"
time3 = "_2071_2099_"

indicator1= "pet"
pet_file1 = pd.read_csv(inpath + indicator1 + time1+ "months_allMetfiles.csv")
pet_file1 = pet_file1.set_index("month")
pet_file2 = pd.read_csv(inpath + indicator1 + time2+ "months_allMetfiles.csv")
pet_file2 = pet_file2.set_index("month")
pet_file3 = pd.read_csv(inpath + indicator1 + time3+ "months_allMetfiles.csv")
pet_file3 = pet_file3.set_index("month")


indicator2= "aET"
aET_file1 = pd.read_csv(inpath + indicator2 + time1+ "months_allMetfiles.csv")
aET_file1 = aET_file1.set_index("month")
aET_file2 = pd.read_csv(inpath + indicator2 + time2+ "months_allMetfiles.csv")
aET_file2 = aET_file2.set_index("month")
aET_file3 = pd.read_csv(inpath + indicator2 + time3+ "months_allMetfiles.csv")
aET_file3 = aET_file3.set_index("month")


time1= aET_file1.div(pet_file1)
time2= aET_file2.div(pet_file2)
time3= aET_file3.div(pet_file3)


############-----------RCPS---------#############
meta = pd.read_csv("/work/malla/ww_leipzig/MET_list.txt",sep=" ")
met_ids = np.sort(pd.unique(meta["met_id"]))
gcms = np.sort(pd.unique(meta["gcm"]))
rcms = np.sort(pd.unique(meta["inst.rcm"]))
rcps = pd.Series(meta["rcp"], dtype="category")
hms= ['mHM']
rcp = pd.DataFrame(rcps, columns = ['rcp'])
#-----------------------------------------------#


t1 = time1.T.reset_index()
t1_rcp= t1.join(rcp)
t1_rcp26 = t1_rcp.loc[t1_rcp['rcp'] == 'rcp26']
t1_rcp45 = t1_rcp.loc[t1_rcp['rcp'] == 'rcp45']
t1_rcp85 = t1_rcp.loc[t1_rcp['rcp'] == 'rcp85']

time1_rcp26 = t1_rcp26.drop(columns=["rcp"]).set_index("index").T.mean(axis= 1)
time1_rcp45 = t1_rcp45.drop(columns=["rcp"]).set_index("index").T.mean(axis= 1)
time1_rcp85 = t1_rcp85.drop(columns=["rcp"]).set_index("index").T.mean(axis= 1)



t2 = time2.T.reset_index()
t2_rcp= t2.join(rcp)
t2_rcp26 = t2_rcp.loc[t1_rcp['rcp'] == 'rcp26']
t2_rcp45 = t2_rcp.loc[t1_rcp['rcp'] == 'rcp45']
t2_rcp85 = t2_rcp.loc[t1_rcp['rcp'] == 'rcp85']

time2_rcp26 = t2_rcp26.drop(columns=["rcp"]).set_index("index").T.mean(axis= 1)
time2_rcp45 = t2_rcp45.drop(columns=["rcp"]).set_index("index").T.mean(axis= 1)
time2_rcp85 = t2_rcp85.drop(columns=["rcp"]).set_index("index").T.mean(axis= 1)


t3 = time3.T.reset_index()
t3_rcp= t3.join(rcp)
t3_rcp26 = t3_rcp.loc[t1_rcp['rcp'] == 'rcp26']
t3_rcp45 = t3_rcp.loc[t1_rcp['rcp'] == 'rcp45']
t3_rcp85 = t3_rcp.loc[t1_rcp['rcp'] == 'rcp85']

time3_rcp26 = t3_rcp26.drop(columns=["rcp"]).set_index("index").T.mean(axis= 1)
time3_rcp45 = t3_rcp45.drop(columns=["rcp"]).set_index("index").T.mean(axis= 1)
time3_rcp85 = t3_rcp85.drop(columns=["rcp"]).set_index("index").T.mean(axis= 1)

month = time3_rcp26.index.astype(str)



fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15,6))
ax1.set_title("RCP26")
ax1.plot(month, time1_rcp26, label="1971-2000",linestyle='dashed',color = "#666261" )#"#359734" )
ax1.plot(month, time2_rcp26, label="2021-2050", color = "#F0810B")#"#0E52E3")
ax1.plot(month, time3_rcp26, label="2071-2099", color = "#B81C17")# "#EC6B4F")
ax1.set_ylabel("aET/pet")
ax1.set_xlabel("Months")
ax1.set_ylim(0.6, 0.85)
#ax1.set_facecolor('xkcd:salmon')
#ax1.patch.set_facecolor('#7CE98A')
#ax1.patch.set_alpha(0.25)
ax1.legend(loc='lower left')
#ax1.grid(True)

ax2.set_title("RCP45")
ax2.plot(month, time1_rcp45, label="1971-2000",linestyle='dashed', color = "#666261")#"#359734")
ax2.plot(month, time2_rcp45, label="2021-2050", color = "#F0810B")#"#0E52E3")
ax2.plot(month, time3_rcp45, label="2071-2099", color ="#B81C17")#"#EC6B4F")
ax2.set_ylim(0.6, 0.85)
#ax2.set_ylabel("aET/pet")
ax2.set_xlabel("Months")
#ax2.patch.set_facecolor('#9DF0F5')
#ax2.patch.set_alpha(0.35)
ax2.legend(loc='lower left')
#ax2.grid(True)


ax3.set_title("RCP85")
ax3.plot(month, time1_rcp85, label="1971-2000",linestyle='dashed', color = "#666261")#"#359734")
ax3.plot(month, time2_rcp85, label="2021-2050", color = "#F0810B")# "#0E52E3")
ax3.plot(month, time3_rcp85, label="2071-2099", color ="#B81C17")#"#EC6B4F")
ax3.set_ylim(0.6, 0.85)
#ax3.set_ylabel("aET/pet")
ax3.set_xlabel("Months")
#ax3.patch.set_facecolor('#E7863F')
#ax3.patch.set_alpha(0.25)
ax3.legend(loc='lower left')
#ax3.grid(True)

#ax1.xaxis.set_major_locator(MultipleLocator())
# # #ax.xaxis.set_major_formatter('{x:.0f}')
# ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
# ax1.tick_params(which='minor', length=5)
# ax1.tick_params(which='major', length=9)

# #ax2.xaxis.set_major_locator(MultipleLocator(10))
# # #ax.xaxis.set_major_formatter('{x:.0f}')
# ax2.xaxis.set_minor_locator(AutoMinorLocator(1))
# ax2.tick_params(which='minor', length=5)
# ax2.tick_params(which='major', length=9)

# #ax3.xaxis.set_major_locator(MultipleLocator(10))

# # #ax.xaxis.set_major_formatter('{x:.0f}')
# ax3.xaxis.set_minor_locator(AutoMinorLocator(1))
# ax3.tick_params(which='minor', length=5)
# ax3.tick_params(which='major', length=9)


plt.legend()
plt.show()

#plt.savefig(inpath + "plot_periods_with_RCPS_" + "88Models_monthly_ts_plain.png" )
