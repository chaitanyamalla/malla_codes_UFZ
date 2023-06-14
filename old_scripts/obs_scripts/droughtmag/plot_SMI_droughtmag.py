#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:       plot_SMI_droughtmag.py
#
#  Created:     Di 22-06-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: ploting single graph VEG1 and VEG2 of SMI droughtmag data. 
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

import ufz as ufz

from ufz import position, get_brewer, abc2plot


png=True
outfile="/data/hydmet/WIS_D/ww_leipzig/output/obs/droughtmag/plots/Duerreintensitaet_SM_0_30cm_vegetationsperiode_1990-2020_ug.png"
colors=["#3182bd", "#e6550d"]
color='#662506'
#  -- define area dictionary for bubbles -----------

bins_area=[0,20,40,60,80,100]
bins_area=[0,0.001,0.05,0.1,0.15,0.2]
bins_num=np.arange(1,len(bins_area))
size_area=[10,100,250,500,750]
dict_size=dict(zip(bins_num,size_area))
##----------bubble plot-----------##


iplot             = 1
nrow              = 3
ncol              = 1
fig=plt.figure(figsize=(10,8))

#  -- read data ------------------------------------

mask_sum=ufz.readnetcdf("/data/hydmet/WIS_D/ww_leipzig/input/masks/mask_ug_fldsum.nc", var='mask')

inpath = "/data/hydmet/WIS_D/ww_leipzig/output/obs/droughtmag/"

file1 ="SMI_SM_0_30cm_ug_1990-2020_droughtmag_fldsum_veg4-10.nc"
file2 = "SMI_SM_0_30cm_ug_1990-2020_droughtmag_fldsum_veg1.nc"
file3 ="SMI_SM_0_30cm_ug_1990-2020_droughtmag_fldsum_veg2.nc"
titles=["Vegetationperiode Gesamt (Apr-Okt)", "Vegetationperiode 1 (Apr-Jun)", "Vegetationperiode 2 (Jul-Sep)"]
#  -- loop over files ------------------------------

for ii,file_tmp in enumerate([file1,file2,file3]):
    print(ii, file_tmp)
    ax_pos = position(nrow, ncol, ii+1,
                          left=0.08, right=0.98,
                      vspace=0.1, hspace=0.05,
                          bottom=0.2, top=0.93)
    ax     = fig.add_axes(ax_pos)
    veg= xr.open_dataset(inpath + file_tmp)

    veg= veg.median(dim=["lat", "lon"]).to_dataframe()
    time_bnds  = ufz.readnetcdf(inpath + file_tmp, var='time_bnds')
    time_diff=time_bnds[:,1] -time_bnds[:,0] + 1

    veg = veg.reset_index()
    veg['year'] = veg["time"].dt.year
    #  -- normalize by timediff and number of gridcells -- 
    veg["SMI"]=veg.SMI/(time_diff)
    veg["SMI"]=veg.SMI.divide(int(mask_sum))
    data_s_cat=np.digitize(veg.SMI,bins_area)
    print(data_s_cat)



    scatter=sns.scatterplot(veg.year,veg.SMI,color=color,edgecolor="black",size=data_s_cat,sizes=dict_size,alpha=0.4,legend=False)


    ax.set_ylim([-0.01,0.22])
    ax.set_title(titles[ii])
    ax.set_xlabel("Jahr")
    if ii == 1:
        ax.set_ylabel("Dürreintensität")
    else:
        ax.set_ylabel("")

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
#  --  legend --------------------------------------

ax_legend_pos = position(1, 1, 1,
                          left=0.25, right=0.75,
                      vspace=0.02, hspace=0.01,
                                 bottom=0.01, top=0.15)
ax_legend     = fig.add_axes(ax_legend_pos)
scatter_leg=sns.scatterplot(bins_num,size_area,color=color,size=bins_num,sizes=dict_size,alpha=0.4)
scatter_leg.set_ylim([0,0])
labels_leg=["Dürreintensität"] +[r"{:} - $<${:}".format(aa,bb) for aa,bb in zip(bins_area[:-1],bins_area[1:])]
ax_legend.legend(ncol=6,loc="center",labels=labels_leg,frameon=False,labelspacing=2,title="Legende: ")
plt.axis('off') # deativate everything

#  -- print or show plot ---------------------------

if png:
    plt.savefig(outfile)
else:
    plt.show()
#fig.savefig(inpath + "plot_obs_SMI_VEG1_VEG2.png")
#fig.savefig(inpath + "plot_obs_SMI_VEG1_VEG2_bubble.png")
