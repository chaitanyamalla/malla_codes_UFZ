#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:        scatterplot_pre_recharge_warminglevels_allMets.py 
#
#  Created:     Di 18-06-2021 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce scatterplot for 3 warming periods for 49 RCP 8.5 MET files with two indicator 
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


outpath = "/work/malla/sachsen_output/scatter_plots/plots/"
data = pd.read_csv("/work/malla/sachsen_output/scatter_plots/data/allMets_allindicators_spmean.csv", index_col=[0])
#print(data)


abs_tmax25_1_5K = data.tmax25_1_5K-data.tmax25_historic
abs_tmax25_2K = data.tmax25_2K-data.tmax25_historic
abs_tmax25_3K = data.tmax25_3K-data.tmax25_historic

abs_rech_adj_1_5K = data.recharge_adjust_1_5K - data.recharge_adjust_historic
abs_rech_adj_2K = data.recharge_adjust_2K - data.recharge_adjust_historic
abs_rech_adj_3K = data.recharge_adjust_3K - data.recharge_adjust_historic

rel_tmax25_1_5K = (abs_tmax25_1_5K /data.tmax25_historic)*100
rel_tmax25_2K = (abs_tmax25_2K /data.tmax25_historic)*100
rel_tmax25_3K = (abs_tmax25_3K /data.tmax25_historic)*100

rel_rech_adj_1_5K = (abs_rech_adj_1_5K / data.recharge_adjust_historic)*100
rel_rech_adj_2K = (abs_rech_adj_2K / data.recharge_adjust_historic)*100
rel_rech_adj_3K = (abs_rech_adj_3K / data.recharge_adjust_historic)*100


# # ######################################################
# # #---------------abs----------------------------------
# # #-----------------------------------------------------

fig, ax = plt.subplots(figsize=(7,7))

a = ax.scatter( y=abs_tmax25_1_5K, x=abs_rech_adj_1_5K, s=12,label="1.5K",c='green')
b = ax.scatter( y=abs_tmax25_2K, x=abs_rech_adj_2K, s=12,label="2K",c='blue')
c = ax.scatter( y=abs_tmax25_3K, x=abs_rech_adj_3K, s=12,label="3K", c='red',marker="^")

d1=ax.scatter(y=abs_tmax25_1_5K.median(),x=abs_rech_adj_1_5K.median(),s=70,edgecolor='black', linewidth=0.5, facecolor='green', marker="o")
d2=ax.scatter(y=abs_tmax25_2K.median(),x=abs_rech_adj_2K.median(),s=70,edgecolor='black', linewidth=0.5, marker="o")
d3=ax.scatter(y=abs_tmax25_3K.median(),x=abs_rech_adj_3K.median(),s=70,edgecolor='black', linewidth=0.5, marker="^",c="red")
# sns.regplot(x=abs_rech_adj_1_5K, y=abs_tmax25_1_5K,ax=ax,label="1.5 °C",ci=None, scatter_kws={"s": 10}, color="green",line_kws={'linewidth':1})
# sns.regplot(x=abs_rech_adj_2K, y=abs_tmax25_2K,ax=ax,label="2 °C",ci=None, scatter_kws={"s": 10},line_kws={'linewidth':1})
# ax= sns.regplot(x=abs_rech_adj_3K, y=abs_tmax25_3K,ax=ax,label="3 °C",ci=None, scatter_kws={"s": 10}, color="red", marker="^", line_kws={'linewidth':1})

ax.set(xlabel ="Δ Recharge [mm/year]", ylabel = "Δ Summerdays [n/year]", title ='Absolute change')
plt.legend()
ax.set_xlabel("Δ Recharge [mm/year]")
ax.set_ylabel("Δ Summer days [n/year]")
# ax.set_xlabel("Δ Grundwasserneubildung [mm/Jahr]")
# ax.set_ylabel("Δ Sommertage [n/Jahr]")
plt.legend(prop={'size': 12})
plt.setp(ax.spines.values(), linewidth=0.5)
plt.tight_layout()

# plt.legend()
plt.savefig(outpath + "scatter_summerdays_recharge_adjust_absolutechange_spmean_new.png")

plt.show()

# ######################################################
# #---------------relative----------------------------------
# #-----------------------------------------------------

# fig, ax = plt.subplots(figsize=(7,7))

# a = ax.scatter( y=rel_tmax25_1_5K, x=rel_rech_adj_1_5K, s=10,label="1.5K")
# b = ax.scatter( y=rel_tmax25_2K, x=rel_rech_adj_2K, s=10,label="2K",)
# c = ax.scatter( y=rel_tmax25_3K, x=rel_rech_adj_3K, s=10,label="3K", c='black')

# #ax.set_xlabel("recharge [mm/year]")
# #ax.set_ylabel("Summer days [n/year]")
# ax.set_xlabel(" Grundwasserneubildung [%]")
# ax.set_ylabel(" Sommertage [%]")

# plt.legend()
# plt.savefig(outpath + "scatterplot_summerdays_recharge_adj_relativechange.png")

# #plt.show()





meta                    = pd.read_csv("/work/malla/sachsen_output/RCP8.5_EurCordex_list.csv", sep=";")
met_ids                 = np.sort(pd.unique(meta["met_id"]))

mets = pd.DataFrame(met_ids, columns = ['mets'])
#data = data.reset_index()
data1 = data.join(mets)

#data1 = data.reset_index(drop=True)
print(data1)
#for col in data.columns:
#    print(col)

data1.to_csv("/work/malla/sachsen_output/scatter_plots/data/tmax25_recharge_adjust_scatterdata.csv")
