#! /usr/bin/env python
# -*- coding: utf-8 -*-




# --------------------------------------------------
#  File:        plot_spatial_pre_allMets_warming.py
#
#  Created:     Mo 30-08-2021 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce spatial plots of 30 years average of each Met and then average of all METS  with single indicator
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------

import glob
import xclim as xc
import xarray as xr
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from xclim import ensembles
import dask.array
from dask.distributed import Client
import sys



 


# ens_1_5K = ensembles.create_ensemble(glob.glob("/work/malla/sachsen_input/*/pre_1_5K.nc")).load()

# ens_1_5K1 = ens_1_5K.chunk({"time":100, "realization":1})

# ens1 = ens_1_5K1.resample(time="Y").sum()
# ens2 = ens1.mean(dim=["time","realization"])
# ens2.pre.plot(cmap = mpl.cm.hot_r)
# plt.show()


#data_set = glob.glob("/work/malla/sachsen_input/*/pre_1_5K.nc")
#data_set = glob.glob("/work/malla/sachsen_input/met_00[12]/pre_1_5K.nc")
output = "/work/malla/sachsen_output/spatial/data/pre/"



def process(filename):
    filename= filename
    data_set = glob.glob("/work/malla/sachsen_input/*/"+ filename)
    data = []
    for d in data_set:
        ds = xr.open_dataset(d)
        ds1 = ds.resample(time="Y").sum()
        ds2 = ds1.mean("time")
        data.append(ds2)
    j = sum(data)/len(data)

    return j


pre_1_5K = process("pre_1_5K.nc")
pre_2K = process("pre_2K.nc")
pre_3K = process ("pre_3K.nc")


pre_1_5K.to_netcdf(output + "pre_1_5K_ensemblemean.nc")
pre_2K.to_netcdf(output + "pre_2K_ensemblemean.nc")
pre_3K.to_netcdf(output + "pre_3K_ensemblemean.nc")

