#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:       plot_pet_div_aET_rcps_ts.py
#
#  Created:     Mi 02-06-2021
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

#data = pet_file.div(aET_file)
data = aET_file.div(pet_file)
#print(pet_file)
#print(aET_file)
#print(data)

#data.T.boxplot()
#plt.show()
#data = data.drop_index()
meta = pd.read_csv("/work/malla/ww_leipzig/MET_list.txt",sep=" ")
met_ids = np.sort(pd.unique(meta["met_id"]))
gcms = np.sort(pd.unique(meta["gcm"]))
rcms = np.sort(pd.unique(meta["inst.rcm"]))
rcps = pd.Series(meta["rcp"], dtype="category")
hms= ['mHM']
data2 = pd.DataFrame(rcps, columns = ['rcp'])
data1 = data.T.reset_index()

data_rcp= data1.join(data2)

data_rcp26 = data_rcp.loc[data_rcp['rcp'] == 'rcp26']
data_rcp45 = data_rcp.loc[data_rcp['rcp'] == 'rcp45']
data_rcp85 = data_rcp.loc[data_rcp['rcp'] == 'rcp85']

df_rcp26 = data_rcp26.drop(columns=["rcp"]).set_index('index').T
df_rcp45 = data_rcp45.drop(columns=["rcp"]).set_index('index').T
df_rcp85 = data_rcp85.drop(columns=["rcp"]).set_index('index').T


##---------------------df_rcp26-----------##


df_rcp26_q75 = df_rcp26.quantile(q=0.75, axis=1, numeric_only=False).astype(float).rolling(30, center=True).mean()
df_rcp26_median = df_rcp26.median(axis=1).astype(float).rolling(30, center=True).mean()
df_rcp26_q25 = df_rcp26.quantile(q=0.25, axis=1, numeric_only=False).astype(float).rolling(30, center=True).mean()
year_rcp26 = df_rcp26.index.astype(float)



##--------------------df_rcp45------------##

df_rcp45_q75 = df_rcp45.quantile(q=0.75, axis=1, numeric_only=False).astype(float).rolling(30, center=True).mean()
df_rcp45_median = df_rcp45.median(axis=1).astype(float).rolling(30, center=True).mean()
df_rcp45_q25 = df_rcp45.quantile(q=0.25, axis=1, numeric_only=False).astype(float).rolling(30, center=True).mean()
year_rcp45 = df_rcp45.index.astype(float)

##-------------------df_rcp85------------##

df_rcp85_q75 = df_rcp85.quantile(q=0.75, axis=1, numeric_only=False).astype(float).rolling(30, center=True).mean()
df_rcp85_median = df_rcp85.median(axis=1).astype(float).rolling(30, center=True).mean()
df_rcp85_q25 = df_rcp85.quantile(q=0.25, axis=1, numeric_only=False).astype(float).rolling(30, center=True).mean()
year_rcp85 = df_rcp85.index.astype(float)



fig, (ax1, ax2, ax3)= plt.subplots(3,1,figsize=(10,10))

#fig.suptitle('(Actual / Potential) yearly Evapotranspiration timeseries on 88 Models', fontsize=12,fontweight='bold',  y=0.92)
#ax.set_title(indicator+" yearly sum analysis on Models with RCP 26")
ax1.set_ylabel("aET/pet")
#ax1.set_title("rcp26")
ax1.plot(year_rcp26, df_rcp26_q75, color= "#F9480B", label=" q75",linewidth='1')
ax1.plot(year_rcp26, df_rcp26_median, color= "#761675", label=" median",linewidth='1')
ax1.plot(year_rcp26, df_rcp26_q25, color= "#095636", label=" q25",linewidth='1')
ax1.set_ylim(0.6, 0.7)

ax1.text(.5,.9,'RCP 26',
        horizontalalignment='center',
        transform=ax1.transAxes)

ax1.fill_between(year_rcp26, df_rcp26_q75, df_rcp26_q25,interpolate=True, alpha=0.25,color="green", label="IQR")
ax1.legend()


#ax2.set_title("rcp45")
ax2.set_ylabel("aET/pet")
ax2.plot(year_rcp45, df_rcp45_q75, color= "#F9480B", label=" q75",linewidth='1')
ax2.plot(year_rcp45, df_rcp45_median, color= "#761675", label=" median",linewidth='1')
ax2.plot(year_rcp45, df_rcp45_q25, color= "#095636", label=" q25",linewidth='1')
ax2.set_ylim(0.6, 0.7)
ax2.fill_between(year_rcp45, df_rcp45_q75, df_rcp45_q25,
                 interpolate=True, alpha=0.25,color="skyblue", label="IQR")
ax2.text(.5,.9,'RCP 45',
        horizontalalignment='center',
        transform=ax2.transAxes)
ax2.legend()


#ax3.set_title("rcp85")
ax3.set_ylabel("aET/pet")
ax3.text(.5,.9,'RCP 85',
        horizontalalignment='center',
        transform=ax3.transAxes)
ax3.plot(year_rcp85, df_rcp85_q75, color= "#F9480B", label=" q75",linewidth='1')
ax3.plot(year_rcp85, df_rcp85_median, color="#761675", label=" median",linewidth='1')
ax3.plot(year_rcp85, df_rcp85_q25, color= "#095636", label=" q25",linewidth='1')
ax3.set_ylim(0.6, 0.7)
ax3.fill_between(year_rcp85, df_rcp85_q75, df_rcp85_q25,
                 interpolate=True, alpha=0.25,color="orange", label="IQR")

ax3.legend()




ax1.xaxis.set_major_locator(MultipleLocator(10))
# #ax.xaxis.set_major_formatter('{x:.0f}')
ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
ax1.tick_params(which='minor', length=5)
ax1.tick_params(which='major', length=9)

ax2.xaxis.set_major_locator(MultipleLocator(10))
# #ax.xaxis.set_major_formatter('{x:.0f}')
ax2.xaxis.set_minor_locator(AutoMinorLocator(10))
ax2.tick_params(which='minor', length=5)
ax2.tick_params(which='major', length=9)

ax3.xaxis.set_major_locator(MultipleLocator(10))
# #ax.xaxis.set_major_formatter('{x:.0f}')
ax3.xaxis.set_minor_locator(AutoMinorLocator(10))
ax3.tick_params(which='minor', length=5)
ax3.tick_params(which='major', length=9)




plt.text(x=0.5, y=0.91, s='(Actual / Potential) yearly Evapotranspiration timeseries on 88 Models', fontfamily="Comic Sans MS", fontsize=12, ha="center", transform=fig.transFigure)
plt.show()

#fig.savefig(inpath+"aET_div_pet_rollingmean30yrs_RCP_ts.png")
