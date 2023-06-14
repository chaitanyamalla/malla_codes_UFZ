#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:       plot_pet_div_aET_ts.py
#
#  Created:     Mi 14-05-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: ploting single graph of pet/aET from the 88 METfiles. 
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
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import matplotlib.patches as patches

inpath= "/work/malla/ww_leipzig/data_1971_2099/output_1971_2099/88_METfiles_csv/"

indicator1= "pet"
pet_file = pd.read_csv(inpath + indicator1 +"_allMETfiles.csv")

indicator2= "aET"
aET_file = pd.read_csv(inpath+ indicator2 +"_allMETfiles.csv")

pet_file = pet_file.set_index('year')
aET_file = aET_file.set_index('year')

data = pet_file.div(aET_file)
#print(pet_file)
#print(aET_file)
#print(data)

#data.T.boxplot()
#plt.show()
#data = data.drop_index()

# data_q75 = data.quantile(q=0.75, axis = 1)
# data_median = data.median(axis=1)
# data_q25= data.quantile(q=0.25, axis=1)
# year = data.index.astype(float)


data_q75 = data.quantile(q=0.75, axis = 1).rolling(30, center=True).mean()
data_median = data.median(axis=1).rolling(30, center=True).mean()
data_q25= data.quantile(q=0.25, axis=1).rolling(30, center=True).mean()
year = data.index.astype(float)

print(data_median)

'''------plotting------''' 
fig, ax = plt.subplots(figsize = (10,6))
ax.set_xlabel("year")
ax.set_title("(potential/actual) evapotranspiration of 88 Models")
ax.set_ylabel("pet/aET")
ax.plot(data_q75.index, data_q75, color= "#F9480B", label=" q75",linewidth='1')
ax.plot(data_median.index, data_median, color= "#761675", label=" median",linewidth='1')
ax.plot(data_q25.index, data_q25, color= "#095636", label=" q25",linewidth='1')
ax.fill_between(year, data_q75, data_q25,
                 interpolate=True, alpha=0.25,color="gold", label="IQR")



ax.xaxis.set_major_locator(MultipleLocator(10))
#ax.xaxis.set_major_formatter('{x:.0f}')

ax.xaxis.set_minor_locator(AutoMinorLocator(10))
ax.tick_params(which='minor', length=5)
ax.tick_params(which='major', length=9)


ax.legend()
plt.show()

#fig.savefig(inpath+"pet_div_aET_rollingmean30yrs_ts.png")
