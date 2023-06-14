#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:        spatialplot_recharge_adjust_abs_rel.py 
#
#  Created:     Do 16-06-2021 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description:  script to produce 3 spatial plots for abs and rel each from 49 RCP 8.5 MET files with single  indicator 
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
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.gridspec as gridspec #chnage size between subplots

import geopandas as gpd
import palettable as pb
import seaborn as sns

inpath = "/work/malla/sachsen_output/spatial/data/recharge/"
outpath = "/work/malla/sachsen_output/spatial/plots_median/recharge/"

indicator= "recharge"

fname = "/work/malla/sachsen_output/sachsen_shapefiles/kreis.shp"
bo = gpd.read_file(fname)

data0 = xr.open_dataset(inpath+"ensemblemedian_" + indicator+"_adjust_historic.nc")
data1 = xr.open_dataset(inpath+"ensemblemedian_" +indicator+ "_adjust_1_5K.nc")
data2 = xr.open_dataset(inpath+"ensemblemedian_" +indicator+ "_adjust_2K.nc")
data3 = xr.open_dataset(inpath+"ensemblemedian_" +indicator+ "_adjust_3K.nc")

#shape= gpd.read_file("/work/malla/sachsen_output/sachsen_shapefiles/kreis.shp")

data0 = data0.where(data0 >0)
data1 = data1.where(data1 >0)
data2 = data2.where(data2 >0)
data3 = data3.where(data3 >0)

data1_abs = data1-data0
data2_abs = data2-data0
data3_abs = data3-data0




data1_rel = (data1_abs/data0)*100
data2_rel = (data2_abs/data0)*100
data3_rel = (data3_abs/data0)*100


# data1_abs = data1_abs.where(data1_abs>0)
# data2_abs = data2_abs.where(data2_abs>0)
# data3_abs = data3_abs.where(data3_abs>0)

#############################################################
#------------------     absolute values      ---------------------------------
#-------------------------------------------------------------------



#cmap_1 = get_brewer('PuRd9',rgb=True)[3:6][::-1]
#cmap_2 = get_brewer('Spectral11',rgb=True)[:8:][::-1]
#cmap_3 = get_brewer('Blues9',rgb= True)[::2]
#cmap = mpl.colors.ListedColormap(cmap_3 + cmap_2 + cmap_1)

#levels = np.array([0,25,50,75,100,150,200,300,350,500,10000])
#colors  = ["#fb8144","#ffb976" ,"#ffd57f","#fff157","#bbd67a", "#8eca94", "#78cbbe", "#55bac8","#32a9b8", "#009eab"  ]
colors  = ["#fb8144","#ffb976" ,"#ffd57f","#fff157","#41ae76", "#8eca94", "#78cbbe", "#55bac8","#32a9b8", "#009eab"  ]
cmap = mpl.colors.ListedColormap(colors[::])

colorbarlabel = 'Recharge [mm/yr]'
levels        = np.arange(0,300,30)


#cmap.set_over("#0D290D")
#cmap.set_under("white")


fig, ax = plt.subplots(2,2, figsize=(12,12), gridspec_kw = {'wspace':-0.2, 'hspace':0.1})
a = data0.recharge.plot(ax=ax[0,0], cmap = cmap, levels= levels, add_colorbar=False)
b = data1.recharge.plot(ax=ax[0,1], cmap = cmap, levels= levels, add_colorbar=False)
c = data2.recharge.plot(ax=ax[1,0], cmap = cmap, levels= levels, add_colorbar=False)
d = data3.recharge.plot(ax=ax[1,1], cmap = cmap, levels= levels, add_colorbar=False)

cbar=fig.colorbar(d, ax=ax, shrink=0.7, location='bottom', extend='both', label= colorbarlabel,extendfrac='Auto',aspect=20*1.2, pad=0.06)
cbar.ax.tick_params(labelsize=16)
bo.plot(ax=(ax[0,0]), color= "none", edgecolor="black", lw=0.2)
bo.plot(ax=(ax[0,1]), color= "none", edgecolor="black", lw=0.2)
bo.plot(ax=(ax[1,0]), color= "none", edgecolor="black", lw=0.2)
bo.plot(ax=(ax[1,1]), color= "none", edgecolor="black", lw=0.2)

ax[0,0].set_title("1971-2000",fontsize= 16)
ax[0,1].set_title("1.5 °C",fontsize= 16)
ax[1,0].set_title("2 °C",fontsize= 16)
ax[1,1].set_title("3 °C",fontsize= 16)

ax[0,0].set_xlabel("")
ax[0,0].set_ylabel("")
ax[0,1].set_xlabel("")
ax[0,1].set_ylabel("")
ax[1,0].set_xlabel("")
ax[1,0].set_ylabel("")
ax[1,1].set_xlabel("")
ax[1,1].set_ylabel("")


ax[0,0].xaxis.set_visible(False)
ax[0,1].xaxis.set_visible(False)
ax[0,1].yaxis.set_visible(False)
ax[1,1].yaxis.set_visible(False)

#ax[1,1].xaxis.set_ticks([])

ax[0,0].tick_params(axis="both", labelsize=7)
ax[0,1].tick_params(axis="both", labelsize=7)
ax[1,0].tick_params(axis="both", labelsize=7)
ax[1,1].tick_params(axis="both", labelsize=7)



plt.savefig(outpath+indicator+"_adjust_absolutevalues_large.png")
# plt.show()



#############################################################
#------------------     abs  change      ---------------------------------
#-------------------------------------------------------------------

cmap_1 = get_brewer('PuBuGn9',rgb=True)
cmap_2 = get_brewer('YlOrRd9',rgb=True)
#cmap_1 = pb.colorbrewer.sequential.PuBuGn_9.mpl_colors
#cmap_2 = pb.colorbrewer.sequential.YlOrRd_8.mpl_colors

cmap = mpl.colors.ListedColormap(cmap_2[::-1] + cmap_1)
# cmap.set_over("darkblue")
#cmap.set_under("darkred")
levels        = np.arange(-60,70,10)

colorbarlabel = 'Absolute Change [mm/yr]'

fig, ax = plt.subplots(1,3, figsize=(15,8), sharey=True, gridspec_kw = {'wspace':0.02, 'hspace':0.0})

b = data1_abs.recharge.plot(ax=ax[0], cmap = cmap, levels= levels, add_colorbar=False)
c = data2_abs.recharge.plot(ax=ax[1], cmap = cmap, levels= levels, add_colorbar=False)
d = data3_abs.recharge.plot(ax=ax[2], cmap = cmap, levels= levels, add_colorbar=False)

cbar=fig.colorbar(d, ax=ax, shrink=0.8, location='bottom', extend='both', label= colorbarlabel,extendfrac='Auto', aspect=20*2, pad=0.08)
cbar.ax.tick_params(labelsize=16)
bo.plot(ax=(ax[0]), color= "none", edgecolor="black", lw=0.2)
bo.plot(ax=(ax[1]), color= "none", edgecolor="black", lw=0.2)
bo.plot(ax=(ax[2]), color= "none", edgecolor="black", lw=0.2)


ax[0].set_title("1.5 °C",fontsize= 16)
ax[1].set_title("2 °C",fontsize= 16)
ax[2].set_title("3 °C",fontsize= 16)

ax[0].set_xlabel("")
ax[0].set_ylabel("")
ax[1].set_xlabel("")
ax[1].set_ylabel("")
ax[2].set_xlabel("")
ax[2].set_ylabel("")

#ax[0].yaxis.set_visible(False)
ax[1].yaxis.set_visible(False)
ax[2].yaxis.set_visible(False)
#ax[3].yaxis.set_visible(False)

#ax[1].xaxis.set_ticks([])

ax[0].tick_params(axis="both", labelsize=7)
ax[1].tick_params(axis="both", labelsize=7)
ax[2].tick_params(axis="both", labelsize=7)
#ax[3].tick_params(axis="both", labelsize=5)



plt.savefig(outpath+"recharge_adjust_absolutechange_large.png")
# plt.show()




################
########------------------  relative  change   ---------------------------------
########-------------------------------------------------------------------

cmap_1 = get_brewer('Blues9',rgb=True)
cmap_2 = get_brewer('Reds9',rgb=True)

# cmap_1 = pb.colorbrewer.sequential.Blues_9.mpl_colors
# cmap_2 = pb.colorbrewer.sequential.Reds_9.mpl_colors

cmap = mpl.colors.ListedColormap(cmap_2[::-1] + [(1.0,1.0,1.0),(1.0,1.0,1.0)] + cmap_1)
levels        = np.arange(-100,110,10)
cmap.set_over("darkblue")
cmap.set_under("darkred")

colorbarlabel = 'Relative Change [%]'

fig, ax = plt.subplots(1,3, figsize=(15,8), sharey=True,gridspec_kw = {'wspace':0.02, 'hspace':0})

b = data1_rel.recharge.plot(ax=ax[0], cmap = cmap, levels= levels, add_colorbar=False)
c = data2_rel.recharge.plot(ax=ax[1], cmap = cmap, levels= levels, add_colorbar=False)
d = data3_rel.recharge.plot(ax=ax[2], cmap = cmap, levels= levels, add_colorbar=False)


cbar=fig.colorbar(d, ax=ax, shrink=0.8, location='bottom', extend='both', label= colorbarlabel,extendfrac='Auto', aspect=20*2, pad=0.08)
cbar.ax.tick_params(labelsize=16)

bo.plot(ax=(ax[0]), color= "none", edgecolor="black", lw=0.2)
bo.plot(ax=(ax[1]), color= "none", edgecolor="black", lw=0.2)
bo.plot(ax=(ax[2]), color= "none", edgecolor="black", lw=0.2)

#ax[0].set_title("1971-2000",fontsize= 10)
ax[0].set_title("1.5 °C",fontsize= 16)
ax[1].set_title("2 °C",fontsize= 16)
ax[2].set_title("3 °C",fontsize= 16)

ax[0].set_xlabel("")
ax[0].set_ylabel("")
ax[1].set_xlabel("")
ax[1].set_ylabel("")
ax[2].set_xlabel("")
ax[2].set_ylabel("")
#ax[3].set_xlabel("")
#ax[3].set_ylabel("")
#ax[0].yaxis.set_visible(False)
ax[1].yaxis.set_visible(False)
ax[2].yaxis.set_visible(False)
#ax[3].yaxis.set_visible(False)

#ax[1].xaxis.set_ticks([])

ax[0].tick_params(axis="both", labelsize=7)
ax[1].tick_params(axis="both", labelsize=7)
ax[2].tick_params(axis="both", labelsize=7)
#ax[3].tick_params(axis="both", labelsize=5)


plt.savefig(outpath+"recharge_adjust_relativechange_large.png")
# plt.show()

def ext(file):
    dd=file
    dd1= dd.recharge.mean(dim=["lat","lon"])
    return dd1

# t=np.array(["1_5K","2K","3K"])
# r1=ext(data1_abs)
# r2=ext(data2_abs)
# r3=ext(data3_abs)

# r4=ext(data1_rel)
# r5=ext(data2_rel)
# r6=ext(data3_rel)

# r_abs=np.concatenate((r1,r2,r3), axis=None)
# r_rel=np.concatenate((r4,r5,r6), axis=None)
# r_data= np.vstack((t,r_abs,r_rel))
# dae = pd.DataFrame(r_data) 
# dae.to_csv(outpath+indicator+"_values.csv")
