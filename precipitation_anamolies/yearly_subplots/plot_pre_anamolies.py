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
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.cm as cm


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



inpath="/work/malla/meteo_germany/precipitation_anamolies/data/results/"
outpath_monthly="./monthly_plots/"
outpath_yearly="./"
#outpath="./"
shape=gpd.read_file("/work/malla/meteo_germany/precipitation_anamolies/data/shps_germany/Deutschland.shp")





####^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

def plot_timesteps(period,stat):
    files=glob.glob(inpath+"pre_"+period+"_anomaly_"+stat+"_1951_*")
    
    for file in files:
        plots_list=[]
        print(file)
        filename=file.split("/")[-1]
        ref_time= filename.split("_")[7]
        if ref_time == "1981":
            ref_period= "1981-2010"
        elif ref_time== "1991":
            ref_period= "1991-2020"
        #print(filename, ref_period)
        data = xr.open_dataset(file)
        #for i in range(len(data.time)):
        for i in range(len(data.time)):          #-70

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
            ax.set_title(p4, fontsize=85, fontweight="medium")
            c=shape.boundary.plot(ax=ax, edgecolor="black", linewidth=5)
            plt.xlim([5.5,15.5])
            plt.ylim([47,55.5])

            #cbar=fig.colorbar(d, ax=ax,shrink=0.6, location='bottom', extend='both', label= colorbarlabel, aspect=10*2, pad=0.05,spacing='uniform')
            #cbar.ax.tick_params(labelsize=10)

            if ref_time == "1981":
                folder= "wrt_1981_2010"
            elif ref_time== "1991":
                folder = "wrt_1991_2020"
            


            plots_list.append(fig)
            plt.close(fig)
        num_plots = len(plots_list)
        num_rows = 8  # Adjust the number of rows as desired
        num_cols = 10  # Adjust the number of columns as desired

        # Create a subplot with the specified grid dimensions
        fig, axs = plt.subplots(num_rows, num_cols,figsize=(15, 10))
        fig.subplots_adjust(bottom=0.2)

        for i, fig_item in enumerate(plots_list):
            if i < 70:
                row = i // num_cols  # Calculate the row index based on the iteration
                col = i % num_cols   # Calculate the column index based on the iteration
            else:
                row = 7  # Row index for the last row
                col = i - 70 
            fig_item.canvas.draw()
            image = fig_item.canvas.renderer.buffer_rgba()
            axs[row, col].imshow(image, aspect='auto')
            axs[row, col].axis('off')

        for col in range(num_plots % num_cols, num_cols):
            fig.delaxes(axs[-1, col])
        plt.subplots_adjust(wspace=0.01, hspace=-0.1)


        #fig.text(0.09, 0.5, 'Niederschlagsanomalie [%]', va='center', rotation='vertical', fontsize=15)


        cbar_ax = fig.add_axes([0.2, 0.1, 0.6, 0.02])
        cbar = fig.colorbar(cm.ScalarMappable(cmap=cmap, norm=norm), cax=cbar_ax, orientation='horizontal',extend='both')
        cbar.set_label('Niederschlagsanomalie[%]')
        fig.suptitle('Jährliche Niederschlagsanomalie im Vergleich zum Mittelwert '+ref_period, y=0.95, fontsize=15)

        if period == "yearly":
            plt.savefig(outpath_yearly+"pre_anamoly_yearly_"+"subplots"+stat+"_"+folder+".png", dpi=500)
            plt.savefig(outpath_yearly+"pre_anamoly_yearly_"+"subplots"+stat+"_"+folder+".pdf", dpi=500)
        elif period == "monthly":
            plt.savefig(outpath_monthly+stat+"/"+folder+"/"+"pre_anamoly_monthly_"+"subplots"+stat+".png")


        #plt.show()
        plt.close(fig)
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





