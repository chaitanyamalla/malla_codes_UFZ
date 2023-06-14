#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:       tmax30_spatial_ensemble_mean_toNC.py
#
#  Created:     Mo 06-09-2021 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce spatial Netcdf file  of 30 years average of each Met and then average of all METS  with single indicator
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


inpath= "/work/malla/sachsen_input/"
outpath="/work/malla/sachsen_output/spatial/data/"
ind="tmax"


def process(filename):
    ens = ensembles.create_ensemble(glob.glob(inpath+"*/"+filename))
    ensx = ens.where(ens>30)
    ens1= ensx.resample(time="Y").count() 
    ens2= ens1.where(ens1>0)
    ens3= ens2.mean(dim="time")                                
    ens4= ens3.median(dim="realization")
    ens3.to_netcdf(outpath+ind+"/"+"ensemble30_"+filename)
    ens4.to_netcdf(outpath+ind+"/"+"ensemblemedian30_"+filename)
    return ens4
    

d1= process(ind+"_historic.nc")
d2= process(ind+"_1_5K.nc")
d3= process(ind+"_2K.nc")
d4= process(ind+"_3K.nc")


# output = "/work/malla/sachsen_output/spatial/data/tmax/"
# def process(filename):
#     filename= filename
#     data_set = glob.glob("/work/malla/sachsen_input/*/"+ filename)
#     data = []
#     for d in data_set:
#         ds = xr.open_dataset(d)
#         d = ds.where(ds > 30)
#         ds1 = d.resample(time="Y").count()
#         ds2 = ds1.mean("time")
#         data.append(ds2)
#     j = sum(data)/len(data)

#     return j


# t_hist = process("tmax_historic.nc")
# t_1_5K = process("tmax_1_5K.nc")
# t_2K = process("tmax_2K.nc")
# t_3K = process ("tmax_3K.nc")

# t_hist.to_netcdf(output + "tmax30_historic_ensemblemean.nc")
# t_1_5K.to_netcdf(output + "tmax30_1_5K_ensemblemean.nc")
# t_2K.to_netcdf(output + "tmax30_2K_ensemblemean.nc")
# t_3K.to_netcdf(output + "tmax30_3K_ensemblemean.nc")
