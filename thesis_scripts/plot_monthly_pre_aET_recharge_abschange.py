#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:        plot_monthly_pre_aET_recharge_abschange.py 
#
#  Created:     Mo 18-02-2022 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description:  script to produce monthlyplots of pre aET recharge with absolute change values. 
#
#  Modified by: 
#  Modified date: 
#

import os
import ufz
from ufz import fread,readnc, position, get_brewer, abc2plot, astr 
import xarray as xr
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.gridspec as gridspec #chnage size between subplots

import geopandas as gpd
import palettable as pb
import seaborn as sns
plt.rcParams['font.size'] = '20'


inpath=("/work/malla/sachsen_output/monthly/")
outpath=("/work/malla/sachsen_output/monthly/plots_median_new/")


data= pd.read_csv(inpath+"pre_aET_rech_abs_change_monthly.csv")


#########################################################################
###---------------------------barplot-------------------------------------
w= 0.15
x=data.index
labels=data.month
#x = np.arange(len(labels))

fig, (ax1, ax2,ax3) = plt.subplots(3,1,figsize=(20,24),sharex=True) 

################------------pre---------------------
d = ax1.bar(x+0.2, data["pre_3K"], label="3 °C" ,width=w, color = "#867AE9")
c = ax1.bar(x + w/2, data["pre_2K"], label="2 °C" ,width=w,color = "#C449C2")
b = ax1.bar(x - w/2, data["pre_1_5K"], label="1.5 °C" ,width=w,color = "#BEAEE2")

ax1.set_xticks(x)
ax1.set_xticklabels(labels)
#ax1.set_xlabel("Month")
ax1.set_ylabel("pre [mm/month]")
ax1.set_title("Precipitation (absolute change)")
ax1.legend()

###############--------------aET-------------------
d = ax2.bar(x + 0.2, data["aET_3K"], label="3 °C" ,width=w, color = "#C34E20")
c = ax2.bar(x + w/2, data["aET_2K"], label="2 °C" ,width=w,color = "#D59044")
b = ax2.bar(x - w/2, data["aET_1_5K"], label="1.5 °C" ,width=w,color = "#DFBD42")
ax2.set_xticks(x)
ax2.set_xticklabels(labels)
#ax1.set_xlabel("Month")
ax2.set_ylabel("aET [mm/month]")
ax2.set_title("Actual Evapotranspiration (absolute change)")
ax2.legend()

#############---------------------recharge----------
d = ax3.bar(x + 0.2, data["rech_3K"], label="3 °C" ,width=w, color = "#10732E")
c = ax3.bar(x + w/2, data["rech_2K"], label="2 °C" ,width=w,color = "#5AC219")
b = ax3.bar(x - w/2, data["rech_1_5K"], label="1.5 °C" ,width=w,color = "#CBD83F")

ax3.set_xticks(x)
ax3.set_xticklabels(labels)
ax3.set_xlabel("Month")
ax3.set_ylabel("Recharge [mm/month]")
ax3.set_title("Recharge (absolute change)")
ax3.legend()

ax1.set_ylim([0,12])
ax2.set_ylim([0,12])
ax3.set_ylim([0,12])



plt.savefig(outpath+"plot_pre_aET_rech_abschange_monthly.png")
plt.show()
