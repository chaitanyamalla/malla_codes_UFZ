#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:        plot_pre_monthly_new.py 
#
#  Created:     Mo 06-12-2021 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description:  script to produce monthlyplots 49 RCP 8.5 MET files with single  indicator 
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
ind = "pre"

inpath=("/work/malla/sachsen_output/monthly/ens_median_monthly/")
outpath=("/work/malla/sachsen_output/monthly/plots_median_new/")

def read(filename):
    d= xr.open_dataset(inpath+ind+"/"+filename)
    return d

def process(filename, var):
    if var==0:
        k="historic"
    elif var==1:
        k="1_5K"
    elif var==2:
        k="2K"
    elif var ==3:
        k="3K"
    f=filename
    f=f.where(f>0)
    da1= f[ind].mean(dim=["latitude","longitude"]).to_dataframe(k)
    
    return(da1)

d0= read("ensmedian_monthly_"+ind+"_historic.nc") 
d1= read("ensmedian_monthly_"+ind+"_1_5K.nc")
d2= read("ensmedian_monthly_"+ind+"_2K.nc")
d3= read("ensmedian_monthly_"+ind+"_3K.nc")

data_hist= process(d0,0)
data_1= process(d1,1)
data_2= process(d2,2)
data_3= process(d3,3)

d1a = d1-d0
d2a = d2-d0
d3a = d3-d0

d1r=(d1a/d0)*100
d2r=(d2a/d0)*100
d3r=(d3a/d0)*100

data1_abs=process(d1a,1)
data2_abs=process(d2a,2)
data3_abs=process(d3a,3)
data1_rel=process(d1r,1)
data2_rel=process(d2r,2)
data3_rel=process(d3r,3)


#########################################################################
###---------------------------barplot-------------------------------------
w= 0.15
labels=data_3.index
x = np.arange(len(labels))



fig, (ax, ax1,ax2) = plt.subplots(3,1,figsize=(20,24),sharex=True)
d = ax.bar(x + 0.2, data_3["3K"], label="3 °C" ,width=w, color = "#FF5733")
c = ax.bar(x + w/2, data_2["2K"], label="2 °C" ,width=w,color = "#4A5ABF")
b = ax.bar(x - w/2, data_1["1_5K"], label="1.5 °C" ,width=w,color = "#39A20C")
a = ax.bar(x - 0.2, data_hist.historic, label="historic",width=w, color = "#48E9DA" )

ax.set_xticks(x)
ax.set_xticklabels(labels)
#ax.set_xlabel("Month")
ax.set_ylabel("pre [mm/month]")
ax.set_title("Precipitation (absolute values)")
ax.legend()
# ########--------------------abs change bar plot#--------------------------

d = ax1.bar(x+0.2, data3_abs["3K"], label="3 °C" ,width=w, color = "#867AE9")
c = ax1.bar(x + w/2, data2_abs["2K"], label="2 °C" ,width=w,color = "#C449C2")
b = ax1.bar(x - w/2, data1_abs["1_5K"], label="1.5 °C" ,width=w,color = "#BEAEE2")

ax1.set_xticks(x)
ax1.set_xticklabels(labels)
#ax1.set_xlabel("Month")
ax1.set_ylabel("pre [mm/month]")
ax1.set_title("Precipitation (absolute change)")
ax1.legend()

# ########--------------------rel change bar plot#--------------------------

d = ax2.bar(x + 0.2, data3_rel["3K"], label="3 °C" ,width=w, color = "#3D2C8D")
c = ax2.bar(x + w/2, data2_rel["2K"], label="2 °C" ,width=w,color = "#9D84B7")
b = ax2.bar(x - w/2, data1_rel["1_5K"], label="1.5 °C" ,width=w,color = "#3EDBF0")#916BBF
ax2.set_xticks(x)
ax2.set_xticklabels(labels)
ax2.set_xlabel("Month")
ax2.set_ylabel("pre [%]")
ax2.set_title("Precipitation (relative change)")
ax2.legend()



# plt.savefig(outpath+ind+"/"+ind+"_all3_monthly.png")

# plt.show()

res_abs= data1_abs.join([data2_abs,data3_abs])
res_rel= data1_rel.join([data2_rel,data3_rel])

res_abs.to_csv(outpath+ind+"/"+ind+"_abs_change_monthly.csv")
res_rel.to_csv(outpath+ind+"/"+ind+"_rel_change_monthly.csv")
print(res_abs,res_rel)
