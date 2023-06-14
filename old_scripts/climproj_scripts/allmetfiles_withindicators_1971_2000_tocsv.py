#! /usr/bin/env python
# -*- coding: utf-8 -*-




# --------------------------------------------------
#  File:        allmetfiles_withindicators_tocsv.py
#
#  Created:     Mi 23-04-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce csv of all METfiles with different indicators to see the far oulier performing METfiles 
#
#  Modified by: Chaitanya Malla
#  Modified date: Sa 17.07.2021
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

inpath="/data/hydmet/WIS_D/ww_leipzig/output/climproj/data_periods/"
#inpath="/work/malla/ww_leipzig/output_periods/"
outpath="/data/hydmet/WIS_D/ww_leipzig/output/climproj/csv/"
#outpath="/work/malla/ww_leipzig/data_1971_2099/"
met_start=1
met_end=88

pre = []   #yearly
pre_s = []  #summer
pre_w = []   #winter
recharge = []
tmax25 = []
tmax30 = []
recharge_adj=[]

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


        
for met in range(met_start, met_end+1):
    met_id="met"+'_'+ str(met).zfill(3)

    timeperiod = "1971_2000"



    pre_y_file1 = readfile("/pre_ug_yearly_{:}_ysum_timmean_fldpctl.nc", timeperiod, "pre")
    pre_w_file1 = readfile("/pre_ug_winter_{:}_ysum_timmean_fldpctl.nc", timeperiod, "pre")
    pre_s_file1 = readfile("/pre_ug_summer_{:}_ysum_timmean_fldpctl.nc", timeperiod, "pre")
    rech_file1 = readfile("/recharge_ug_{:}_ysum_timmean_fldpctl.nc", timeperiod, "recharge")
    tmax25_file1 = readfile("/tmax_ug_gtc25_{:}_ysum_timmean_fldpctl.nc", timeperiod, "tmax")
    tmax30_file1 = readfile("/tmax_ug_gtc30_{:}_ysum_timmean_fldpctl.nc", timeperiod, "tmax")
    rech_adj_file1 = readfile("/recharge_adjust_ug_{:}_ysum_timmean_fldpctl.nc", timeperiod, "recharge")
    
    pre.append(pre_y_file1.copy())
    pre_w.append(pre_w_file1.copy())
    pre_s.append(pre_s_file1.copy())
    recharge.append(rech_file1.copy())
    tmax25.append(tmax25_file1.copy())
    tmax30.append(tmax30_file1.copy())
    recharge_adj.append(rech_adj_file1.copy())


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
recharge = processing(recharge, "recharge")
tmax25 = processing(tmax25, "Tmax25[n]")
tmax30 = processing(tmax30, "Tmax30[n]")
recharge_adj = processing(recharge_adj, "recharge_adjust")
recharge_adj= recharge_adj.dropna(axis=1, how='all')
#print(recharge_adj)
#print(recharge)
data = pre.join([ pre_s, pre_w, recharge,recharge_adj, tmax25, tmax30])  #recharge_adj, tmax25, pre_s, pre_w,
#print(data)


#######--------------rcps-----------------#########
meta = pd.read_csv("/work/malla/ww_leipzig/MET_list.txt",sep=" ")
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


data.to_csv(outpath + "AllMETfiles_1971_2000_rcp_indicators.csv")
