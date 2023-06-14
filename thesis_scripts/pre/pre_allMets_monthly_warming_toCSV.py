#! /usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------
#  File:        Pre_allMets_degree_monthly_toCSV.py
#
#  Created:     Di 17-06-2021 
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
import glob
import ufz
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr
import xclim as xc 
from xclim import ensembles
outpath= "/work/malla/sachsen_output/monthly/ens_median_monthly/"
inpath="/work/malla/sachsen_input/"

ind="pre"



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

    pre1=[]
    mets=[1,2,7,8,9,10,21,22,23,24,25,26,27,28,29,30,31,35,36,37,40,41,50,51,52,53,54,55,56,57,58,67,68,69,70,71,72,73,74,75,76,77,78,82,83,84,85,86,87]
    ind="pre"
    for met in mets:
        met_id= "met"+'_'+ str(met).zfill(3)
        data = xr.open_dataset(inpath + met_id+"/" + filename)
        data1 = data.resample(time='M').sum()
        gp1= data1.pre.groupby("time.month")
        gpt1 = gp1.mean(dim="time")
        gpt2 = gpt1.where(gpt1>0)
        #gpt3 = gpt2.mean(dim=['latitude', 'longitude'])#.to_dataframe(k)
        pre1.append(gpt2)

    combi = xr.concat(pre1,dim='met')
    pre_h = combi.median(dim="met")
    pre_h.to_netcdf(outpath+ind+"/"+"ensmedian_monthly_"+filename)
    pre_h1= pre_h.mean(dim=["latitude","longitude"]).to_dataframe(k)
    return pre_h1


pre_hist = readfile("pre_historic.nc",1)
pre_1_5K = readfile("pre_1_5K.nc",2)
pre_2K = readfile("pre_2K.nc",3)
pre_3K = readfile("pre_3K.nc",4)


result= pre_hist.join([pre_1_5K,pre_2K,pre_3K])
result.to_csv(outpath+"pre_monthly_ensmedian.csv")
print(result.sum(axis=0))

