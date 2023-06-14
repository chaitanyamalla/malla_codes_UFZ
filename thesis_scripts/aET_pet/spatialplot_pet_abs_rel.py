#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:        spatialplot_aET_abs_rel.py 
#
#  Created:     Do 24-06-2021 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description:  script to produce  spatial plots for abs and rel  from 49 RCP 8.5 MET files with single  indicator 
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

inpath = "/work/malla/sachsen_output/spatial/data/pet/"
outpath = "/work/malla/sachsen_output/spatial/plots_median/aET_pet/"
indicator = "pet"
ind="pet"
fname = "/work/malla/sachsen_output/sachsen_shapefiles/kreis.shp"
bo = gpd.read_file(fname)

data0 = xr.open_dataset(inpath+"ensemblemedian_" + indicator+"_historic.nc")
data1 = xr.open_dataset(inpath+"ensemblemedian_" +indicator+ "_1_5K.nc")
data2 = xr.open_dataset(inpath+"ensemblemedian_" +indicator+ "_2K.nc")
data3 = xr.open_dataset(inpath+"ensemblemedian_" +indicator+ "_3K.nc")


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

# #############################################################
# #------------------     absolute values      ---------------------------------
# # #-------------------------------------------------------------------

# # cmap_1 = pb.colorbrewer.sequential.PuRd_9.mpl_colors
# # cmap_2 = pb.colorbrewer.diverging.Spectral_11.mpl_colors
# # cmap_3 = pb.colorbrewer.sequential.Blues_9.mpl_colors

# #cmap = mpl.colors.ListedColormap(cmap_3[3:6][::2] + cmap_2[2:4][::-1] + cmap_1[3:9][::1])

cmap_1 = get_brewer('PuRd9',rgb=True)[3:6][::-1]
cmap_2 = get_brewer('Spectral11',rgb=True)[:8:][::-1]
cmap_3 = get_brewer('Blues9',rgb= True)[2:8][::1]
cmap = mpl.colors.ListedColormap(cmap_3 + cmap_2 + cmap_1)

colorbarlabel = 'Potential Evapotranspiration [mm/yr]'
levels        = np.arange(600,840,20)


#cmap.set_over("#0D290D")
#cmap.set_under("white")


fig, ax = plt.subplots(2,2, figsize=(12,12), gridspec_kw = {'wspace':-0.2, 'hspace':0.1})
a = data0[ind].plot(ax=ax[0,0], cmap = cmap, levels= levels, add_colorbar=False)
b = data1[ind].plot(ax=ax[0,1], cmap = cmap, levels= levels, add_colorbar=False)
c = data2[ind].plot(ax=ax[1,0], cmap = cmap, levels= levels, add_colorbar=False)
d = data3[ind].plot(ax=ax[1,1], cmap = cmap, levels= levels, add_colorbar=False)

fig.colorbar(d, ax=ax, shrink=0.7, location='bottom', extend='both', label= colorbarlabel,extendfrac='Auto',aspect=20*1.2, pad=0.06)

bo.plot(ax=(ax[0,0]), color= "none", edgecolor="black", lw=0.2)
bo.plot(ax=(ax[0,1]), color= "none", edgecolor="black", lw=0.2)
bo.plot(ax=(ax[1,0]), color= "none", edgecolor="black", lw=0.2)
bo.plot(ax=(ax[1,1]), color= "none", edgecolor="black", lw=0.2)

ax[0,0].set_title("1971-2000",fontsize= 12)
ax[0,1].set_title("1.5 °C",fontsize= 12)
ax[1,0].set_title("2 °C",fontsize= 12)
ax[1,1].set_title("3 °C",fontsize= 12)

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

plt.savefig(outpath+indicator+"_absolutevalues.png")
plt.show()

########### ####------------------     abs change       ---------------------------------
########  # # # # -------------------------------------------------------------------

cmap_1 = get_brewer('PuBuGn9',rgb=True)
cmap_2 = get_brewer('YlOrRd9',rgb=True)


cmap = mpl.colors.ListedColormap(cmap_2[::-1] +[(1.0,1.0,1.0),(1.0,1.0,1.0)] + cmap_1)

#cmap.set_over("#0D290D")
#cmap.set_under("darkred")

levels        = np.arange(-60,70,10)

colorbarlabel = 'Absolute Change [mm/yr]'

fig, ax = plt.subplots(1,3, figsize=(15,8), sharey=True, gridspec_kw = {'wspace':0.02, 'hspace':0})

b = data1_abs[indicator].plot(ax=ax[0], cmap = cmap, levels= levels, add_colorbar=False)
c = data2_abs[indicator].plot(ax=ax[1], cmap = cmap, levels= levels, add_colorbar=False)
d = data3_abs[indicator].plot(ax=ax[2], cmap = cmap, levels= levels, add_colorbar=False)

fig.colorbar(d, ax=ax, shrink=0.8, location='bottom', extend='both', label= colorbarlabel,extendfrac='Auto', aspect=20*2, pad=0.08)

bo.plot(ax=(ax[0]), color= "none", edgecolor="black", lw=0.2)
bo.plot(ax=(ax[1]), color= "none", edgecolor="black", lw=0.2)
bo.plot(ax=(ax[2]), color= "none", edgecolor="black", lw=0.2)


ax[0].set_title("1.5 °C",fontsize= 12)
ax[1].set_title("2 °C",fontsize= 12)
ax[2].set_title("3 °C",fontsize= 12)

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



plt.savefig(outpath+indicator+"_absolutechange.png")
plt.show()





# ###------------------     relative        ---------------------------------
# ####-------------------------------------------------------------------

cmap_1 = get_brewer('Blues9',rgb=True)
cmap_2 = get_brewer('Reds9',rgb=True)

#cmap_1 = pb.colorbrewer.sequential.Blues_9.mpl_colors
#cmap_2 = pb.colorbrewer.sequential.Reds_9.mpl_colors

cmap = mpl.colors.ListedColormap(cmap_2[0::][::-1] + cmap_1[0::])
levels        = np.arange(-8,9,1)
#cmap.set_over("darkblue")
#cmap.set_under("darkred")

colorbarlabel = 'Relative Change [%]'

fig, ax = plt.subplots(1,3, figsize=(15,8), sharey=True,gridspec_kw = {'wspace':0.02, 'hspace':0})

b = data1_rel[indicator].plot(ax=ax[0], cmap = cmap, levels= levels, add_colorbar=False)
c = data2_rel[indicator].plot(ax=ax[1], cmap = cmap, levels= levels, add_colorbar=False)
d = data3_rel[indicator].plot(ax=ax[2], cmap = cmap, levels= levels, add_colorbar=False)


fig.colorbar(d, ax=ax, shrink=0.8, location='bottom', extend='both', label= colorbarlabel,extendfrac='Auto', aspect=20*2, pad=0.08)


bo.plot(ax=(ax[0]), color= "none", edgecolor="black", lw=0.2)
bo.plot(ax=(ax[1]), color= "none", edgecolor="black", lw=0.2)
bo.plot(ax=(ax[2]), color= "none", edgecolor="black", lw=0.2)


ax[0].set_title("1.5 °C",fontsize= 12)
ax[1].set_title("2 °C",fontsize= 12)
ax[2].set_title("3 °C",fontsize= 12)

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


plt.savefig(outpath+indicator+"_relativechange.png")
plt.show()

def ext(file):
    dd=file
    dd1= dd[indicator].mean(dim=["latitude","longitude"])
    return dd1

t=np.array(["1_5K","2K","3K"])
r1=ext(data1_abs)
r2=ext(data2_abs)
r3=ext(data3_abs)

r4=ext(data1_rel)
r5=ext(data2_rel)
r6=ext(data3_rel)

r_abs=np.concatenate((r1,r2,r3), axis=None)
r_rel=np.concatenate((r4,r5,r6), axis=None)
r_data= np.vstack((t,r_abs,r_rel))
dae = pd.DataFrame(r_data) 
print(dae)
dae.to_csv(outpath+indicator+"_values.csv")
