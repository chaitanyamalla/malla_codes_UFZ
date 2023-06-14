#!/usr/bin/env python
# --------------------------------------------------
#  File:        plot_indicators.py
#
#  Created:     Mi 05-05-2021
#  Author:      Friedrich Boeing
#
# --------------------------------------------------
#
#  Description: Script to plot indicators for hicam data
#
#  Modified:
# original scripts:

# author: Stephan Thober
# created: Aug 2017

# adapted: Friedrich Boeing, April 2018
# adapted for HICAM Friedrich Boeing Oct 2020

#
# --------------------------------------------------


from __future__ import print_function
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from os.path import isfile
from sys import exit
import os
import pandas as pd

from datetime import datetime
import datetime
#  -- import from ufz library  ---------------------

from ufz import fread,readnc, position, get_brewer, abc2plot, astr  #dumpnetcdf, 
from ufz.netcdf4 import NcDataset

#  -- import from local python scripts! ------------

from common_plot_setting import *
from common_functions import *
from common_settings import *
miss_value = -9999.

from scipy.stats import ranksums



def calc_direction(data_hist,data_warm,robust_threshold=0.66):
    '''
    calculate the direction of change and determine if robustness criterion is met.
    Robust means here that [robust_threshold]*100 % of models agree on the direction

    Parameters
    ----------
    data_hist : 4d array (time,met_id,lat,lon)
          time is aggregated value for 30-year period 1971-2000, met_id ensemble member
    data_warm : 4d array (time,met_id,lat,lon)
          time is aggregated value for 30-year future periods, met_id ensemble member
    robust_threshold : float
      
    Returns
    -------
    res :  3d array (time,lat,lon)

    '''
    if var_type == 'rel_change' or var_type == "abs-rel_change":
        tmp_data = (data_warm - data_hist)/data_hist * 100.
    if var_type == 'abs_change' or var_type == "abs-abs_change":
        tmp_data = (data_warm - data_hist)
    print(tmp_data.shape)
    tmp_sign=np.sign(tmp_data)
    #  -- check model change direction ----------------------
    # check whether either models agree on negative or positive direction of change
    res_sign=(np.sum(tmp_sign == 1, axis=(1)) > tmp_sign.shape[1]*robust_threshold) | \
             (np.sum(tmp_sign == -1, axis=(1)) > tmp_sign.shape[1]*robust_threshold)
    res=np.ma.masked_greater(res_sign, 0) # mask array 
    return res
def calc_significance(wilcox_data,pval_threshold=0.05,robust_threshold=0.66):
    '''
    read in p values of wilcoxon rank sum tests

    Parameters
    ----------
    wilcox_data : 4d array (time,met_id,lat,lon)
          time is 30-year period, met_id ensemble member
    Returns
    -------
    significance : 3d array (time,lat,lon)
    '''
    tmp_data = wilcox_data < pval_threshold
    print(tmp_data.shape)
    print( tmp_data.shape[1]*robust_threshold)
    # determine if 66% of models show significant change
    tmp_data = (np.sum(tmp_data,axis=(1)) > tmp_data.shape[1]*robust_threshold)
    res=np.ma.masked_greater(tmp_data, 0) # mask array 
    return res

if __name__ == '__main__':
    #  -- main script settings -------------------------
    if mask_region == "germany": 
        do_main_catch_ger      = True
    else:
        do_main_catch_ger      = False
    do_main_catch_ger      = True
    # if var_type == "rel_change" or var_type == "abs_change":
    #     nc_write               = True
    # else:
    if mask_region == "germany":
        nc_write               = True
    else:
        nc_write               = False

    do_plot                = True
    do_table               = False
    # do_table               = False
    # assumeAdaptation       = False # not implemented
    do_text                = True
    # if eval_rcp == "rcp26":
    #     do_colorbar=False
    # else:
    do_colorbar            = True
    do_robustness          = False
    # ens_stat="ensmedian"
    # ens_stat="worstcase"
    print("plot "  + indicator + " " +eval_period)
    #  -- set paths and filename bases -----------------

    inpath="./data1"
    outpath_plots="./plots_periods/"
    outpath_tables="./tables_periods/"
    if do_periods:
        outpath_data="./data_periods/"
    else:
        print("no path created yet for warming levels")
    if do_robustness:
        robust = "_robustness"
    else:
        robust = ""
    # input file:
    # fname_data               = '{:}/{:}_{:}_de_hicam.nc'.format(inpath,indicator,eval_period)
    fname_data       = '{:}/{:}_{:}_{:}_{:}_ensmedian_de_hicam.nc'.format(inpath,indicator,eval_period,var_type,eval_rcp)
    # fname_data_wilcox        = '{:}/{:}_{:}_de_hicam_wilcoxon.nc'.format(inpath,indicator,eval_period)
    # output name base:
    outbase                  = '{:}_{:}_{:}_{:}_{:}'.format(indicator,eval_period,var_type,eval_rcp,ens_stat)
    if do_main_catch_ger:
        if (var_type in ["abs-abs_change","abs-rel_change"]) and grid == "2x2":
            pngbase          = '{:}/{:}_{:}_maincatchments_2x2'.format(outpath_plots,outbase,mask_region)
        else:
            pngbase          = '{:}/{:}_{:}_maincatchments'.format(outpath_plots,outbase,mask_region)

    else:
        if (var_type in ["abs-abs_change","abs-rel_change"]) and grid == "2x2":
            pngbase          = '{:}/{:}_{:}_2x2'.format(outpath_plots,outbase,mask_region)
        else:
            pngbase          = '{:}/{:}_{:}'.format(outpath_plots,outbase,mask_region)

    ncbase           = '{:}/{:}_{:}'.format(outpath_data,outbase,mask_region)
    ncbase_ger       = '{:}/{:}_germany'.format(outpath_data,outbase,mask_region)
    figname          =  pngbase + robust + ".png"
    ncfile           = ncbase + '.nc'
    print(ncfile)
    tablebase        = '{:}/{:}'.format(outpath_tables,outbase)
    table_file       = '{:}/{:}_{:}_{:}_{:}_{:}.tex'.format(outpath_tables,indicator,eval_period,var_type,eval_rcp,mask_region)
    print(title_periods)
    if var_type == 'abs' or var_type == "abs-abs_change" or var_type == "abs-rel_change":
        if do_periods:
            title_warm      = title_periods
        iplot               = 1
        ncol                = len(title_warm)
        if var_type == "abs-abs_change" or var_type == "abs-rel_change":
            ncol                = 2

    else:
        if do_periods:
            title_warm      = title_periods[1:]
        iplot               = 1
        ncol                = len(title_warm)
    ncvarname=indicator_ncvarnames[indicator]
    Ndeg                    = len(title_warm)
    Nrcp                    = len(rcps)
    Ngcm                    = len(gcms)
    Nhm                     = len(hms)
    Nrcm                    = len(rcms)

    #  -- labels ---------------------------------------
    if language == "German":
        indicator_longnames=indicator_longnames_de
    elif language == "English":
        indicator_longnames=indicator_longnames_en

    #  -- colors ---------------------------------------




    # read mask for germany /hicam_domain /federalstates
    mask               = readnc(mask_path, 'mask')
    mask_ger           = np.zeros(mask.shape, dtype='bool')

    facc_threshold = 100 # minimum flow accumulation area of 100 km² for visualization of routed streamflow

    if ncvarname == "Qrouted":
        mask_ger[...]     = np.logical_and((mask == 1), (facc >facc_threshold))
    else:
        mask_ger[...]      = (mask == 1)


    # from common_plot_setting import outtype


    #  -- read files -----------------------------------

    # if  (isfile(ncfile) or (mask_region != "de_hicam" and (isfile(ncbase_ger +'.nc')))) and ens_stat != "worstcase":
    # if  (isfile(ncfile) or (mask_region != "de_hicam" and (isfile(ncbase_ger +'.nc')))) and ens_stat == "":
    # if  (isfile(ncfile) and not do_robustness and not do_main_catch_ger):
    if  (isfile(ncfile)):
        if not isfile(ncfile):
            ncfile = ncbase_ger + '.nc'

        print('')
        print(' plot data {:} stored.'.format(ncfile))
        write_data=readnc(ncfile,indicator)
    else:
        if not isfile(fname_data):
            print('')
            print(' indicator file {:} not stored.'.format(fname_data))
            print(' and run')
            print(' python calc_indicators.py')
            exit()
        else:
            print('')
            print('read input from file: ', fname_data)
            data = readnc(fname_data, var=ncvarname)
            if do_robustness:
                data_wilcoxon = readnc(fname_data_wilcox, var=ncvarname)

            # print(data.shape)

            if eval_rcp == "rcpall":
                print("plot data for all rcps")
            else:
                rr=list(np.where(meta["rcp"] == eval_rcp)[0])
                print("plot changes for {:}: met ids {:}".format(eval_rcp,rr))
                data               = data[:,rr,:]
                if do_robustness:
                    data_wilcoxon      = data_wilcoxon[:,rr,:]
        
            data_hist      = data[0,:]
            data_warm      = data[1:,:]
            if do_robustness:
                data_direction=calc_direction(data_hist,data_warm)
                data_significance=calc_significance(data_wilcoxon)
 
            write_data=np.ma.array(np.zeros((Ndeg, data.shape[-2], data.shape[-1])),
                                      mask=True, fill_value=-9999.)-9999.
            # print(write_data.shape)
            # if do_table == True:
            #     print('creating table file: {:}'.format(table_file))
            #     th = open(table_file, 'w')
            if ens_stat == "ensmedian":
                plot_data_hist = np.ma.median(data_hist,axis= 0)
            elif ens_stat == "ensmaximum":
                plot_data_hist = np.ma.max(data_hist,axis= 0)
            elif ens_stat == "ensminimum":
                plot_data_hist = np.ma.min(data_hist,axis= 0)
            elif ens_stat == "ensp90":
                data_hist      = np.ma.filled(data_hist,np.nan)
                plot_data_hist = np.nanpercentile(data_hist,90,axis= 0)
                plot_data_hist = np.ma.array(plot_data_hist)
                plot_data_hist.mask = (plot_data_hist == np.nan)
            elif ens_stat == "worstcase":
                # select last period to define worstcase model (strongest deviation from historic)
                dat=data_warm[-1,:]
                dat.mask = np.logical_or(~mask_ger, dat.mask)
                print(np.ma.sum(dat.mask == True,axis=(0,1,2)))

                avg_change = np.ma.mean(dat, axis = (1,2)) # calculate spatial mean for average change
                print(avg_change)
                if indicator == "n_droughtdays_0_30cm":
                    wcm  = np.ma.max(avg_change) # identify worst case model
                elif ncvarname == "recharge_adjust":
                    wcm  = np.ma.min(avg_change) # identify worst case model
                pos_wcm = np.where(avg_change == wcm)[0][0]
                print(pos)
                print("identified: " + met_ids[pos_wcm] + " as most extreme scenario in period: " + title_periods[-1] +" with mean change: " + '{:}'.format(wcm))
                plot_data_hist = data_hist[pos_wcm,:] # select worst case model to plot
                # print(plot_data_hist.shape)
            elif ens_stat == "SNR":
                data_SNR = data_warm - data_hist
            ll = 0
            for iper, peri in enumerate(title_warm):
                print(iper,peri)
                if iper == 0 and (var_type == "abs" or var_type == "abs-abs_change" or var_type == "abs-rel_change"):
                    plot_data = plot_data_hist
                else:
                    if var_type == 'abs' or var_type == "abs-abs_change" or var_type == "abs-rel_change":
                        iper = iper - 1 # reduce iper to start by 0 in data_warm array
                    if ens_stat == "ensmedian":
                        plot_data_warm = np.ma.median(data_warm[iper,...], axis = 0)
                    elif ens_stat == "ensmaximum":
                        plot_data_warm = np.ma.max(data_warm[iper,...], axis = 0)
                    elif ens_stat == "ensminimum":
                        plot_data_warm = np.ma.min(data_warm[iper,...], axis = 0)
                    elif ens_stat == "ensp90":
                        tmp_warm = np.ma.filled(data_warm[iper,...],np.nan)
                        plot_data_warm = np.nanpercentile(tmp_warm,90,axis= 0)
                        plot_data_warm = np.ma.array(plot_data_warm)
                        plot_data_warm.mask = (plot_data_warm == np.nan)
                    elif ens_stat == "worstcase":
                        plot_data_warm = data_warm[iper,pos_wcm,:]
                        print(plot_data_warm.shape)
                    elif ens_stat == "SNR":
                        if var_type != "SNR":
                            raise IOError('***ERROR: for Signal-to-Noise-Ratio both ens_stat and var_type need to be set to "SNR"')

                        tmp_median = np.ma.median(data_SNR[iper,...], axis = 0)
                        tmp_warm = np.ma.filled(data_SNR[iper,...],np.nan)
                        tmp_IQR = np.nanpercentile(tmp_warm,75,axis = 0) - np.nanpercentile(tmp_warm,25,axis = 0)



                    # print(plot_data_hist.shape)
                    # print(plot_data_warm.shape)
                    if var_type == 'rel_change' or var_type == "abs-rel_change":
                        plot_data = (plot_data_warm - plot_data_hist)/plot_data_hist * 100.
                    if var_type == 'abs_change' or var_type == "abs-abs_change":
                        plot_data = (plot_data_warm - plot_data_hist)
                    if var_type == 'abs':
                        plot_data = plot_data_warm
                    if var_type == "SNR":
                        if ens_stat != "SNR":
                            raise IOError('***ERROR: for Signal-to-Noise-Ratio both ens_stat and var_type need to be set to "SNR"')
                        plot_data = np.abs(tmp_median/tmp_IQR)
                plot_data.mask = np.logical_or(~mask_ger,plot_data.mask)
                np.ma.set_fill_value(plot_data, -9999)
                # if do_table:
                #     # write table file ################################################
                #     data_table_median    = np.ma.median(plot_data,axis=(0,1))
                #     data_table_max       = np.ma.max(plot_data,axis=(0,1))
                #     data_table_min       = np.ma.min(plot_data,axis=(0,1))
                #     print('min: {}'.format(data_table_min))
                #     print('median: {}'.format(data_table_median))
                #     print('max: {}'.format(data_table_max))
                #     print_table(th, [data_table_median,data_table_max], ll, "")   
                write_data[ll,:] =plot_data
                ll = ll + 1
            # if do_table:
            #     # close table file ################################################
            #     th.close()

    if do_table:
        #  -- table for mask_region ------------------------

        write_data.mask      = np.logical_or(~mask_ger,write_data.mask)
        table_data           = np.ma.filled(write_data,np.nan)
        table_data_region    = calc_metrics(table_data,round_dig=1,title_warm=title_warm,method="spatial")
        print("write spatial stat table for: " + mask_region)
        print(table_data_region)
        table_data_region.to_csv(tablebase+ '_' +mask_region + "_spatialstat.csv")
        if do_main_catch_ger:
            mask_main_catch               = readnc(mask_main_catch_path, 'mask')
            for catch in range(mask_main_catch.shape[0]):
                # print(mask_main_catch.shape)
                mask_tmp           = np.zeros((mask_main_catch.shape[1],mask_main_catch.shape[2]), dtype='bool')
                mask_tmp[...]      = (mask_main_catch[catch,:] == 1)
                tmp           = write_data.copy()
                for nn in range(Ndeg):
                    tmp[nn,:].mask      = np.logical_or(~mask_tmp,tmp.mask)
                tmp         = np.ma.filled(tmp,np.nan)
                # print("calculate {:} for main catchments".format(var_type))
                tmp_stat         = calc_metrics(tmp,round_dig=1,title_warm=title_warm,method="spatial")
                # print(main_catch_names[catch],tmp_stat)
                tablefile=tablebase + "_{:}_spatialstat".format(main_catch_names[catch])
                tmp_stat.to_csv(tablefile + ".csv")
                #  -- create latex table for report ----------------

                table_header=colorbarlabel+ ": Raeumliche Metriken im Einzugsgebiet " +main_catch_names[catch]+  ' fuer ensemble median: ' + rcp_titles[eval_rcp]
                print_table_latex(tablefile + ".tex",tmp_stat,header=table_header,rownames=title_warm)

            # --------------------------------------------------
            #  -- CALCULATE ENSEMBLE STATS OVER SPATIAL MEAN ---
            # --------------------------------------------------

            if var_type == "abs-rel_change":
                tmp_data = data.copy()
                print(tmp_data.shape)
                tmp_data[1:,:] = (tmp_data[1:,:]- tmp_data[0,:])/tmp_data[0,:] * 100.
            if var_type == 'rel_change':
                tmp_data = (data_warm - data_hist)/data_hist * 100.
            if var_type == 'abs_change':
                tmp_data = (data_warm - data_hist)
            if var_type == "abs-abs_change":
                tmp_data = data.copy()
                tmp_data[1:,:] = tmp_data[1:,:]- tmp_data[0,:]
            if var_type == 'abs':
                tmp_data = data.copy()
            print(tmp_data.shape)
            for catch in range(mask_main_catch.shape[0]):
                mask_tmp           = np.zeros((mask_main_catch.shape[1],mask_main_catch.shape[2]), dtype='bool')
                mask_tmp[...]      = (mask_main_catch[catch,:] == 1)
                tmp           = tmp_data.copy()
                for nn in range(Ndeg):
                    # print(str(nn+1) + '/' +str(Ndeg))
                    for ee in range(tmp.shape[1]):
                        # print(tmp[nn,ee,:].mask)
                        # # print(tmp[nn,ee,:])
                        # print(~mask_tmp)
                        tmp[nn,ee,:].mask      = np.logical_or(~mask_tmp,tmp[nn,ee,:].mask)
                tmp         = np.ma.filled(tmp,np.nan)
                print(tmp.shape)

                # calculate mean value over region:
                tmp         = np.nanmean(tmp,axis=(2,3))
                # print(tmp)
                print("calculate {:} for main catchments".format(var_type))
                tmp_stat         = calc_metrics(tmp,round_dig=1,title_warm=title_warm,method="ensemble")
                # print(main_catch_names[catch],tmp_stat)
                outbase          = '{:}_{:}_{:}_{:}_spatialmean'.format(indicator,eval_period,var_type,eval_rcp)
                tablebase        = '{:}/{:}'.format(outpath_tables,outbase)
                tablefile        = tablebase + "_{:}_ensemblestat".format(main_catch_names[catch])
                tmp_stat.to_csv(tablefile + ".csv")
                #  -- create latex table for report ----------------
                table_header     = colorbarlabel+ ": Mittelwert über das Einzugsgebiet " +main_catch_names[catch]+  ' und Metriken über das Ensemble: ' + rcp_titles[eval_rcp]
                print_table_latex(tablefile + ".tex",tmp_stat,header=table_header,rownames=title_warm)
            
    # --------------------------------------------------
    #  -- PLOTTING -------------------------------------
    # --------------------------------------------------
    if do_plot:
        print('<<< start plotting')

        if (outtype == 'pdf'):
            print('Plot PDF ', pdffile)
            pdf_pages = PdfPages(pdffile)
        elif (outtype == 'png'):
            print('Plot PNG ', pngbase)
        else:
            print('Plot X')

        print('setting figsize almost as square for plotting')
        # double column width in NCC
        mpl.rc('figure',     figsize=figsize) 
        figsize            = mpl.rcParams['figure.figsize']
        ifig               = int(np.ceil(np.random.exponential(100)))
        fig                = plt.figure(ifig)

        ll = 0
        for iper, peri in enumerate(title_warm):
            if var_type == "abs" or (iper == 0 and  (var_type == "abs-abs_change" or var_type == "abs-rel_change")):
                colors   = colors_abs
                levels = levels_abs
                colorbarlabel=colorbarlabel_abs
            elif var_type == 'rel_change' or var_type == "abs-rel_change":
                colors = colors_rel_change
                levels = levels_rel_change
                colorbarlabel=colorbarlabel_rel_change
            elif var_type == 'abs_change' or var_type == "abs-abs_change":
                colors = colors_abs_change
                levels = levels_abs_change
                colorbarlabel=colorbarlabel_abs_change
            elif var_type == "SNR":
                colors = colors_SNR
                levels = levels_SNR
                colorbarlabel=colorbarlabel_SNR

            cmap=mpl.colors.ListedColormap(colors)
            if ll == 0:
                print("color levels:")
                print(*levels)
                print("colors: ")
                print([mpl.colors.rgb2hex(color) for color in colors])
                print("Label: ")
                print(colorbarlabel)
                print("time labels:")
                print(title_periods)
            plot_data = write_data[iper,:]

            plot_data.mask = np.logical_or(~mask_ger,plot_data.mask)

            mp = fig.add_axes(position(nrow,ncol, iplot, wspace=0.03, hspace=0.01,
                                           bottom=0.15, top=top_plot,
                                           left=left_plot, right=0.95),
                                  projection=projection)
 
            # create colorscheme
            norm          = mpl.colors.BoundaryNorm(levels, cmap.N)
            pcm     = mp.pcolormesh(lons, lats, plot_data,
                                   transform=ccrs.PlateCarree(),
                                   cmap=cmap, norm=norm, edgecolors='None',
                                rasterized=True)
            if do_robustness:
                plot_direction = data_direction[iper,:]
                plot_direction.mask = np.logical_or(~mask_ger,plot_direction.mask)
                plot_significance = data_significance[iper,:]
                plot_significance.mask = np.logical_or(~mask_ger,plot_significance.mask)
                r_contourf= mp.contourf(
                    lons, lats, plot_direction, 
                   transform=ccrs.PlateCarree(), colors='#bdbdbd', alpha = 0.0, hatches = ['////']#bdbdbd
            )
                r_contourf= mp.contourf(
                    lons, lats, plot_significance, 
                   transform=ccrs.PlateCarree(), colors='#bdbdbd', alpha = 0.0, hatches = ['\\\\\\']#bdbdbd
            )
            # pcm = mp.contourf(lons, lats, plot_data, transform=ccrs.PlateCarree(), cmap=cmap, norm=norm, edgecolors='None')

            ##### Gridlines ###################################################
            #gl = mp.gridlines(xlocs=np.arange(5,21,3),
                              #ylocs=np.arange(45,58,3),
                              #color='0.2',
                              #linewidth=0.125)

            ##### Tickmarks and X, Y Labels ####################################
            from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
            if mask_region == "de_hicam" or mask_region == "germany":
                x_step=2
                y_step=2
                mp.set_xticks(np.arange(int(extent[0]),int(extent[1])+0.1,x_step), crs=crs_latlon)
                mp.set_yticks(np.arange(int(extent[2]),int(extent[3])+0.1,y_step),  crs=crs_latlon)
            elif mask_region == "ww_leipzig_ug":
                x_step=0.2
                y_step=0.1
                # mp.set_xticks(np.arange(int(extent[0]-2),int(extent[1]+2)+0.1,x_step), crs=crs_latlon)
                # mp.set_yticks(np.arange(int(extent[2]-2),int(extent[3]+2)+0.1,y_step),  crs=crs_latlon)
            else:
                x_step=1
                y_step=0.5
                mp.set_xticks(np.arange(int(extent[0]-2),int(extent[1]+2)+0.1,x_step), crs=crs_latlon)
                mp.set_yticks(np.arange(int(extent[2]-2),int(extent[3]+2)+0.1,y_step),  crs=crs_latlon)
            xticklabels = mp.get_xticklabels()
            yticklabels = mp.get_yticklabels()
            if do_text:
                if (grid == "2x2"):
                    if (iplot > ncol):
                        mp.set_xticklabels(xticklabels, fontsize=6) #  rotation=90,
                        mp.xaxis.set_major_formatter(LongitudeFormatter(zero_direction_label=True))
                    else:
                        mp.set_xticklabels('')
                else:
                    mp.set_xticklabels(xticklabels, fontsize=6) #  rotation=90,
                    mp.xaxis.set_major_formatter(LongitudeFormatter(zero_direction_label=True))
                if iplot == 1 or (iplot == (1+ ncol) and grid == "2x2"):
                    mp.set_yticklabels(yticklabels, fontsize=6)#, rotation=90)
                    mp.yaxis.set_major_formatter(LatitudeFormatter())
                else:
                    mp.set_yticklabels('')
            else:
                mp.set_xticklabels('')
                mp.set_yticklabels('')

            # mp.set_yticks(np.arange(0,100,90),  crs=crs_latlon)
            # mp.set_yticklabels('')
            mp.tick_params(axis='both', which='major', labelsize=6,direction='in')

            ##### set title left side, rotated #############################
            if ((var_type == "abs-rel_change") or (var_type ==  "abs-abs_change")):
                if grid == "2x2":
                    title_y=0.98
                    fig.text(0.5, title_y, rcp_titles[eval_rcp], ha="center", va="center", fontsize=24)
                else:
                    title_y=0.6

                    fig.text(0.03, title_y, rcp_titles[eval_rcp], ha="center", va="center", fontsize=24,rotation=90)
            else:
                if ens_stat == "worstcase":
                    fig.text(0.5, 0.9, 'Worstcase Model ' + rcp_titles[eval_rcp] +' (mean value in region {:}): '.format(title_periods[-1]) + meta['inst.rcm'][pos_wcm] +"({:})".format(met_ids[pos]) , ha="center", va="center", fontsize=16)
                else: 
                    fig.text(0.5, 0.9, ens_stat_titles[ens_stat]+': ' + rcp_titles[eval_rcp], ha="center", va="center", fontsize=24)



            ##### label with warming name ##################################
            # if (iplot <= ncol):
            if do_periods:

                mp.set_title(peri,fontsize = 12 )
            else:
                mp.set_title(peri.replace('deg',' °C').replace('p0','').replace('p','.'),fontsize = 12 ) 

            mp.set_extent(extent) #, crs=ccrs.Mercator())

            ##### geographical features ###################################
            # add country borders
            if ncvarname == "Qrouted":
                mp.add_feature(state_borders, facecolor='0.85', edgecolor='k', lw=0.5, zorder = -1)
            else:
                # mp.add_feature(state_borders, facecolor='0.7', edgecolor='k', lw=0.5)#, zorder = -1)
                mp.add_feature(state_borders, facecolor='none', edgecolor='k', lw=0.5)
            if ncvarname != "Qrouted":
                mp.add_feature(
                    cfeature.NaturalEarthFeature(
                        category='physical',
                        name='rivers_lake_centerlines',
                        scale='10m',
                        facecolor='none'
                    ),
                    edgecolor='#045a8d',
                    lw=0.5
                )

            # federal countries, bundeslaender
            if mask_region != "de_hicam" or mask_region != "germany":
                pass
            else:
                shpf_fedcon = '/data/hydmet/WIS_D/shapes/BuLaender.shp'
                reader    = shpreader.Reader(shpf_fedcon)
                fedstates = reader.records()
                i = 0
                for c in fedstates:
                    fed = c.attributes['GEN']
                    
                    # print('fed: ' +str(fed))
                    if i == 6 or i == 14:
                        fed = str(fed).replace('\\xfc','ü')
                    i = i + 1
                    # print('fed: ' +str(fed))
                    #https://modelingguru.nasa.gov/docs/DOC-2602
                    # for federalstates which only have one shapefile no iteration over shapefiles:        
                    if isinstance(BL['{:}'.format(mask_region)], str) == True: 
                        if fed == BL['{:}'.format(mask_region)]:
                            # print('BL: ' +  str(BL['{:}'.format(region)]))
                            mp.add_feature(
                                    ShapelyFeature([c.geometry], ccrs.PlateCarree()),
                                    facecolor='none', 
                                    #facecolor='w',
                                    lw=1.5,
                                    edgecolor='0',
                            )
                                # loop over shapefiles in dictionary (for regions e-g- MD or NDR:
                    else:
                        for x in BL['{:}'.format(mask_region)]: 
                            #print('BL: ' + str(x))
                            if fed == x:
                                mp.add_feature(
                                    ShapelyFeature([c.geometry], ccrs.PlateCarree()),
                                    facecolor='none', 
                                    #facecolor='w',
                                    lw=1.0,
                                    edgecolor='0',
                                )

                mp.add_feature(fed_count, facecolor='none', lw=1.0,alpha=0.4, edgecolor='0') #, alpha=0.75)
            if do_main_catch_ger:
                if iplot == 1:
                    print("plot shapes of main river catchments")
                mp.add_feature(main_catch_ger, facecolor='none', lw=1.0,alpha=1.0, edgecolor='0') #, alpha=0.75)

            if mask_region == "ww_leipzig_ug":
                for ww_shps in [shape_ug,shape_vg]:
                    mp.add_feature(
                    ww_shps,
                    facecolor='none', 
                    #facecolor='w',
                    lw=1.0,
                    edgecolor='0',
                )
            ##### add letter tags to subplots #############################
            if (iplot == ncol):
                if ncol == 3:
                    yyyy = 0.27
                if ncol == 4:
                    yyyy = 0.32
                # fig.text( 0.6, yyyy,"(C) O. Rakovec, L. Samaniego, F.Boeing, T. Remke et al.; UFZ Oct 2020 ",fontsize=6)
            iplot  += 1


            # colorbar ########################################################
            if do_colorbar:
                if (iper == 0) and ((var_type == "abs-rel_change") or (var_type ==  "abs-abs_change")):
                    print("plot abs")
                    left_cb,bottom_cb, width_cb, heigth_cb=(0.08,0.1, 0.2, 0.4)
                    left_cb,bottom_cb, width_cb, heigth_cb=(0.08,0.1, 0.3, 0.4)
                    if grid == "2x2":
                        left_cb,bottom_cb, width_cb, heigth_cb=(0.05,0.03, 0.4, 0.4)
                    cbr=fig.add_axes([left_cb,bottom_cb,width_cb,heigth_cb]) #0.75 # 0.95
                    cb = plt.colorbar(pcm,ax=cbr,
                          orientation='horizontal',
                          # aspect=10,
                          fraction=0.225,           # start of colorbar on the left 
                          # shrink=1.4,             # lenght of the colorbar
                          # pad=0.04,                 # distance between picture and colorbar 
                          extend='both',            # extend - show colors for out of range values
                          extendfrac='auto',       # length of extensions is oriebtated at other pathcs
                          # spacing='proportional'   # length of patch is scaled with value
                          )
                    # set ticks
                    # if (indicator in ["recharge_adjust_sum","recharge_adjust_20perc_avg"]):
                    #     cmap_label = levels[1:-1]
                    # else:
                    cmap_label = levels[1:-1:2]
                    cb.set_ticks(cmap_label)     
                    cb.ax.tick_params(labelsize=10) 
                    # add Legend title:
                    #fig.text(0.15, 0.22, 'Legende', ha="left", va="center", fontsize=16)

                    colorbarlabel_abs = colorbarlabel_abs.replace(',','\n')   
                    cb.set_label(colorbarlabel_abs, labelpad=9., fontsize=10)
                    plt.axis('off') # deativate everything
                if (iper == 1) and ((var_type == "abs-rel_change") or (var_type ==  "abs-abs_change")):
                    print("plot change")
                    left_cb,bottom_cb, width_cb, heigth_cb=(0.5,0.1, 0.3, 0.4)
                    left_cb,bottom_cb, width_cb, heigth_cb=(0.58,0.1, 0.3, 0.4)
                    if grid == "2x2":
                        left_cb,bottom_cb, width_cb, heigth_cb=(0.52,0.03, 0.4, 0.4)
                    cbr=fig.add_axes([left_cb,bottom_cb,width_cb,heigth_cb]) #0.75 # 0.95
                    cb = plt.colorbar(pcm,ax=cbr,
                          orientation='horizontal',
                          # aspect=10,
                          fraction=0.225,           # start of colorbar on the left 
                          # shrink=1.4,             # lenght of the colorbar
                          # pad=0.04,                 # distance between picture and colorbar 
                          extend='both',            # extend - show colors for out of range values
                          extendfrac='auto',       # length of extensions is oriebtated at other pathcs
                          # spacing='proportional'   # length of patch is scaled with value
                          )
                    # set ticks
                    cmap_label = levels[1:-1:2]
                    cb.set_ticks(cmap_label)
                    cb.ax.tick_params(labelsize=10) 
                    # add Legend title:
                    #fig.text(0.15, 0.22, 'Legende', ha="left", va="center", fontsize=16)
                    if var_type == "abs-rel_change":
                        colorbarlabel_change=colorbarlabel_rel_change
                    if var_type == "abs-abs_change":
                        colorbarlabel_change=colorbarlabel_abs_change

                        colorbarlabel_change=colorbarlabel_change.replace('Δ °C','K')
                    colorbarlabel_change = colorbarlabel_change.replace(',','\n')   
                    cb.set_label(colorbarlabel_change, labelpad=9., fontsize=10)
                    plt.axis('off') # deativate everything
                if (iper == 0) and (var_type not in ["abs-abs_change","abs-rel_change"]):
                    print("plot colorbar 1")
                    if ncol == 2:
                        bottom_cb, top_cb, left_cb, right_cb=(0.15,0.5, 0.1, 0.9)
                    if ncol == 3:
                        bottom_cb, top_cb, left_cb, right_cb=(0.15,0.5, 0.1, 0.9)
                    if ncol == 4:
                        bottom_cb, top_cb, left_cb, right_cb=(0.18,0.8, 0.2, 0.8)
                    if var_type == "SNR":
                        extend = "max"
                    else:
                        extend = "both"
                    cbr=fig.add_axes(position(1, 1, 1,# horizontal space between subplots
                              bottom=bottom_cb, top=top_cb,
                              left=left_cb, right=right_cb)) #0.75 # 0.95
                    cb = plt.colorbar(pcm,ax=cbr,
                          orientation='horizontal',
                          # aspect=10,
                          # fraction=0.09,           # start of colorbar on the left 
                          # shrink=1.4,             # lenght of the colorbar
                          # pad=0.04,                 # distance between picture and colorbar 
                          extend=extend,            # extend - show colors for out of range values
                          extendfrac='auto',       # length of extensions is oriebtated at other pathcs
                          # spacing='proportional'   # length of patch is scaled with value
                          )
                    # set ticks
                    if (var_type == "abs") and (indicator in ["recharge_adjust_sum","recharge_adjust_20perc_avg"]):
                        cmap_label = levels[1:-1]
                    else:
                        cmap_label = levels[1:-1:2]
                    cb.set_ticks(cmap_label)     
                    # add Legend title:
                    #fig.text(0.15, 0.22, 'Legende', ha="left", va="center", fontsize=16)

                    cb.set_label(colorbarlabel, labelpad=9., fontsize=12)
                    plt.axis('off') # deativate everything

            ll = ll + 1
        print('')
        print('  Finished meteo plotting!')
        print('')

        if (outtype == 'pdf'):
            pdf_pages.savefig(fig, dpi=600)
            plt.close()
        elif (outtype == 'png'):
            fig.savefig(figname, dpi=600) #, transparent=transparent, bbox_inches=bbox_inches, pad_inches=pad_inches)
            plt.close(fig)
        else:
            plt.show()

        if (outtype == 'pdf'):
            pdf_pages.close()
        elif (outtype == 'png'):
            pass

    if nc_write == True:

        if isfile(ncfile):
            print("netcdf already stored!")
            print("Exit")
        else:
            print("Writing netcdf file")
        if do_periods:
            dims=['time','latitude','longitude']
        else:
            dims=['deg_warm','latitude','longitude']
        if var_type in ["rel_change", "abs_change","SNR"]:
            # remove historical period if only writing changesfd
            periods=periods[1:]

        # crs, COnventions and institution are set in common_settings.py!
        nc_title = '{:} {:} HICAM {:} {:}'.format(indicator_longnames_en[indicator],var_type_longnames_en[var_type],rcp_titles[eval_rcp],ens_stat_titles[ens_stat])
        globalAttsMandatory = {'title'               : nc_title,
                               'originator'          : 'Friedrich Boeing',
                               'contact'             : 'friedrich.boeing@ufz.de',
                               'source'              : 'Data produced within HICAM and WIS-D projects. Meteorological data based on disaggregated and biascorrected EUROCORDEX climate projection data. Hydrological variables generated with mHM.',
                               'creation_date': '{:}'.format(datetime.date.today())}

        globalAttsOptional  = {'time_bnds' : '{:}'.format([str(tt) for tt in title_warm]),
                               'eval_rcp'            : eval_rcp,
                               'eval_period'         : eval_period,
                               'var_type'            : var_type,
                               'mask_region'         : mask_region}
        ncout = NcDataset(ncfile, 'w')
        ncout.createDimension(dims[0], len(title_warm))
        ncout.createDimension('bnds', 2)
        ncout.createDimension('latitude', lats.shape[0])
        ncout.createDimension('longitude', lons.shape[1])                                      

        ncout.setncatts(globalAttsFixed)
        ncout.setncatts(globalAttsMandatory)
        ncout.setncatts(globalAttsOptional)

        var = ncout.createVariable('time','i4',('time'))
        var.setncatts({'standard_name' : 'time',
                       'axis'     : 'T',
                       'units'    : 'days since 1971-01-01 00:00:00',
                       'calendar' : 'proleptic_gregorian',
                       'bounds' : 'time_bnds'},)

        times=[(datetime.datetime(pp,1,1)-datetime.datetime(1971,1,1)).days for pp in periods]
        print(times)
        var[:]= times
        # indicator_name="{:}_{:}_{:}_{:}".format(indicator,eval_period,var_type,eval_rcp)
        var = ncout.createVariable(indicator, 'f8', (dims[0], 'latitude', 'longitude'))
        var.setncatts({'long_name' : '{:} {:}'.format(indicator_longnames_en[indicator],
                                                     var_type_longnames_en[var_type]),
                       'long_name_de' : '{:} {:}'.format(indicator_longnames_de[indicator],
                                                     var_type_longnames_de[var_type]),
                       'units' : var_type_units[var_type],
                       'missing_value': -9999.,
                       '_FillValue': -9999.,
                       'cell_methods' : 'time: mean', 
                       })
        print(write_data.shape)
        var[:] = write_data
        # --------------------------------------------------
        #  -- WRITE LAT LON VARIABLES ----------------------
        # --------------------------------------------------

        var = ncout.createVariable('latitude', 'f8', ('latitude'))
        var.setncatts({'axis': 'Y',
                       'units' : 'degrees_north',
                       'standard_name' : 'latitude'},)
        var[:] = lats[:,0]
        var = ncout.createVariable('longitude', 'f8', ('longitude'))
        var.setncatts({'axis': 'X',
                       'units' : 'degrees_east',
                       'standard_name' : 'longitude'},)
        var[:] = lons[0,:]

        var = ncout.createVariable('time_bnds', 'f8', (dims[0],'bnds'))
        ends = [(datetime.datetime(periods[tt]+15,12,31)-datetime.datetime(1971,1,1)).days for tt in np.arange(len(periods))]
        starts = [(datetime.datetime(periods[tt]-14,1,1)-datetime.datetime(1971,1,1)).days for tt in np.arange(len(periods))]
        var[:] = np.column_stack([starts,ends])

        ncout.close()
