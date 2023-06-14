#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:        plot_pet_monthly.py 
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

indicator = "pet"

inpath=("/work/malla/sachsen_output/monthly/csv/")
outpath=("/work/malla/sachsen_output/monthly/plots_median/aET_pet/")



def read(filename):
    data = pd.read_csv(filename)
    data = data.set_index("month")
    data["median"]=data.median(axis=1)
    data_mean = data["median"].to_frame("avg")
    data_mean = data_mean.reset_index()
    data_mean['month'] =  data_mean['month'].astype(str)
    return data_mean



data_hist= read(inpath+indicator+"_hist_monthly.csv")
data_1= read(inpath+indicator+"_1_5K_monthly.csv")
data_2= read(inpath+indicator+"_2K_monthly.csv")
data_3= read(inpath+indicator+"_3K_monthly.csv")

data1 = data_1.set_index("month")
data2 = data_2.set_index("month")
data3 = data_3.set_index("month")
data_hist = data_hist.set_index("month")

data1_abs = data1-data_hist
data2_abs = data2-data_hist
data3_abs = data3-data_hist

data1_rel = (data1_abs/data_hist)*100
data2_rel = (data2_abs/data_hist)*100
data3_rel = (data3_abs/data_hist)*100



# fig, ax = plt.subplots(figsize=(6,8))
# ax.plot(data_3.month, data_3.avg, label="3 °C" , color = "orange")
# ax.plot(data_2.month, data_2.avg, label="2 °C" ,color = "blue")
# ax.plot(data_1.month, data_1.avg, label="1.5 °C" ,color = "cyan")
# ax.plot(data_hist.month, data_hist.avg, label="historic", color = "green" )
# ax.set_xlabel("Month")
# ax.set_ylabel("pet [mm/month]")
# ax.set_title("Potential Evapotranspiration (absolute values)")
# plt.legend()
# #plt.show()
# plt.savefig(outpath+indicator+"_abs_monthly.png")


#########################################################################
#---------------------------barplot-------------------------------------
w= 0.15
labels=data_3.month
x = np.arange(len(labels))
# fig, ax = plt.subplots(figsize=(12,6))
fig, (ax, ax1,ax2) = plt.subplots(3,1,figsize=(20,24),sharex=True)
d = ax.bar(x + 0.2, data_3.avg, label="3 °C" ,width=w, color = "#FF5733")
c = ax.bar(x + w/2, data_2.avg, label="2 °C" ,width=w,color = "#4A5ABF")
b = ax.bar(x - w/2, data_1.avg, label="1.5 °C" ,width=w,color = "#39A20C")
a = ax.bar(x - 0.2, data_hist.avg, label="historic",width=w, color = "#48E9DA" )


# ax.bar_label(a,rotation=90,size=5, padding=5,fmt='%.2f')
# ax.bar_label(b,rotation=90,size=5, padding=5,fmt='%.2f')


ax.set_xticks(x)
ax.set_xticklabels(labels)
#ax.set_xlabel("Month")
ax.set_ylabel("pET [mm/month]")
ax.set_title("Potential Evapotranspiration (absolute values)")
#plt.legend()

ax.legend()
# plt.savefig(outpath+indicator+"_abs_monthly_bar.png")
# plt.show()


########--------------------abs change bar plot#--------------------------
w= 0.15
labels=data3_abs.index
x = np.arange(len(labels))
#fig, ax = plt.subplots(figsize=(12,6))
d = ax1.bar(x + 0.2, data3_abs.avg, label="3 °C" ,width=w, color = "#E99497")
c = ax1.bar(x + w/2, data2_abs.avg, label="2 °C" ,width=w,color = "#F3C583")
b = ax1.bar(x - w/2, data1_abs.avg, label="1.5 °C" ,width=w,color = "#E8E46E")

ax1.set_xticks(x)
ax1.set_xticklabels(labels)
#ax1.set_xlabel("Month")
ax1.set_ylabel("pET [mm/month]")
ax1.set_title("Potential Evapotranspiration (absolute change)")
ax1.legend()
# plt.legend()
# plt.savefig(outpath+indicator+"_abschange_monthly_bar_new.png")
# plt.show()

########--------------------rel change bar plot#--------------------------
w= 0.15
labels=data3_abs.index
x = np.arange(len(labels))
#fig, ax = plt.subplots(figsize=(12,6))
d = ax2.bar(x + 0.2, data3_rel.avg, label="3 °C" ,width=w, color = "#99154E")
c = ax2.bar(x + w/2, data2_rel.avg, label="2 °C" ,width=w,color = "#FFC93C")
b = ax2.bar(x - w/2, data1_rel.avg, label="1.5 °C" ,width=w,color = "#FFBBCC")

ax2.set_xticks(x)
ax2.set_xticklabels(labels)
ax2.set_xlabel("Month")
ax2.set_ylabel("pET [%]")
ax2.set_title("Potential Evapotranspiration [aET] (relative change)")
ax2.legend()
# plt.legend()
# plt.savefig(outpath+indicator+"_relchange_monthly_bar.png")
plt.savefig(outpath+indicator+"_all3_monthly.png")
plt.show()

