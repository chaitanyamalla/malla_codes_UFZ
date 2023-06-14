#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:        recharge_allMets_monthly_warming_toCSV.py
#
#  Created:     Di 18-06-2021 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce Monthly Timeseries for different warming periods for 49 RCP 8.5 MET files   with single indicator for HICAM climate ensemble evaluation
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


outpath= "/work/malla/sachsen_output/monthly/csv/"
inpath="/work/malla/sachsen_input/"
mets=[1,2,7,8,9,10,21,22,23,24,25,26,27,28,29,30,31,35,36,37,40,41,50,51,52,53,54,55,56,57,58,67,68,69,70,71,72,73,74,75,76,77,78,82,83,84,85,86,87]
#mets=[1,2]

rech_hist=[]
rech_1_5K =[]
rech_2K =[]
rech_3K= []


def readfile(filename):
    
    filename =filename
    data = xr.open_dataset(inpath + met_id + filename)

    data= data.mean(dim= ['lat', 'lon'])
    data1 = data.resample(time='M').sum()
    
    gp1= data1.recharge
    gpp1 = gp1.groupby("time.month")
    gpt1 = gpp1.mean(dim ="time").to_dataframe(met_id)

    return gpt1




for met in mets:
    
    met_id= "met"+'_'+ str(met).zfill(3)

    r_hist=readfile("/recharge_historic.nc")
    r_1_5K = readfile("/recharge_1_5K.nc")
    r_2K = readfile("/recharge_2K.nc")
    r_3K = readfile("/recharge_3K.nc")

    rech_hist.append(r_hist.copy())
    rech_1_5K.append(r_1_5K.copy())
    rech_2K.append(r_2K.copy())
    rech_3K.append(r_3K.copy())

rech_hist = pd.concat(rech_hist, axis=1)
rech_1_5K = pd.concat(rech_1_5K, axis=1)
rech_2K = pd.concat(rech_2K, axis=1)
rech_3K = pd.concat(rech_3K, axis=1)


rech_3K.to_csv(outpath +'rech_3K_monthly.csv')
rech_2K.to_csv(outpath +'rech_2K_monthly.csv')
rech_1_5K.to_csv(outpath +'rech_1_5K_monthly.csv')
rech_hist.to_csv(outpath +'rech_historic_monthly.csv')
