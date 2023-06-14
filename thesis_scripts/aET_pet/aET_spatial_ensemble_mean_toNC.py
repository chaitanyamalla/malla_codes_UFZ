#! /usr/bin/env python
# -*- coding: utf-8 -*-


# --------------------------------------------------
#  File:        aET_spatial_ensemble_mean_toNC.py
#
#  Created:     Di 07-09-2021 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce spatial plot data of 30 years average of each Met and then average of all METS  of single indicator for different warming periods
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------

import glob
import xarray as xr
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xclim as xc
from xclim import ensembles




inpath= "/work/malla/sachsen_input/"
outpath="/work/malla/sachsen_output/spatial/data/"
ind="aET"


def process(filename):
    ens = ensembles.create_ensemble(glob.glob(inpath+"*/"+filename))
    ens1= ens.resample(time="Y").sum() 
    ens2= ens1.where(ens1>0)
    ens3= ens2.mean(dim="time")                                
    ens4= ens3.median(dim="realization")
    ens3.to_netcdf(outpath+ind+"/"+"ensemble_"+filename)
    ens4.to_netcdf(outpath+ind+"/"+"ensemblemedian_"+filename)
    return ens4
    

d1= process(ind+"_historic.nc")
d2= process(ind+"_1_5K.nc")
d3= process(ind+"_2K.nc")
d4= process(ind+"_3K.nc")



















# output = "/work/malla/sachsen_output/spatial/data/aET_pet/"

# def process(filename):
#     filename= filename
#     data_set = glob.glob("/work/malla/sachsen_input/*/"+ filename)
#     data = []
#     for d in data_set:
#         ds = xr.open_dataset(d)
#         ds1 = ds.resample(time="Y").sum()
#         ds2 = ds1.mean("time")
#         data.append(ds2)
#     j = sum(data)/len(data)

#     return j


# aET_hist = process("aET_historic.nc")
# aET_1_5K = process("aET_1_5K.nc")
# aET_2K = process("aET_2K.nc")
# aET_3K = process ("aET_3K.nc")

# aET_hist.to_netcdf(output + "aET_historic_ensemblemean.nc")
# aET_1_5K.to_netcdf(output + "aET_1_5K_ensemblemean.nc")
# aET_2K.to_netcdf(output + "aET_2K_ensemblemean.nc")
# aET_3K.to_netcdf(output + "aET_3K_ensemblemean.nc")

