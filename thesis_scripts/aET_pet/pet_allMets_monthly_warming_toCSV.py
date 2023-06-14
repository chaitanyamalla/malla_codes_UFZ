#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:        pet_allMets_monthly_warming_toCSV.py
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


#outpath= "/work/malla/sachsen_output/monthly/csv/"
outpath= "/work/malla/sachsen_output/monthly/ens_median_monthly/"
inpath="/work/malla/sachsen_input/"
#mets=[1,2,7,8,9,10,21,22,23,24,25,26,27,28,29,30,31,35,36,37,40,41,50,51,52,53,54,55,56,57,58,67,68,69,70,71,72,73,74,75,76,77,78,82,83,84,85,86,87]
#mets=[1,2]

# pet_hist=[]
# pet_1_5K =[]
# pet_2K =[]
# pet_3K= []


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
    ind="aET_pet" 
    for met in mets:
        met_id= "met"+'_'+ str(met).zfill(3)

        data = xr.open_dataset(inpath + met_id+"/" + filename)
        #data = data.mean(dim= ['latitude', 'longitude'])
        data1 = data.resample(time='M').sum()
        gp1= data1.pet.groupby("time.month")
        gpt1 = gp1.mean(dim ="time")#.to_dataframe(met_id)
        gpt2 = gpt1.where(gpt1>0)
        empty.append(gpt2)

    combi = xr.concat(empty,dim='met')
    r_h = combi.median(dim="met")
    r_h.to_netcdf(outpath+ind+"/"+"ensmedian_monthly_"+filename)
    r_h1= r_h.mean(dim=["latitude","longitude"]).to_dataframe(k)
    return r_h1






a_hist= readfile("pet_historic.nc",1)
a_1_5K = readfile("pet_1_5K.nc",2)
a_2K = readfile("pet_2K.nc",3)
a_3K = readfile("pet_3K.nc",4)


result= a_hist.join([a_1_5K,a_2K,a_3K])
result.to_csv(outpath+"pet_monthly_ensmedian.csv")
print(result)
