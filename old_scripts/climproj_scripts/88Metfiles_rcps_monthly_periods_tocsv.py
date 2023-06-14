#! /usr/bin/env python
# -*- coding: utf-8 -*-




# --------------------------------------------------
#  File:        plot_88Metfiles_rcps_monthly_periods_ts.py
#
#  Created:     Do 03-06-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce Monthly Timeseries for different climate periods 1971-2000, 2021-2050, 2071-2099 for all 88 MET files   with single indicator for HICAM climate ensemble evaluation
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



outpath= "/work/malla/ww_leipzig/data_1971_2099/output_1971_2099/88_METfiles_csv/"
inpath="/work/malla/ww_leipzig/data_1971_2099/input_1971_2099/"
met_start=1
met_end=88

# ####################-----------  aET ----------------################################

# aET_data_1971_2000 = []
# aET_data_2021_2050 = []
# aET_data_2071_2099 = []



# for met in range(met_start, met_end+1):
#     met_id="met"+'_'+ str(met).zfill(3)

    

#     aET_file ="/aET_ug.nc"
#     data_aET = xr.open_dataset(inpath + met_id + aET_file)
#     #data_aET = xr.open_dataset(inpath + met_id + aET_file)


#     data1= data_aET.sel(time=slice('1971-01-01', '2000-12-31')).median(dim= ['lat','lon'])
#     data2= data_aET.sel(time=slice('2021-01-01', '2050-12-31')).median(dim= ['lat','lon'])
#     data3= data_aET.sel(time=slice('2071-01-01', '2099-12-31')).median(dim= ['lat','lon'])
   

#     gp1 = data1.aET
#     gpt1 = gp1.groupby("time.month")
#     aET1 = gpt1.mean(dim="time").to_dataframe(met_id)
    
#     gp2 = data2.aET
#     gpt2 = gp2.groupby("time.month")
#     aET2 = gpt2.mean(dim="time").to_dataframe(met_id)

#     gp3 = data3.aET
#     gpt3 = gp3.groupby("time.month")
#     aET3 = gpt3.mean(dim="time").to_dataframe(met_id)

#     aET_data_1971_2000.append(aET1)
#     aET_data_2021_2050.append(aET2)
#     aET_data_2071_2099.append(aET3)
    
# aET_data_1971_2000 = pd.concat(aET_data_1971_2000, axis=1)
# aET_data_2021_2050 = pd.concat(aET_data_2021_2050, axis=1)
# aET_data_2071_2099 = pd.concat(aET_data_2071_2099, axis=1)
# #print(data_1971_2000)
# #print(data_2021_2050)

# aET_data_1971_2000.to_csv(outpath +'88MetfilesMonthly_clim_periods_csv/'
# +'aET_1971_2000_months_allMetfiles.csv')
# aET_data_2021_2050.to_csv(outpath +'88MetfilesMonthly_clim_periods_csv/'
# +'aET_2021_2050_months_allMetfiles.csv')
# aET_data_2071_2099.to_csv(outpath +'88MetfilesMonthly_clim_periods_csv/'
# +'aET_2071_2099_months_allMetfiles.csv')


####################-----------  pet  ----------------################################

pet_data_1971_2000 = []
pet_data_2021_2050 = []
pet_data_2071_2099 = []

for met in range(met_start, met_end+1):
    met_id="met"+'_'+ str(met).zfill(3)

    
    pet_file ="/pet_ug.nc"
    data_pet = xr.open_dataset(inpath + met_id + pet_file)
    data_pet = data_pet.resample(time= 'M').sum()
    
    
    data1= data_pet.sel(time=slice('1971-01-01', '2000-12-31')).median(dim= ['latitude','longitude'])
    data2= data_pet.sel(time=slice('2021-01-01', '2050-12-31')).median(dim= ['latitude','longitude'])
    data3= data_pet.sel(time=slice('2071-01-01', '2099-12-31')).median(dim= ['latitude','longitude'])

    gp1 = data1.pet
    gpt1 = gp1.groupby("time.month")
    pet1 = gpt1.mean(dim="time").to_dataframe(met_id)
    
    
    gp2 = data2.pet
    gpt2 = gp2.groupby("time.month")
    pet2 = gpt2.mean(dim="time").to_dataframe(met_id)
   

    gp3 = data3.pet
    gpt3 = gp3.groupby("time.month")
    pet3 = gpt3.mean(dim="time").to_dataframe(met_id)

    
    pet_data_1971_2000.append(pet1)
    pet_data_2021_2050.append(pet2)
    pet_data_2071_2099.append(pet3)


pet_data_1971_2000 = pd.concat(pet_data_1971_2000, axis=1)
pet_data_2021_2050 = pd.concat(pet_data_2021_2050, axis=1)
pet_data_2071_2099 = pd.concat(pet_data_2071_2099, axis=1)
#print(pet_data_1971_2000)
#print(pet_data_2021_2050)

pet_data_1971_2000.to_csv(outpath +'88MetfilesMonthly_clim_periods_csv/'
+'pet_1971_2000_months_allMetfiles.csv')
pet_data_2021_2050.to_csv(outpath +'88MetfilesMonthly_clim_periods_csv/'
+'pet_2021_2050_months_allMetfiles.csv')
pet_data_2071_2099.to_csv(outpath +'88MetfilesMonthly_clim_periods_csv/'
+'pet_2071_2099_months_allMetfiles.csv')

