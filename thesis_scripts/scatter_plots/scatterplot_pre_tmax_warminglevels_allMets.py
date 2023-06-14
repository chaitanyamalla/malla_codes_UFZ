#! /usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------
#  File:        scatterplot_pre_tmax_warminglevels_allMets.py 
#
#  Created:     Di 18-06-2021 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce scatterplot for 3 warming periods for 49 RCP 8.5 MET files with two indicator 
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------

import os
import ufz
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns



def read_data(VAR,filename):
    ls=[]
    for met_id in mets:
        tmp_data=ufz.readnetcdf("{:}/met_{:}/{:}".format(inpath,str(met_id).zfill(3),filename), var=VAR)
        tmp_data=float(tmp_data[0][0])
        ls.append(tmp_data)
    return ls




meta                    = pd.read_csv("/work/malla/sachsen_output/RCP8.5_EurCordex_list.csv", sep=";")
met_ids                 = np.sort(pd.unique(meta["met_id"]))
# if len(met_ids) < 88: # if not all simulations are in the directory
# met_ids                 = np.sort(os.listdir("/work/malla/ww_leipzig/output_periods/"))
# met_ids                 = ["met_001", "met_002"]

# list of names of the rcps climate models
#gcms                    = np.sort(pd.unique(meta["gcm"]))
gcms = pd.Series(meta["gcm"], dtype="category")
# list of names of the regional climate models
rcms            = np.sort(pd.unique(meta["inst.rcm"]))
# list of names of the hydrological models
hms                     = ['mHM']
# list of names of the rcps
# rcps                    = ['rcp2p6', 'rcp6p0', 'rcp8p5']
# rcps                    = np.sort(pd.unique(meta["rcp"]))
rcps                      = pd.Series(meta["rcp"], dtype="category")



#print(gcms)






if __name__ == '__main__':

    inpath="/work/malla/sachsen_output/yearly/"
    mets=[1,2,7,8,9,10,21,22,23,24,25,26,27,28,29,30,31,35,36,37,40,41,50,51,52,53,54,55,56,57,58,67,68,69,70,71,72,73,74,75,76,77,78,82,83,84,85,86,87]


    listA = np.array(['1_5K', '2K', '3K'], dtype=np.str)
    for i in range(3):
        warmperiod= listA[i]

    
        save_results_to = '/work/malla/sachsen_output/scatter_plots/'

        filename="pre_{:}_ysum_timmean_fldpctl.nc".format(warmperiod)
        data_yearlyprecip=read_data(VAR="pre",filename=filename)


        filename="tmax_{:}_gtc25_ysum_timmean_fldpctl.nc".format(warmperiod)
        data_summerdays=read_data(VAR="tmax",filename=filename)



        
        fig = plt.figure(figsize=(5,7))
        
        sns.scatterplot(data_summerdays, data_yearlyprecip, hue= gcms, s=20)
        plt.title(warmperiod)
        plt.xlabel("Number of days > 25°C per year (summerdays)")
        plt.ylabel("Average Yearly precipitation [mm/yr]")
        plt.xlim(35, 80)
        plt.ylim(675, 950)
        #plt.show()

        plt.savefig(save_results_to + warmperiod + '_yearlyprecip_vs_summerdays_GCMs' + '.png')
        plt.clf()
