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


outpath = "/work/malla/sachsen_output/plots_andreas/"
data = pd.read_csv("/work/malla/sachsen_output/scatter_plots/data/allMets_allindicators_spmedian.csv")
#print(data)



fig, ax = plt.subplots(figsize=(6,6))

#a1 = ax.scatter( y=data.tmax25_historic, x=data.recharge_adjust_historic, s=10,label="historic")
a = ax.scatter( y=data.tmax25_1_5K, x=data.recharge_adjust_1_5K, s=10,label="1.5 °C")

b = ax.scatter( y=data.tmax25_2K, x=data.recharge_adjust_2K, s=10,label="2 °C",)
c = ax.scatter( y=data.tmax25_3K, x=data.recharge_adjust_3K, s=10,label="3 °C", c='red')

# sns.regplot(x=data.recharge_adjust_1_5K, y=data.tmax25_1_5K,ax=ax,label="1.5 °C",ci=None, scatter_kws={"s": 10}, color="green")
# sns.regplot(x=data.recharge_adjust_2K, y=data.tmax25_2K,ax=ax,label="2 °C",ci=None, scatter_kws={"s": 10})
# ax= sns.regplot(x=data.recharge_adjust_3K, y=data.tmax25_3K,ax=ax,label="3 °C",ci=None, scatter_kws={"s": 10}, color="red", marker="^", line_kws={'linewidth':1})

ax.set_xlabel("recharge [mm/year]")
ax.set_ylabel("Summer days [n/year]")
# ax.set_xlabel("Grundwasserneubildung [mm/Jahr]"

# ax.set_ylabel("Sommertage [n/Jahr]")
ax.set(xlabel ="Recharge", ylabel = "Summerdays", title ='Absolute values')

plt.legend(prop={'size': 12})
plt.setp(ax.spines.values(), linewidth=0.5)
plt.tight_layout()
plt.legend()
#plt.savefig(outpath + "scatterplot_summerdays_recharge_adj_neu.png")

#plt.show()

