#! /usr/bin/env python
# -*- coding: utf-8 -*-



# --------------------------------------------------
#  File:        plot_data.py
#
#  Created:     Mi 14-04-2021
#  Author:      Friedrich Boeing
#
# --------------------------------------------------
#
#  Description: script to produce scatterplots for HICAM climate ensemble evaluation
#
#  Modified:
#
# --------------------------------------------------


import ufz
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

def read_data(VAR,filename):
    tmp_data=ufz.readnetcdf("{:}/{:}".format(inpath,filename), var=VAR)
    return tmp_data


if __name__ == '__main__':

    #inpath="/work/malla/ww_leipzig/data_1990_2020/data_1990_2020"
    inpath="/work/malla/ww_leipzig/data_1990_2020/data_1990_2020"
    outpath="/work/malla/ww_leipzig/data_1990_2020/data_1990_2020/plots_1990_2020/"
    #inpath="/data/hydmet/WIS_D/ww_leipzig/data_obs/"
    year_start=1990
    year_end=2020
    timeperiod="{:}_{:}".format(year_start,year_end)
    years=np.arange(year_start,year_end+1)
    var="tmax"
    #filename="{:}_ug_{:}_ysum.nc".format(var,timeperiod)
    
    filename="{:}_ug_{:}_gtc30_ysum.nc".format(var,timeperiod)
    
    data=read_data(VAR=var,filename=filename)
    q25, median, q75 =np.percentile(data,[25,50,75],axis=(1,2)) # calculates the median
    #datetimes = [datetime.datetime(years[i],months[i],days[i]) for i in np.arange(times.shape[0])]
    ifig       = 0
    fig        = plt.figure(ifig)
    ax         = fig.add_axes(ufz.position(1,1, 1, bottom=0.10, top=0.97, left=0.098, right=0.92))
    ax.fill_between(years,q75,median,alpha=0.5,color="grey")
    ax.fill_between(years,q25,median,alpha=0.5,color="grey")
    ax.plot(years,median)
    ax.set_xlabel("Jahre")

    if var == "pre" :
        ax.set_ylabel("Jahresniederschlag [mm]") #precipitation oder Niederschlag
    elif var == "recharge" or var == "recharge_adjust":
        ax.set_ylabel("jährliche Grundwasserneubildung [mm]")
    elif var == "tmax" and filename == "tmax_ug_1990_2020_gtc30_ysum.nc":
        ax.set_ylabel("Anzahl Hitzetage [n]")
    elif var == "tmax" and filename == "tmax_ug_1990_2020_gtc25_ysum.nc":
        ax.set_ylabel("Anzahl Sommertage [n]")
    elif var == "aET":
        ax.set_ylabel("aktuelle Evapotranspiration [mm]")
    elif var == "pet":
        ax.set_ylabel("potentielle Evapotranspiration [mm]")
        
    minor_locator = AutoMinorLocator(5)
    ax.xaxis.set_minor_locator(minor_locator)
    #plt.grid(which='both')
    #plt.show()

    plt.savefig(outpath + var+"_gtc30_" +timeperiod + '_ysum' + '.png')
    #plt.savefig(outpath + var +timeperiod + '_ysum' + '.png')
