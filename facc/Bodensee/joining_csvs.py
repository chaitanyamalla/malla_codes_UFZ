#!/usr/bin/env python


import pandas as pd
import numpy as np
import glob 
import os

rcps= ["rcp26", "rcp85"]
vars= ["abs-rel"] ###, "abs-abs"]
types= ["sum"]   ###"avg", 
stats=["ensminimum","ensp25", "ensmedian", "ensp75", "ensmaximum"]

#ind="Qrouted_avg_year_"

inpath= "./dams_output_csv/"
outpath="./"

dams= pd.read_csv("/work/malla/meteo_germany/DE_indicatorsdata/facc/Bodensee/Bodensee.csv", encoding = "ISO-8859-1") # error_bad_lines=False)

for type in types:
    ind="Qrouted_daily_"+type+"_year_"
    print(ind)
    for v in vars:
        list=[]
        s_file=pd.read_csv(inpath+"Qrouted_daily_sum_year_abs-rel_change_rcp26_ensmaximum_de_hicam_facc1.csv", encoding="ISO-8859-1") #, error_bad_lines=False)
        list.append(s_file.iloc[:,:2])
        
        for r in rcps:
            for stat in stats:
                file=inpath+ind+v+"_change_"+r+"_"+stat+"_de_hicam_facc1.csv"
                k = file.split("/")
                print(k)
                k1=k[-1]
                print(k1)
                k2=k1.split("_")
                print(k2)
                k3=k2[7] 
                print(k3)

                df= pd.read_csv(file, encoding = "ISO-8859-1") #, error_bad_lines=False)
                #print(df["value"])
                #pd.to_numeric(data["value"], errors='coerce')
                df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
                data1= df.rename(columns={'Facc':k3}).round(2)
                #data1.drop(data1.columns[data1.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)


                #print(data1)
                list.append(data1[k3])

        #print(list)
        data= pd.concat(list, axis=1, join="inner")
        print(data)
        #data.to_csv(inpath+ind+v+"_ensstats.csv", encoding = "ISO-8859-1")
        #print(data.dtypes)

        #text=file[75:106]
        #print(text)
        i=0
        j=1
        k=2
        l=3
        daa=0
        length=int(len(data)/4)
        print(length)
        for po in range(0,length):
            if type == "sum":
                #data.iloc[i,2:12] = data.iloc[i,2:12]*86400*30
                data.iloc[i,2:12] = data.iloc[i,2:12]/1000000

            data.iloc[i,2:12]= data.iloc[i,2:12].astype(float).round(2)
            data.iloc[j,2:12] = data.iloc[j,2:12].apply(lambda x: "+"+str(x) if x>0 else x)
            data.iloc[k,2:12] = data.iloc[k,2:12].apply(lambda x: "+"+str(x) if x>0 else x)
            data.iloc[l,2:12] = data.iloc[l,2:12].apply(lambda x: "+"+str(x) if x>0 else x)
            #data.iloc[i,0] = '\multirow{4}{*}{' + data.iloc[i,0] +'}'

            data.iloc[j,0]="Lon: "+str(dams.iloc[daa,1])+"°"
            data.iloc[k,0]="Lat: "+str(dams.iloc[daa,2])+"°"
            data.iloc[l,0]="EZG: "+str(dams.iloc[daa,3].round(2))+" $km^2$"

            i += 4
            j += 4
            k += 4
            l += 4
            daa+=1

        data=data.round(2) 
        
        if v == "abs-abs" and type== "sum":
            unit_abs="[Mio. $m^3/y$]"
            unit_change="[$\Delta m^3/y$]"
        elif v == "abs-rel" and type== "sum":
            unit_abs="[Mio. $m^3/y$]"
            unit_change="[\%]"
        elif v == "abs-rel" and type== "avg":
            unit_abs="[$m^3/s$]"
            unit_change="[\%]"
        elif v == "abs-abs" and type== "avg":
            unit_abs="[$m^3/s$]"
            unit_change="[$\Delta m^3/s$]"
                
        data['date'] = data['date'].replace('1985-01-01','1971-2000 '+unit_abs+' ')
        data['date'] = data['date'].replace('2035-01-01','2021-2050 '+unit_change+' ')
        data['date'] = data['date'].replace('2050-01-01','2036-2065 '+unit_change+' ')
        data['date'] = data['date'].replace('2083-01-01','2069-2098 '+unit_change+' ')
        data['Dam'] = data['Dam'].replace('_', ' ', regex=True)
        data['ensminimum']= data['ensminimum'].astype(str)
        print(data.dtypes)
        # for col in data.columns:
        #     data[col]= data[col].astype("string").str.replace('.',',')

        data = data.rename(columns={'Dam': 'Talsperre', 'date': 'Zeitscheibe'})
        #data.to_csv(r"C:\Users\malla\Documents\Facc_extract\dams_facc_stats_tables\Q"+ file[62:94]+"_updated.csv", encoding="ISO-8859-1")
        data.to_csv(outpath+ind+v+"_change_ensstats_updated_forlatex.csv", sep=";", encoding = "utf-8-sig") #seprator change when converting all points to commas
        print(data)  
