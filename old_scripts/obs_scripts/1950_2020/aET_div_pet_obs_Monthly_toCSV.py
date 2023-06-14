#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:       plot_aET_div_pet_obs_Monthly_ts.py
#
#  Created:     Mi 15-06-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: ploting single graph of aET/pet for Obs data 1951-2020. 
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

data = []
inpath= "/work/malla/ww_leipzig/data_obs/data_obs_neu/"

###########-----------aET--------------##########


aET_file ="aET_ug_monsum_1951-2020.nc"
data_aET = xr.open_dataset(inpath + aET_file)
nc1 = data_aET.aET.median(dim=['lat', 'lon'])
dataframe= nc1.groupby(data_aET["time.month"]).min().to_dataframe("min")

for year, yearda in nc1.groupby(nc1["time.year"]):
    dataframe[year] = pd.Series(index=yearda["time"].dt.month, data=yearda.values)
dataframe.columns = dataframe.columns.map(str)

dataframe = dataframe.drop("min", 1)

###------pet------#####

pet_file = "pet_ug_monsum_1951-2020.nc"
data_pet = xr.open_dataset(inpath + pet_file)
nc2 = data_pet.pet.median(dim=["latitude", "longitude"])

dataframe2= nc2.groupby(data_pet["time.month"]).min().to_dataframe("min")
for year, yearda in nc2.groupby(nc2["time.year"]):
    dataframe2[year] = pd.Series(index=yearda["time"].dt.month, data=yearda.values)
dataframe2.columns = dataframe2.columns.map(str)

dataframe2 = dataframe2.drop("min", 1)


#dataframe.to_csv("/work/malla/ww_leipzig/data_obs/csv/aET_monthly_obs.csv")
#dataframe2.to_csv("/work/malla/ww_leipzig/data_obs/csv/pet_monthly_obs.csv")

#print(dataframe)
#print(dataframe2)

aETdivpet = dataframe.div(dataframe2)
#aETdivpet.to_csv("/work/malla/ww_leipzig/data_obs/csv/aETdivpet_monthly_obs.csv")
#print(aETdivpet)

