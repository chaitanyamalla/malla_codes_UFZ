#! /usr/bin/env python
# -*- coding: utf-8 -*-



import os
import ufz
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


def read_data(VAR,filename):
    ls=[]
    for met_id in range(met_start,met_end+1):
        tmp_data=ufz.readnetcdf("{:}/met_{:}/{:}".format(inpath,str(met_id).zfill(3),filename), var=VAR)
        tmp_data=float(tmp_data[0][0])
        ls.append(tmp_data)
    return ls


# def create_dir(folder):
#     if not os.path.exists(folder):
#         os.mkdir(folder)

#  meta                    = pd.read_csv("/data/hicam/data/processed/meteo/germany/climproj/euro-cordex/88realizations_mhm/88_main_LUT.txt",sep=" ")
meta                    = pd.read_csv("MET_list.txt",sep=" ")
met_ids                 = np.sort(pd.unique(meta["met_id"]))
# if len(met_ids) < 88: # if not all simulations are in the directory
# met_ids                 = np.sort(os.listdir("/work/malla/ww_leipzig/output_periods/"))
# met_ids                 = ["met_001", "met_002"]

# list of names of the rcps climate models
gcms                    = np.sort(pd.unique(meta["gcm"]))
# list of names of the regional climate models
rcms            = np.sort(pd.unique(meta["inst.rcm"]))
# list of names of the hydrological models
hms                     = ['mHM']
# list of names of the rcps
# rcps                    = ['rcp2p6', 'rcp6p0', 'rcp8p5']
# rcps                    = np.sort(pd.unique(meta["rcp"]))
rcps                      = pd.Series(meta["rcp"], dtype="category")

if __name__ == '__main__':

    inpath="/work/malla/ww_leipzig/output_periods/"
    met_start=1
    met_end=88

    #timeperiod="1971_2000"

    listA = np.array(['2021', '2036', '2070'], dtype=np.str)
    listB = np.array(['2050', '2065', '2099'], dtype=np.str)
    for i in range(3):
        timeperiod= listA[i]+'_'+ listB[i]
        #print(timeperiod)
        #timeperiod = item#     print (timeperiod)
        save_results_to = '/public/malla/plot_pre_tmax/'
        
        filename="pre_ug_halfyear_{:}_ysum_timmean_fldpctl_difference.nc".format(timeperiod)
        data_winterprecip=read_data(VAR="pre",filename=filename)
        # when fldpctl not computed with cdo
        #data_winterprecip=[[np.median(i)] for i in data_winterprecip]


        filename="tmax_ug_gtc25_{:}_ysum_timmean_fldpctl_difference.nc".format(timeperiod)
        data_summerdays=read_data(VAR="tmax",filename=filename)
        #filename="recharge_ug_{:}_ysum_timmean_fldpctl_difference.nc".format(timeperiod)
        #data_recharge=read_data(VAR="recharge",filename=filename)

        #sns.scatterplot(data_recharge, data_winterprecip, hue= rcps, palette= ["C2", "C0", "k"])
        sns.scatterplot(data_summerdays, data_winterprecip, hue= rcps, palette= ["C2", "C0", "k"])
        #plt.scatter(data_summerdays,data_winterprecip)
        plt.xlabel("Number of days > 25°C, difference with 1971-2000")
        plt.ylabel("winter precipitation difference with historic 1971-2000(mm)")
        plt.title(timeperiod)
        #plt.xlim(-10, 50)
        #plt.ylim(-25, 170)
        plt.xlim(0, 90)
        plt.ylim(-25, 170)
        plt.show()

        # plt.savefig(save_results_to + timeperiod + 'recharge_diff' + '.png')
        #plt.savefig(save_results_to + timeperiod + '_tmax_pre_diff' + '.png')
        plt.clf()
        


