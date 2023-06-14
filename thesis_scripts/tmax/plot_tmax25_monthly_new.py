#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:        plot_tmax25_monthly.py 
#
#  Created:     Mo 27-09-2021 
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

ind = "tmax"

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
    #da11=da1.iloc[:9]
    return(da1)


d0= read("ensmedian_monthly_summerdays_"+ind+"_historic.nc") 
d1= read("ensmedian_monthly_summerdays_"+ind+"_1_5K.nc")
d2= read("ensmedian_monthly_summerdays_"+ind+"_2K.nc")
d3= read("ensmedian_monthly_summerdays_"+ind+"_3K.nc")

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

data1_rel.iloc[[1,2,3,-1,-2,-3,]]=np.nan
data2_rel.iloc[[1,2,3,-1,-2,-3,]]=np.nan
data3_rel.iloc[[1,2,3,-1,-2,-3,]]=np.nan
#########################################################################
#---------------------------barplot-------------------------------------
w= 0.15
labels=data_3.index
x = np.arange(len(labels))

fig, (ax, ax1) = plt.subplots(2,1,figsize=(20,16),sharex=True)
d = ax.bar(x + 0.2, data_3["3K"], label="3 °C" ,width=w, color = "#FF5733")
c = ax.bar(x + w/2, data_2["2K"], label="2 °C" ,width=w,color = "#4A5ABF")
b = ax.bar(x - w/2, data_1["1_5K"], label="1.5 °C" ,width=w,color = "#39A20C")
a = ax.bar(x - 0.2, data_hist.historic, label="historic",width=w, color = "#48E9DA" )
ax.set_xticks(x)
ax.set_xticklabels(labels)
#ax.set_xlabel("Month")
ax.set_ylabel("Summerdays [n/month]")
ax.set_title("Summerdays tmax>25 °C (absolute values)")
ax.legend()


########--------------------abs change bar plot#--------------------------

d = ax1.bar(x + 0.2, data3_abs["3K"], label="3 °C" ,width=w, color = "#B0326B")
c = ax1.bar(x + w/2, data2_abs["2K"], label="2 °C" ,width=w,color = "#D136F2")
b = ax1.bar(x - w/2, data1_abs["1_5K"], label="1.5 °C" ,width=w,color = "#F86FDE")


ax1.set_xticks(x)
ax1.set_xticklabels(labels)
ax1.set_xlabel("Month")
ax1.set_ylabel("Summerdays [n/month]")
ax1.set_title("Summerdays (absolute change)")
#plt.legend()
ax1.legend()

########--------------------rel change bar plot#--------------------------

# d = ax2.bar(x + 0.2, data3_rel["3K"], label="3 °C" ,width=w, color = "#CD3717")
# c = ax2.bar(x + w/2, data2_rel["2K"], label="2 °C" ,width=w,color = "#E88552")
# b = ax2.bar(x - w/2, data1_rel["1_5K"], label="1.5 °C" ,width=w,color = "#D85B9D")
# ax2.set_xticks(x)
# ax2.set_xticklabels(labels)
# ax2.set_xlabel("Month")
# ax2.set_ylabel("Summerdays [%]")
# ax2.set_title("Summerdays (relative change)")

# ax2.legend()




plt.savefig(outpath+ind+"/"+ind+"25_all3_monthly_new.png")
plt.show()
res_abs= data1_abs.join([data2_abs,data3_abs])
res_rel= data1_rel.join([data2_rel,data3_rel])

res_abs.to_csv(outpath+ind+"/"+ind+"25_abs_change_monthly_new.csv")
res_rel.to_csv(outpath+ind+"/"+ind+"25_rel_change_monthly_new.csv")

#res_abs=res_abs.replace(res_abs.iloc[3], np.NaN)
print(res_rel,res_abs)
