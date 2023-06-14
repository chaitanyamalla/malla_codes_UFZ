#! /usr/bin/env python
# -*- coding: utf-8 -*-




# --------------------------------------------------
#  File:       tmax_30_recharge_allMets_monthly_warming_toCSV.py
#
#  Created:     Di 19-06-2021 
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
#import ufz
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr


#outpath= "/work/malla/sachsen_output/monthly/csv/new/"
outpath= "/work/malla/sachsen_output/monthly/ens_median_monthly/"
inpath="/work/malla/sachsen_input/"
#mets=[1,2,7,8,9,10,21,22,23,24,25,26,27,28,29,30,31,35,36,37,40,41,50,51,52,53,54,55,56,57,58,67,68,69,70,71,72,73,74,75,76,77,78,82,83,84,85,86,87]


def readfile(filename,var):
    if var==1:
        k="historic"
    elif var==2:
        k="1_5K"
    elif var==3:
        k="2K"
    elif var ==4:
        k="3K"
    filename =filename  
    empty=[] 
    mets=[1,2,7,8,9,10,21,22,23,24,25,26,27,28,29,30,31,35,36,37,40,41,50,51,52,53,54,55,56,57,58,67,68,69,70,71,72,73,74,75,76,77,78,82,83,84,85,86,87] 
    ind="tmax" 
    for met in mets:
        met_id= "met"+'_'+ str(met).zfill(3)

        data = xr.open_dataset(inpath + met_id+"/" + filename)
        data= data.where(data > 30)

        data1 = data.resample(time='M').count()
    
        g1 = data1.tmax.groupby("time.month")
        gpt1 = g1.mean(dim ="time")
        gpt2 = gpt1.where(gpt1>0)
        #data2 = dat1.mean(dim= ['latitude', 'longitude']).to_dataframe(met_id)
        empty.append(gpt2)

    combi = xr.concat(empty,dim='met')
    r_h = combi.median(dim="met")
    r_h.to_netcdf(outpath+ind+"/"+"ensmedian_monthly_heatdays_"+filename)
    r_h1= r_h.mean(dim=["latitude","longitude"]).to_dataframe(k)
    return r_h1




t_hist = readfile("tmax_historic.nc",1)
t_1_5K = readfile("tmax_1_5K.nc",2) 
t_2K = readfile("tmax_2K.nc",3)
t_3K = readfile("tmax_3K.nc",4)


result= t_hist.join([t_1_5K,t_2K,t_3K])
result.to_csv(outpath+"tmax30_monthly_ensmedian.csv")
print(result)

