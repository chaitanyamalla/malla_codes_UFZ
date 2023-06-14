#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:        allMets_allindicators_tmax25_recharge_toCSV.py 
#
#  Created:     Sa 25-06-2021 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce csv  for 3 warming periods CSV for 49 RCP 8.5 MET files with all indicator 
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
from pandas import DataFrame


def read_data(VAR,filename):
    ls=[]
    for met_id in mets:
        tmp_data=ufz.readnetcdf("{:}/met_{:}/{:}".format(inpath,str(met_id).zfill(3),filename), var=VAR)
        tmp_data=float(tmp_data[0][0])
        ls.append(tmp_data)
    return ls




if __name__ == '__main__':

    inpath="/work/malla/sachsen_output/scatter_data/spmean/"
    mets=[1,2,7,8,9,10,21,22,23,24,25,26,27,28,29,30,31,35,36,37,40,41,50,51,52,53,54,55,56,57,58,67,68,69,70,71,72,73,74,75,76,77,78,82,83,84,85,86,87]

    data=[]

    listA = np.array(['historic','1_5K', '2K', '3K'], dtype=np.str)
    for i in range(4):
        warmperiod= listA[i]

    
        save_results_to = '/work/malla/sachsen_output/scatter_plots/'


        filename1="pre_{:}_ysum_timmean_fldmean.nc".format(warmperiod)
        data_pre=read_data(VAR="pre",filename=filename1)
        da = DataFrame (data_pre,columns=["pre_"+warmperiod])
        data.append(da)
        


        filename2="tmax_{:}_gtc25_ysum_timmean_fldmean.nc".format(warmperiod)
        data_tmax25=read_data(VAR="tmax",filename=filename2)
        df = DataFrame (data_tmax25,columns=["tmax25_"+warmperiod])
        data.append(df)
        
        filename3="tmax_{:}_gtc30_ysum_timmean_fldmean.nc".format(warmperiod)
        data_tmax30=read_data(VAR="tmax",filename=filename3)
        dt = DataFrame (data_tmax30,columns=["tmax30_"+warmperiod])
        data.append(dt)

        filename7="recharge_{:}_ysum_timmean_fldmean.nc".format(warmperiod)
        data_recharge=read_data(VAR="recharge",filename=filename7)
        dj = DataFrame (data_recharge,columns=["recharge_"+warmperiod])
        data.append(dj)

        filename4="recharge_adjust_{:}_ysum_timmean_fldmean.nc".format(warmperiod)
        data_recharge_adj=read_data(VAR="recharge",filename=filename4)
        dr = DataFrame (data_recharge_adj,columns=["recharge_adjust_"+warmperiod])
        data.append(dr)

        
        filename5="aET_{:}_ysum_timmean_fldmean.nc".format(warmperiod)
        data_aET=read_data(VAR="aET",filename=filename5)
        db = DataFrame (data_aET,columns=["aET_"+warmperiod])
        data.append(db)

        filename6="pet_{:}_ysum_timmean_fldmean.nc".format(warmperiod)
        data_pet=read_data(VAR="pet",filename=filename6)
        dc = DataFrame (data_pet,columns=["pet_"+warmperiod])
        data.append(dc)
        
    
    data = pd.concat(data, axis=1)
    #print(data)

    meta = pd.read_csv("/work/malla/sachsen_output/RCP8.5_EurCordex_list.csv", sep=";")
    met_ids= np.sort(pd.unique(meta["met_id"]))
    mets = pd.DataFrame(met_ids, columns = ['mets'])
    #data = data.reset_index()
    data1 = data.join(mets)

    #data1 = data.reset_index(drop=True)
    print(data1)
    #for col in data.columns:
    #    print(col)


    
    data1.to_csv("/work/malla/sachsen_output/scatter_plots/data/allMets_allindicators_spmean.csv")
