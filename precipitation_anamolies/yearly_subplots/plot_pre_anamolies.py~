#! /usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import ufz
from ufz import fread,readnc, position, get_brewer, abc2plot, astr
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr
import geopandas as gpd
import datetime
#import palettable as pb
from matplotlib import colors
from matplotlib.colors import ListedColormap, BoundaryNorm
import optparse




stat=''
period=''

parser = optparse.OptionParser(usage='%prog [options]',
                               description="Changing CRS of existing Netcdf files")
parser.add_option('-s', '--stat', action='store',
                  default=stat, dest='stat', metavar='stat',
                  help='stats of file like percentage or abs')
parser.add_option('-p', '--period', action='store',
                  default=period, dest='period', metavar='period',
                  help='yearly or monthly')


(opts, args) = parser.parse_args()
stat= opts.stat
period=opts.period



inpath="./data/results/"
outpath_monthly="./monthly_plots/"
outpath_yearly="./yearly_plots/"
#outpath="./"
shape=gpd.read_file("./data/shps_germany/Deutschland.shp")







####^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

def plot_timesteps(period,stat):
    files=glob.glob(inpath+"pre_"+period+"_anomaly_"+stat+"_2018_*")
    for file in files:
        print(file)
        filename=file.split("/")[-1]
        ref_time= filename.split("_")[7]
        if ref_time == "1981":
            ref_period= "1981-2010 mean"
        elif ref_time== "1991":
            ref_period= "1991-2020 mean"
        #print(filename, ref_period)
        data = xr.open_dataset(file)
        for i in range(len(data.time)):

            p=data.pre[i].time
            p1=p.item(0)
            p2=pd.to_datetime(p1, utc=True)
            if period == "monthly":
                p4= p2.strftime('%Y-%m')
                time="m"
            elif period == "yearly":
                p4= p2.strftime('%Y')
                time="y"
            if stat== "perc":
                units= "[%]"
            elif stat=="abs":
                units= "difference [mm/"+time+"]"
             
            colorbarlabel = period.title()+" precipitation anomaly "+units+" of "+ p4 + " with respect to " + ref_period

            fig, ax = plt.subplots(figsize=(9,12.5))

            d=data.pre[i].plot.imshow(ax=ax, cmap = cmap,  interpolation=None, norm=norm, add_colorbar=False)
            ax.set_title(p4)
            c=shape.boundary.plot(ax=ax, edgecolor="black", linewidth=0.5)
            plt.xlim([5.5,15.5])
            plt.ylim([47,55.5])

            cbar=fig.colorbar(d, ax=ax,shrink=0.6, location='bottom', extend='both', label= colorbarlabel, aspect=10*2, pad=0.05,spacing='uniform')
            cbar.ax.tick_params(labelsize=10)

            if ref_time == "1981":
                folder= "wrt_1981_2010"
            elif ref_time== "1991":
                folder = "wrt_1991_2020"
            
            if period == "yearly":
                plt.savefig(outpath_yearly+stat+"/"+"pre_anamoly_yearly_"+p4+"_"+folder+"_"+stat+".png")
            elif period == "monthly":
                plt.savefig(outpath_monthly+stat+"/"+folder+"/"+"pre_anamoly_monthly_"+p4.replace("-","_")+"_"+folder+"_"+stat+".png")
            #plt.show()



##########################################################################################################################################
#######----------------------color bars and colors -------------------------------------------------------------------------------------
if period=="yearly":
    if stat =="perc":
        cmap_1 = get_brewer('GnBu9',rgb=True)
        cmap_2 = get_brewer("YlOrBr9",rgb=True)
        #cmap=mpl.colors.ListedColormap(cmap_2[::-1]+cmap_1) 
        cmap = mpl.colors.ListedColormap(cmap_2[::-1]+[(1.0,1.0,1.0), (1.0,1.0,1.0)]+cmap_1) 
        cmap.set_over("#091457") 
        cmap.set_under("#570F09")
        norm = colors.Normalize(vmin=-50,vmax=50) 
    elif stat == "abs":
        cmap_1 = get_brewer('PuBu9',rgb=True)
        cmap_2 = get_brewer("YlOrRd9",rgb=True)
        cmap = mpl.colors.ListedColormap(cmap_2[::-1]+cmap_1) 
        cmap.set_over("#091457") 
        cmap.set_under("#570F09")
        norm = colors.Normalize(vmin=-450, vmax=450)

elif period=="monthly":
    if stat=="perc":
        cmap_1 = get_brewer('GnBu9',rgb=True)
        cmap_2 = get_brewer("YlOrBr9",rgb=True)
        cmap = mpl.colors.ListedColormap(cmap_2[::-1]+cmap_1) 
        cmap.set_over("#091457") 
        cmap.set_under("#570F09")
    elif stat=="abs":
        cmap_1 = get_brewer('PuBu9',rgb=True)
        cmap_2 = get_brewer("YlOrRd9",rgb=True)
        cmap = mpl.colors.ListedColormap(cmap_2[::-1]+cmap_1) 
        cmap.set_over("#091457") 
        cmap.set_under("#570F09")
        
    norm = colors.Normalize(vmin=-80, vmax=80)
####--------------------------------------------------------------------------------------------------------------------------------------        
        
    

anamoly= plot_timesteps(period, stat)




