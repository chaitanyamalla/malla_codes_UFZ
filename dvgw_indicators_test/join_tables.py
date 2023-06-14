

from __future__ import print_function
import numpy as np
from scipy import stats
from os.path import isfile
from sys import exit
import os
import pandas as pd
import optparse

#  -- import from ufz library  ---------------------

from ufz import fread,readnc, position, get_brewer, abc2plot, astr  #dumpnetcdf, 
from ufz.netcdf4 import NcDataset

#  -- import from local python scripts! ------------

from common_functions import *
from common_settings import *

indicator=''
eval_period= ''
var_type=''

parser  = optparse.OptionParser(usage='%prog [options]',
                               description="Plotting of SMI for drought monitor.")
parser.add_option('-i', '--indicator', action='store',
                    default=indicator, dest='indicator', metavar='indicator',
                    help='type of indicator')
parser.add_option('-t', '--var_type', action='store',
                    default=var_type, dest='var_type', metavar='var_type',
                    help='evaluation period (spring, winter, summer, autumn, fullyears)')
parser.add_option('-e', '--eval_period', action='store',
                    default=eval_period, dest='eval_period', metavar='eval_period',
                    help='evaluation period (spring, winter, summer, autumn, fullyears)')
parser.add_option('-s', '--eval_stat', action='store',
                    default=eval_period, dest='eval_stat', metavar='eval_stat',
                    help='evaluation type (spatial statistics or ensemble statistics)')

(opts, args) = parser.parse_args()

indicator   = opts.indicator
eval_period = opts.eval_period
var_type    = opts.var_type
eval_stat   = opts.eval_stat

del parser, opts, args

indicator_units   ={ 'n_heatdays'             : "d/a",
                     'n_summerdays'           : "d/a",
                     'n_consec_summerdays'    : "d/a",
                     'n_consec_heatdays'      : "d/a",
                     'n_consec_droughtdays'   : "d",
                     'n_droughtdays_0_30cm'   : "d",
                     'pre_sum'                : 'mm',
                     'recharge_sum'           : 'mm',
                     'recharge_adjust_sum'    : 'mm',
                     'recharge_20perc'        : 'mm',
                     'recharge_adjust_20perc' : 'mm',
                     'recharge_adjust_20perc_avg' : 'mm',
                     'recharge_20perc'        : 'mm',
                     'tavg_mean'              : '°C',
                     'Qrouted_sum'            : 'qrouted' 
}
indicator_ncvarnames  ={ 'n_heatdays'         : "tmax",
                     'n_summerdays'           : "tmax",
                     'n_consec_heatdays'      : "tmax",
                     'n_consec_summerdays'    : "tmax",
                     'n_consec_droughtdays'    : "SMI",
                     'n_droughtdays_0_30cm'    : "SMI",
                     'pre_sum'                : 'pre',
                     'recharge_sum'           : 'recharge',
                     'recharge_adjust_sum'    : 'recharge_adjust',
                     'recharge_20perc'        : 'recharge',
                     'recharge_adjust_20perc' : 'recharge_adjust',
                     'recharge_adjust_20perc_avg' : 'recharge_adjust',
                     'recharge_20perc'        : 'recharge',
                         'tavg_mean'              : 'tavg',
                           'Qrouted_sum'            : 'qrouted'
}
var_type_units   ={'abs'            : indicator_units[indicator],
                   'abs_change'     : u'${\\Delta}$ [' +indicator_units[indicator] + ']',
                   'rel_change'     : '[%]',
                   'abs-rel_change'     : '[%]'}
var_type_longnames_de={'abs'        : "[{:}]".format(indicator_units[indicator]),
                       'abs_change'     : 'absolute Änderung zu 1971-2000 [${\\Delta}$ [' + indicator_units[indicator]+']',
                       'rel_change'     : 'relative Änderung zu 1971-2000 [%]',
                       'abs-rel_change'     : 'Absolute Werte für die historische Zeischeibe 1971-2000 [{:}] und zukünftige relative Änderung dazu in drei Zukunftszeitscheiben [%].'.format(indicator_units[indicator]),
                       'abs-abs_change'     : u'Absolute Werte für die historische Zeischeibe 1971-2000 ['+ indicator_units[indicator] +'] und zukünftige absolute Änderung dazu in drei Zukunftszeitscheiben [${\\Delta}$ '+indicator_units[indicator]+'].'}

indicator_longnames_de={'n_heatdays'             : 'mittleren Anzahl Hitzetage',
                        'n_summerdays'           : 'mittleren Anzahl Sommertage',
                        'n_consec_heatdays'      : 'mittleren Anzahl aufeinanderfolgender Hitzetage',
                        'n_consec_summerdays'    : 'mittleren Anzahl aufeinanderfolgender Sommertage',
                        'n_consec_droughtdays'    : 'mittleren Anzahl aufeinanderfolgender Tage, unter Bodenfeuchtedürre 0-30cm',
                        'recharge_20perc'        : '20. Perzentil Grundwasserneubildungssumme',
                        'recharge_sum'           : 'mittleren Grundwasserneubildungssumme (GWN)',
                        'recharge_adjust_20perc' : '20. Perzentil Grundwasserneubildungssumme (GWN)',
                        'recharge_adjust_20perc_avg' : '20 % mittleren Grundwasserneubildungssumme (GWN)',
                        'recharge_adjust_sum'    : 'mittleren Grundwasserneubildungssumme (GWN)',
                        'pre_sum'                : 'mittleren Niederschlagssumme',
                        'tavg_mean'              : 'mittleren Tagesdurchschnittstemperatur',
                        'Qrouted_sum'            : 'xxxxxxxxxxxxxxxxxxx'
}
eval_periods_de={"year"      : "Jahr",
                 "summer"    : "Sommer",
                 "winter"    : "Winter",
                 "autumn"    : "Herbst",
                 "spring"    : "Frühling",
                 "veg4-10"   : "lange Veg.-periode",
                 "veg4-6"    : "Veg.-periode 1",
                 "veg7-9"    : "Veg.-periode 2"
                 }
eval_periods_adj_de={"year"      : "jährliche",
                 "summer"    : "sommerliche",
                 "winter"    : "winterliche",
                 "autumn"    : "herbstliche",
                 "spring"    : "Frühling",
                 "veg4-10"   : "lange Veg.-periode",
                 "veg4-6"    : "Veg.-periode 1",
                 "veg7-9"    : "Veg.-periode 2"
                 }
if __name__ == '__main__':
    if var_type == "abs" or var_type == "abs-abs_change" or var_type == "abs-rel_change":
        if do_periods:
            title_warm      = title_periods
            title_units          = ['[{:}]'.format(indicator_units[indicator])]
            if var_type == "abs":
                title_units     = 4*[vt_abs]
            elif var_type == "abs-abs_change":
                title_units.extend(3*['[${\\Delta}$ ' + indicator_units[indicator] + ']'])
                title_units=[ tt.replace('${\\Delta}$ °C','K') for tt in title_units]
                print(3*['[${\\Delta}$ ' + indicator_units[indicator] + ']'])
                print(title_units)
            elif var_type == "abs-rel_change":
                title_units.extend(3*['[\%]'])
        
    else:
        if do_periods:
            title_warm      = title_periods[1:]
            if var_type == "abs_change":
                title_units     = 3*['[${\\Delta}$ ' + indicator_units[indicator] + ']']
                title_units=[ tt.replace('${\\Delta}$ °C','K') for tt in title_units]
            elif var_type == "rel_change":
                title_units     = 3*['[\%]']

    print(title_units)
    var_type_name=var_type_longnames_de[var_type]
    indicator_name=indicator_longnames_de[indicator]
    var_type_name=var_type_name.replace('${\Delta}$ °C','K')
    eval_period_name=eval_periods_de[eval_period]
    ncvarname=indicator_ncvarnames[indicator]

    colorbarlabel  = indicator_name +' im ' + eval_period_name  + ', ' + var_type_name 
    inpath="./tables_periods"
    outpath="./tables_periods_main_catchments/"
    main_catch_names=["Maas","Donau","Rhein","Oder","Weser","Warnow-Peene","Eider","Elbe","Schlei-Trave","Ems"]
    main_catch_names_short=["Maas","Donau","Rhein","Oder","Weser","W-P","Eider","Elbe","S-T","Ems"]

    if eval_stat == "ensemble":
        
        table_header=colorbarlabel+ ": Mittelwert über die Haupteinzugsgebiete (Abkürzungen W-P: Warnow-Peene, S-T: Schlei-Trave) und statistische Kennzahlen (Minimum, 25. Perzentil, Median, arithmetisches Mittel, 75. Perzentil, Maximum) über die Ensemblemitglieder aus RCP 2.6 und RCP 8.5. "
        table_header='Änderungen der ' + indicator_name + ' im ' + eval_period_name + ' über die Teilensembles unter RCP 2.6 (21 Klima-Hydrologie-Simulationen) und RCP 8.5 (49 Klima-Hydrologie-Simulationen). ' +   var_type_name+ ' Gezeigt werden die \\textbf{statistischen Kennzahlen über die Teilensembles unter RCP 2.6 und RCP 8.5} (Minimum, 25. Perzentil, Median, arithmet. Mittel, 75. Perzentil, Maximum) der Haupteinzugsgebiete (Abkürzungen W-P: Warnow-Peene, S-T: Schlei-Trave). Das Minimum bescheibt die größte mögliche Abnahme, das Maximum die größte mögliche Zunahme des Indikators innerhalb der Teilensemble. Der Median stellt im Rahmen der Modellunsicherheiten jeweils die wahrscheinlichste zukünftige Änderung dar.'
        if ncvarname == "recharge" or ncvarname == "recharge_adjust":
            table_header = table_header + ' Die insgesamt 70 Simulationen der GWN wurden jeweils mit dem hydrologischen Modell mHM durchgeführt.'
        filename=outpath + indicator + '_' + eval_period + '_' + var_type + '_maincatchments_ensemblestat.tex'
    elif eval_stat == "spatial":
        table_header=colorbarlabel+ ": Räumliche Statistische Kennzahlen (Minimum, 25. Perzentil, Median, arithmet. Mittel, 75. Perzentil, Maximum) der Haupteinzugsgebiete (Abkürzungen W-P: Warnow-Peene, S-T: Schlei-Trave). Gezeigt wird der Ensemble Median für jeweils RCP 2.6 und RCP 8.5."

        table_header='Änderungen der ' + indicator_name + ' im ' + eval_period_name + ' des Ensemble-Medians über jeweils alle Simulationen unter RCP 2.6 (21 Klima-Hydrologie-Simulationen) und RCP 8.5 (49 Klima-Hydrologie-Simulationen). Gezeigt werden die \\textbf{räumlichen statistischen Kennzahlen des Ensemble-Medians} (Minimum, 25. Perzentil, Median, arithmet. Mittel, 75. Perzentil, Maximum) der Haupteinzugsgebiete (Abkürzungen W-P: Warnow-Peene, S-T: Schlei-Trave). ' + var_type_name
        if ncvarname == "recharge" or ncvarname == "recharge_adjust":
            table_header = table_header + ' Die Berechnung der GWN erfolgte jeweils mit dem hydrologischen Modell mHM.'
        filename=outpath + indicator + '_' + eval_period + '_' + var_type + '_maincatchments_spatialstat.tex'


    th = open(filename, 'w')
    columns=["min","p25","median","mean","p75","max","min","p25","median","mean","p75","max"]
    # --------------------------------------------------
    #  -- WRITING TABLE --------------------------------
    # --------------------------------------------------

    th.write('\\begin{table}[H]') # H need package float \usepackage{float}
    th.write('\n')
    th.write('\scriptsize')
    th.write('\n')
    th.write('\caption{' + table_header.replace('%','\%') +'}' )
    #  -- write rcp column -----------------------------

    th.write('\n')
    th.write('\\begin{tabular}{ll|r|r|r|r|r|r||r|r|r|r|r|r}')
    th.write('\n')

    th.write('\\multicolumn{2}{c}{} & ')
    th.write('\\multicolumn{6}{c||}{RCP 2.6}  & ')
    th.write('\\multicolumn{6}{c}{RCP 8.5}')
    th.write('\\' + '\\')
    th.write('\n')

    #  -- write columns of metrics ---------------------

    th.write('\\multicolumn{2}{c}{} & ')
    for col in np.arange(len(columns)):
        if col == (len(columns) - 1):
            th.write(str(columns[col]))  
        else:
            th.write(str(columns[col]) + " & ")
    th.write('\\' + '\\')
    th.write('\\hline')
    th.write('\n')
    
    #  -- write data -----------------------------------

    for catch,catch_name in enumerate(main_catch_names):
        # print(catch_name)
        th.write('\\multirow{3}{*}{\\rotatebox[origin=c]{90}{'+ main_catch_names_short[catch] + '}}  & ')
        tablebase        = '{:}/{:}_{:}_{:}'.format(inpath,indicator,eval_period,var_type)
        if eval_stat == "ensemble":

            infile_rcp26     = tablebase + "_rcp26"+ "_spatialmean_{:}_ensemblestat.csv".format(catch_name)
            infile_rcp85     = tablebase + "_rcp85"+ "_spatialmean_{:}_ensemblestat.csv".format(catch_name)
        elif eval_stat == "spatial":
            infile_rcp26     = tablebase + "_rcp26"+ "_ensmedian_{:}_spatialstat.csv".format(catch_name)
            infile_rcp85     = tablebase + "_rcp85"+ "_ensmedian_{:}_spatialstat.csv".format(catch_name)

        dat_rcp26=np.array(pd.read_csv(infile_rcp26,index_col=0))
        # print(dat_rcp26)
        dat_rcp85=np.array(pd.read_csv(infile_rcp85,index_col=0))
        for rr,row in enumerate(title_warm):
            # print(row)
            if rr == 0:
                th.write(str(title_warm[rr] + ' ' + title_units[rr]) + " & ")
            else:
                th.write(" & " + str(title_warm[rr] + ' ' + title_units[rr]) + " & ")

            for cc in range(dat_rcp26.shape[1]):
                tt = dat_rcp26[rr,cc]
                # put + sign for change data
                if rr > 0:
                    if np.sign(tt) == 1:
                        tt = "+{:}".format(tt)
                    else:
                        tt = "{:}".format(tt)
                else:
                    tt = "{:}".format(tt)

                th.write("{:} &".format(tt))
            for cc in range(dat_rcp85.shape[1]):
                tt = dat_rcp85[rr,cc]
                # put + sign for change data
                if rr > 0:
                    if np.sign(tt) == 1:
                        tt = "+{:}".format(tt)
                    else:
                        tt = "{:}".format(tt)
                else:
                    tt = "{:}".format(tt)
                # write the data:
                if cc < (len(dat_rcp85[1]) -1):
                    th.write("{:} & ".format(tt))
                else:
                    th.write("{:}".format(tt))

            th.write('\\' + '\\')
            if rr == 0 and (var_type == "abs-abs_change" or "abs-rel_change"):
                th.write('\\cline{2-14}') # needs package
            th.write('\n')
        th.write('\\hline')
        th.write('\n')
        
    th.write('\\end{tabular}')
    th.write('\n')
    th.write('\\end{table}')
    th.close()
