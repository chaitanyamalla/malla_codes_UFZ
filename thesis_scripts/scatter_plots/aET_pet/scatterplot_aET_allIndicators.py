#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:        scatterplot_aET_allIndicators.py 
#
#  Created:     Do 06-10-2021 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce scatterplot for 49 RCP 8.5 MET files with two indicator 
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



outpath = "/work/malla/sachsen_output/scatter_plots/plots/aET_pet/"
data = pd.read_csv("/work/malla/sachsen_output/scatter_plots/data/allMets_allindicators_spmean.csv")
#print(data)
#ind1="tmax25"
ind1="aET"
ind2="recharge_adjust"


fig, ax = plt.subplots(figsize=(6,6))
a1 = ax.scatter( y=data[ind1+"_historic"], x=data[ind2+"_historic"], s=12,label="historic",c="c")
a = ax.scatter( y=data[ind1+"_1_5K"], x=data[ind2+"_1_5K"], s=12,label="1.5K",c="g")
b = ax.scatter( y=data[ind1+"_2K"], x=data[ind2+"_2K"], s=12,label="2K",c="b")
c = ax.scatter( y=data[ind1+"_3K"], x=data[ind2+"_3K"], s=12,label="3K",marker="v",c="r")
ax.set_xlabel("Annual Recharge [mm/year]")
ax.set_ylabel("Actual Evapotranspiration [mm/year]")

plt.legend(prop={'size': 12})
plt.setp(ax.spines.values(), linewidth=0.5)
plt.tight_layout()
plt.savefig(outpath+ind1+"_"+ind2+"_abs.png")
plt.show()



ind1_abs1 = data[ind1+"_1_5K"]-data[ind1+"_historic"]
ind1_abs2 = data[ind1+"_2K"]-data[ind1+"_historic"]
ind1_abs3 = data[ind1+"_3K"]-data[ind1+"_historic"]

ind2_abs1 = data[ind2+"_1_5K"]-data[ind2+"_historic"]
ind2_abs2 = data[ind2+"_2K"]-data[ind2+"_historic"]
ind2_abs3 = data[ind2+"_3K"]-data[ind2+"_historic"]


ind1_rel1=(ind1_abs1/data[ind1+"_historic"])*100
ind1_rel2=(ind1_abs2/data[ind1+"_historic"])*100
ind1_rel3=(ind1_abs3/data[ind1+"_historic"])*100

ind2_rel1=(ind2_abs1/data[ind2+"_historic"])*100
ind2_rel2=(ind2_abs2/data[ind2+"_historic"])*100
ind2_rel3=(ind2_abs3/data[ind2+"_historic"])*100

###----------absolute change plot------------------------------
fig, ax = plt.subplots(figsize=(6,6))
a = ax.scatter( y=ind1_abs1, x=ind2_abs1, s=12,label="1.5K",c="g")
b = ax.scatter( y=ind1_abs2, x=ind2_abs2, s=12,label="2K",c="b")
c = ax.scatter( y=ind1_abs3, x=ind2_abs2, s=12,label="3K",marker="v",c="r")
ax.set_ylabel("aET Absolute change [mm/year]")
ax.set_xlabel("Recharge Absolute change [mm/year]")
plt.legend(prop={'size': 12})
plt.setp(ax.spines.values(), linewidth=0.5)
plt.tight_layout()
plt.savefig(outpath+ind1+"_"+ind2+"_abschange.png")
plt.show()

#############------relative change plot-----------------------------
fig, ax = plt.subplots(figsize=(6,6))
a = ax.scatter( y=ind1_rel1, x=ind2_rel1, s=12,label="1.5K",c="g")
b = ax.scatter( y=ind1_rel2, x=ind2_rel2, s=12,label="2K",c="b")
c = ax.scatter( y=ind1_rel3, x=ind2_rel2, s=12,label="3K",marker="v",c="r")
ax.set_ylabel("Actual Evapotranspiration(aET) [%]")
ax.set_xlabel("Recharge [%]")
plt.legend(prop={'size': 12})
plt.setp(ax.spines.values(), linewidth=0.5)
plt.tight_layout()
plt.savefig(outpath+ind1+"_"+ind2+"_relchange.png")
plt.show()
