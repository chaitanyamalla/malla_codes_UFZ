#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:        spatialplot_heatdays_abs_rel.py 
#
#  Created:     DO 23-06-2021 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description:  script to produce absolute values 4 spatial plots for 49 RCP 8.5 MET files with single  indicator 
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------


import os
import ufz
from ufz import fread,readnc, position, get_brewer, abc2plot, astr 
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec #chnage size between subplots
import geopandas as gpd
import seaborn as sns
#from pandas import DataFrame

indicator= "tmax"
ind="tmax"
fname = "/work/malla/sachsen_output/sachsen_shapefiles/kreis.shp"
bo = gpd.read_file(fname)



inpath = "/work/malla/sachsen_output/spatial/data/tmax/"
outpath = "/work/malla/sachsen_output/spatial/plots_median/tmax/"

data0 = xr.open_dataset(inpath+"ensemblemedian30_" +indicator+"_historic.nc")
data1 = xr.open_dataset(inpath+"ensemblemedian30_" +indicator+ "_1_5K.nc")
data2 = xr.open_dataset(inpath+"ensemblemedian30_" +indicator+ "_2K.nc")
data3 = xr.open_dataset(inpath+"ensemblemedian30_" +indicator+ "_3K.nc")
# data0 = xr.open_dataset(inpath + "tmax30_historic_ensemblemean.nc")
# data1 = xr.open_dataset(inpath + "tmax30_1_5K_ensemblemean.nc")
# data2 = xr.open_dataset(inpath + "tmax30_2K_ensemblemean.nc")
# data3 = xr.open_dataset(inpath + "tmax30_3K_ensemblemean.nc")

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


# # #############################################################
# # #------------------     absolute values      ---------------------------------
# # #-------------------------------------------------------------------

cmap_1 = get_brewer('PuRd9',rgb=True)[3:6][::-1]
cmap_2 = get_brewer('Spectral11',rgb=True)[:8:][::-1]
cmap_3 = get_brewer('Blues9',rgb= True)[::2]
cmap = mpl.colors.ListedColormap(cmap_3 + cmap_2 + cmap_1)
#cmap.set_over("#a24f92")
#cmap.set_under("#eff2f9")


levels        = np.arange(0,28,2)
#colorbarlabel = 'mittl. Anzahl Sommertage [tmax >25°C] pro Jahr'
colorbarlabel = "Number of Average Heat days [tmax >30°C] per Year"


fig, ax = plt.subplots(2,2, figsize=(12,12), gridspec_kw = {'wspace':-0.2, 'hspace':0.1})
a = data0[ind].plot(ax=ax[0,0], cmap = cmap, levels= levels, add_colorbar=False)
b = data1[ind].plot(ax=ax[0,1], cmap = cmap, levels= levels, add_colorbar=False)
c = data2[ind].plot(ax=ax[1,0], cmap = cmap, levels= levels, add_colorbar=False)
d = data3[ind].plot(ax=ax[1,1], cmap = cmap, levels= levels, add_colorbar=False)

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


plt.savefig(outpath+"Heatdays_absolute_values_large.png")
plt.show()



# #############################################################
# #------------------     abs  change      ---------------------------------
# #-------------------------------------------------------------------

cmap_1 = get_brewer('PuBuGn9',rgb=True)
cmap_2 = get_brewer('YlOrRd9',rgb=True)


#cmap = mpl.colors.ListedColormap(cmap_2[::-1] + cmap_1)
cmap = mpl.colors.ListedColormap(cmap_1[::-1] + [(1.0,1.0,1.0)] + cmap_2)
# cmap.set_over("darkblue")
#cmap.set_under("darkred")
levels        = np.arange(-30,35,5)

colorbarlabel = 'Absolute Change Heatdays [n/yr]'

fig, ax = plt.subplots(1,3, figsize=(15,8), sharey=True, gridspec_kw = {'wspace':0.02, 'hspace':0.0})

b = data1_abs.tmax.plot(ax=ax[0], cmap = cmap, levels= levels, add_colorbar=False)
c = data2_abs.tmax.plot(ax=ax[1], cmap = cmap, levels= levels, add_colorbar=False)
d = data3_abs.tmax.plot(ax=ax[2], cmap = cmap, levels= levels, add_colorbar=False)

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



plt.savefig(outpath+"Heatdays_absolutechange_large.png")
plt.show()




######################################################################
####------------------  relative  change   ---------------------------------
########-------------------------------------------------------------------

cmap_1 = get_brewer('Blues9',rgb=True)
cmap_2 = get_brewer('Reds9',rgb=True)

cmap = mpl.colors.ListedColormap(cmap_1[::-1] + [(1.0,1.0,1.0),(1.0,1.0,1.0)] + cmap_2)
levels        = np.arange(-100,110,10)
cmap.set_under("darkblue")
#cmap.set_over("darkred")

colorbarlabel = 'Relative Change [%]'

fig, ax = plt.subplots(1,3, figsize=(15,8), sharey=True,gridspec_kw = {'wspace':0.02, 'hspace':0})

b = data1_rel.tmax.plot(ax=ax[0], cmap = cmap, levels= levels, add_colorbar=False)
c = data2_rel.tmax.plot(ax=ax[1], cmap = cmap, levels= levels, add_colorbar=False)
d = data3_rel.tmax.plot(ax=ax[2], cmap = cmap, levels= levels, add_colorbar=False)


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

plt.savefig(outpath+"Heatdays_relativechange_large.png")
plt.show()


# def ext(file):
#     dd=file
#     dd1= dd[indicator].mean(dim=["latitude","longitude"])
#     return dd1

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
# print(dae)
# dae.to_csv(outpath+indicator+"_heatdays_values.csv")
