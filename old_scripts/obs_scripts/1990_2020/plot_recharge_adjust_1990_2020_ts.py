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


def read_data(VAR,filename):
    tmp_data=ufz.readnetcdf("{:}/{:}".format(inpath,filename), var=VAR)
    return tmp_data


if __name__ == '__main__':

    inpath="/data/hydmet/WIS_D/ww_leipzig/output/obs/ts"
    outpath="/data/hydmet/WIS_D/ww_leipzig/output/obs/plots/1990_2020/"

    year_start=1990
    year_end=2020
    timeperiod="{:}-{:}".format(year_start,year_end)
    years=np.arange(year_start,year_end+1)
    var="recharge_adjust"
    filename="{:}_ug_{:}_yearsum.nc".format(var,timeperiod)

    
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


    ax.set_ylabel("jährliche adjustierte Grundwasserneubildung [mm]") #precipitation oder Niederschlag

    
    #plt.show()

    plt.savefig(outpath + var+'_'+timeperiod + '_ysum' + '.png')
    #plt.savefig(outpath + var+"_"+timeperiod + '_ysum' + '.png')
