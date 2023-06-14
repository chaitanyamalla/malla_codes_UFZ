#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:       plot_aET_pet_obs_Monthly_ts.py
#
#  Created:     Di 15-06-2021
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


inpath = "/work/malla/ww_leipzig/data_obs/csv/"

petfile = "pet_monthly_obs.csv"
pet= pd.read_csv(inpath + petfile)
pet = pet.set_index("month")

aetfile = "aET_monthly_obs.csv"
aet= pd.read_csv(inpath +aetfile)
aet = aet.set_index("month")

aetpetfile = "aETdivpet_monthly_obs.csv"
aetpet = pd.read_csv(inpath +aetpetfile)
aetpet = aetpet.set_index("month")
####-----aET and pet-plot------#####

ind= aetpet
ind1 = "aET/pet"

median= ind.median(axis=1)
min1= ind.min(axis=1)
max1= ind.max(axis=1)
mean1 = ind.mean(axis=1)
month = ind.index
q25 = ind.quantile(0.25, axis=1)
q75 = ind.quantile(0.75, axis=1)
year2017 = ind["2017"]
year2018 = ind["2018"]
year2019 = ind["2019"]
print(month)

fig, ax= plt.subplots(figsize=(10,6))

ax.set_title(ind1 +" of monthly sums for years 1951 to 2020")
#ax.set_ylabel("mm/month")
ax.set_xlabel("Months in a Year")
ax.plot(month, year2019, color= "#0E925C", label="2019",ls = '--',linewidth = '2')
ax.plot(month, year2018, color= "#060606", label="2018",ls = '-',linewidth = '2')
ax.plot(month, year2017, color= "#8A8B76", label="2017",ls = '-.',linewidth = '2')

ax.plot(month, max1, color= "#A91E20", label="max", linewidth='0.5')
ax.plot(month, q75, color= "#DF4949", label="q75",linewidth='0.5')

ax.plot(month, median, color="#1B43D6", label="median",linewidth='1')

ax.plot(month, q25, color= "#9CD363", label="q25",linewidth='0.5')
ax.plot(month, min1, color= "#50C512", label="min",linewidth='0.5')

#ax = dataframe.T.boxplot()


ax.fill_between(month, year2018, median,
                where=(year2018> median),
                interpolate=True, alpha=0.25,color="blue", label="Above median")

ax.fill_between(month, year2018, median,
                where=(year2018<= median),
                interpolate=True, alpha=0.25, color="red", label="Below median")

ax.legend()
plt.show()
#fig.savefig(ind1+"_obs_withallyears_monthly.png")
