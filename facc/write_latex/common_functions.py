# --------------------------------------------------
#  File:        common_functions.py
#
#  Created:     Di 05-10-2021
#  Author:      Friedrich Boeing
#
# --------------------------------------------------
#
#  Description: useful functions
#
#  Modified:
#
# --------------------------------------------------

import pandas as pd
import numpy as np
from common_settings import *

#  -- import from ufz library  ---------------------

from ufz import fread,readnc, position, get_brewer, abc2plot, astr  #dumpnetcdf, 
from ufz.netcdf4 import NcDataset

def calc_metrics(data, title_warm, method, round_dig=4):

    '''
    function to calculate metrics over array
    Metrics are minimum, 25 percentile, median, mean, 75 percentile, maximum

    method: spatial

    function to calculate spatial metrics for 3D array (time, lat, lon)
    metrics are calculated over axis 1 and 2 (counting from 0)

    method: ensemble

    function to calculate ensemble metrics for 4D array (time, ensemblemembers, lat, lon)
    metrics are calculated over axis 1 (counting from 0)

    '''

    if method == "spatial":
        axis_val=(1,2)
    elif method == "ensemble":
        axis_val=1

    tmp_q25, tmp_median, tmp_q75     = np.nanpercentile(data,[25,50,75],axis=axis_val) # calculates the median
    tmp_max                          = np.nanmax(data,axis=axis_val)
    tmp_min                          = np.nanmin(data,axis=axis_val)
    tmp_mean                         = np.nanmean(data,axis=axis_val)
    tmp_data=np.column_stack([tmp_min, tmp_q25, tmp_median, tmp_mean, tmp_q75, tmp_max])
    # print(tmp_data)
    if round_dig != False:
        tmp_data=tmp_data.round(decimals=round_dig)
    tmp_merge=pd.DataFrame(data=tmp_data,index=title_warm,columns=["min","p25","median","mean","p75","max"])
    return tmp_merge

def print_table(th, median_list, ll, headerline,do_periods=do_periods):
    # add header
    if ll == 0:
        th.write('\n')
        if do_periods:
            th.write('period & median &  max \\\n')
        # th.write('\multicolumn{7}{|c|}{' + headerline + '} \\\\\n')
        th.write('\hline\n')
    if do_periods:
        th.write("       {:}".format(title_warm[ll]) + ' &       '  + ' &        '.join(astr(np.array(median_list), prec=1)) + ' \\\\\n')
    else:
        th.write("       {:.1f}".format(title_warm[ll]) + ' K &       ' + ' &        '.join(astr(np.array(median_list), prec=1)) + ' \\\\\n')

def print_table_latex(filename,data,header,rownames):
    data=np.array(data)
    th = open(filename, 'w')
    columns=["min","p25","median","mean","p75","max"]
    th.write('\\begin{table}[h!]')
    th.write('\n')
    th.write('\caption{' + header.replace('%','\%') +'}' )

    th.write('\n')
    th.write('\\begin{tabular}{ll|r|r|r|r|r|r}')
    th.write('\n')
    th.write('\\multicolumn{1}{c}{} & ')
    for col in np.arange(len(columns)):
        if col == (len(columns) - 1):
            th.write(str(columns[col]))  
        else:
            th.write(str(columns[col]) + " & ")
    th.write('\\' + '\\')
    th.write('\\hline')
    th.write('\n')
    for rr,rows in enumerate(rownames):
        th.write(str(rownames[rr]) + " & ")
        for cc,cols in enumerate(columns):
            if col == (len(columns) - 1):
                th.write("{:} & ".format(data[rr,cc]))
            else:
                th.write("{:}".format(data[rr,cc]))

        th.write('\\' + '\\')
        th.write('\n')
    th.write('\\hline')

    th.write('\n')
    th.write('\\end{tabular}')
    th.write('\n')
    th.write('\\end{table}')
    th.close()
