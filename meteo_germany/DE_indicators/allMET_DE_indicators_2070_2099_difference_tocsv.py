#! /usr/bin/env python
# -*- coding: utf-8 -*-




# --------------------------------------------------
#  File:        allMET_DE_indicators_2070_2099_difference_tocsv.py 
#
#  Created:     Do 23-07-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce csv of all METfiles with different indicators for region GERMANY for year 2070_2099 difference from 1971_2000
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
import xarray as xr


inpath = "/work/malla/meteo_germany/data_output/"
outpath = "/work/malla/meteo_germany/"

mets=[1,2,3,4,7,8,9,10,11,12,13,14,15,21,22,23,24,25,26,27,28,29,30,31,32,35,36,37,38,39,40,41,42,43,44,45,50,51,52,53,54,55,56,57,58,59,60,61,62,67,68,69,70,71,72,73,74,75,76,77,78,79,80,82,83,84,85,86,87,88]


      
pre = []   #yearly
pre_s = []  #summer
pre_w = []   #winter
recharge = []
tmax25 = []
tmax30 = []



def readfile(filename, timeperiod, indicator):
    try:
        
    
        filename =filename.format(timeperiod)

    
        data = xr.open_dataset(inpath + met_id + filename)

        
        if indicator == "pre":
            data_mean = data.pre.mean(dim=["lat", "lon"]).to_dataframe(met_id)
        elif indicator == "recharge":
            data_mean = data.recharge.mean(dim=["lat", "lon"]).to_dataframe(met_id)
        elif indicator == "tmax":
            data_mean = data.tmax.mean(dim=["lat", "lon"]).to_dataframe(met_id)
        #print(data_mean.shape)    
        return data_mean
    
    except:
        data_mean = pd.DataFrame(np.nan,index=[0], columns=[met_id])
        #print(data_mean)
        return data_mean 


    
        
for met in mets:
    met_id="met"+'_'+ str(met).zfill(3)

 
    timeperiod = "2070_2099"



    pre_y_file1 = readfile("/pre_yearly_{:}_ysum_timmean_fldpctl_difference.nc", timeperiod, "pre")
    pre_w_file1 = readfile("/pre_winter_{:}_ysum_timmean_fldpctl_difference.nc", timeperiod, "pre")
    pre_s_file1 = readfile("/pre_summer_{:}_ysum_timmean_fldpctl_difference.nc", timeperiod, "pre")
    rech_file1 = readfile("/recharge_adjust_{:}_ysum_timmean_fldpctl_difference.nc", timeperiod, "recharge")
    tmax25_file1 = readfile("/tmax25_{:}_ysum_timmean_fldpctl_difference.nc", timeperiod, "tmax")
    tmax30_file1 = readfile("/tmax30_{:}_ysum_timmean_fldpctl_difference.nc", timeperiod, "tmax")


    pre.append(pre_y_file1.copy())
    pre_w.append(pre_w_file1.copy())
    pre_s.append(pre_s_file1.copy())
    recharge.append(rech_file1.copy())
    tmax25.append(tmax25_file1.copy())
    tmax30.append(tmax30_file1.copy())




def processing(data1, name):
    r = pd.concat(data1, axis=1)
    r["files"]= name
    r = r.set_index("files")
    r = (r.T)
    #print(r)
    return r


pre = processing(pre, "pre_yearly")
pre_s = processing(pre_s, "pre_summer")
pre_w = processing(pre_w, "pre_winter")
recharge = processing(recharge, "recharge_adjust")
tmax25 = processing(tmax25, "Tmax25[n]")
tmax30 = processing(tmax30, "Tmax30[n]")


data = pre.join([ pre_s, pre_w, recharge, tmax25, tmax30])  #recharge_adj, tmax25, pre_s, pre_w,
#print(data)


#######--------------rcps-----------------#########
meta = pd.read_csv("/work/malla/meteo_germany/METs_RCP26_85.1.csv",sep=";")
met_ids = np.sort(pd.unique(meta["met_id"]))
gcms = np.sort(pd.unique(meta["gcm"]))
rcms = np.sort(pd.unique(meta["inst.rcm"]))
rcps = pd.Series(meta["rcp"], dtype="category")
hms= ['mHM']
rcp = pd.DataFrame(rcps, columns = ['rcp'])
##########----------------------------------------####

data = data.reset_index()
data = data.join(rcp)
print(data)


data.to_csv(outpath + "AllMETfiles_DE_2070_2099_difference_rcp26_85_indicators.csv")
