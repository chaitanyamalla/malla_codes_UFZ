
from __future__ import print_function
import numpy as np
from scipy import stats
from os.path import isfile
from sys import exit
import os
import pandas as pd
import optparse
import csv
from csv import reader

#  -- import from ufz library  ---------------------

from ufz import fread, readnc, position, get_brewer, abc2plot, astr  # dumpnetcdf,
from ufz.netcdf4 import NcDataset

#  -- import from local python scripts! ------------

from common_functions import *
from common_settings import *

indicator = ''
eval_period = ''
var_type = ''
eval_stat = ''

parser = optparse.OptionParser(usage='%prog [options]',
                               description="latex tables.")
parser.add_option('-i', '--indicator', action='store',
                  default=indicator, dest='indicator', metavar='indicator',
                  help='type of indicator')
parser.add_option('-t', '--var_type', action='store',
                  default=var_type, dest='var_type', metavar='var_type',
                  help='evaluation period (spring, winter, summer, autumn, fullyears)')
parser.add_option('-e', '--eval_period', action='store',
                  default=eval_period, dest='eval_period', metavar='eval_period',
                  help='evaluation period (spring, winter, summer, autumn, fullyears)')
# parser.add_option('-s', '--eval_stat', action='store',
#                     default=eval_period, dest='eval_stat', metavar='eval_stat',
#                     help='evaluation type (spatial statistics or ensemble statistics)')

(opts, args) = parser.parse_args()

indicator = opts.indicator
eval_period = opts.eval_period
var_type = opts.var_type
eval_stat = "ensemble"  # opts.eval_stat

del parser, opts, args

indicator_units = {'n_heatdays': "d/a",
                   'n_summerdays': "d/a",
                   'n_consec_summerdays': "d/a",
                   'n_consec_heatdays': "d/a",
                   'n_consec_droughtdays': "d",
                   'n_droughtdays_0_30cm': "d",
                   'pre_sum': 'mm',
                   'recharge_sum': 'mm',
                   'recharge_adjust_sum': 'mm',
                   'recharge_20perc': 'mm',
                   'recharge_adjust_20perc': 'mm',
                   'recharge_adjust_20perc_avg': 'mm',
                   'recharge_20perc': 'mm',
                   'tavg_mean': '°C',
                   'Qrouted_sum': 'Mio. $m^3/y$',
                   'Qrouted_daily_sum': 'Mio. $m^3/y$'
                   }

indicator_ncvarnames = {'n_heatdays': "tmax",
                        'n_summerdays': "tmax",
                        'n_consec_heatdays': "tmax",
                        'n_consec_summerdays': "tmax",
                        'n_consec_droughtdays': "SMI",
                        'n_droughtdays_0_30cm': "SMI",
                        'pre_sum': 'pre',
                        'recharge_sum': 'recharge',
                        'recharge_adjust_sum': 'recharge_adjust',
                        'recharge_20perc': 'recharge',
                        'recharge_adjust_20perc': 'recharge_adjust',
                        'recharge_adjust_20perc_avg': 'recharge_adjust',
                        'recharge_20perc': 'recharge',
                        'tavg_mean': 'tavg',
                        'Qrouted_sum': 'Qrouted',
                        'Qrouted_daily_sum': 'Qrouted'
                        }
var_type_units = {'abs': indicator_units[indicator],
                  'abs_change': u'${\\Delta}$ [' + indicator_units[indicator] + ']',
                  'rel_change': '[%]',
                  'abs-rel_change': '[%]'}
var_type_longnames_de = {'abs': "[{:}]".format(indicator_units[indicator]),
                         'abs_change': 'absolute Änderung zu 1971-2000 [${\\Delta}$ [' + indicator_units[indicator]+']',
                         'rel_change': 'relative Änderung zu 1971-2000 [%]',
                         'abs-rel_change': 'absolute Werte für die historische Zeitscheibe 1971-2000 [{:}] und zukünftige relative Änderung dazu in drei Zukunftszeitscheiben [\%].'.format(indicator_units[indicator]),
                         'abs-abs_change': u'Absolute Werte für die historische Zeitscheibe 1971-2000 [' + indicator_units[indicator] + '] und zukünftige absolute Änderung dazu in drei Zukunftszeitscheiben [${\\Delta}$ '+indicator_units[indicator]+'].'}

indicator_longnames_de = {'n_heatdays': 'mittleren Anzahl Hitzetage',
                          'n_summerdays': 'mittleren Anzahl Sommertage',
                          'n_consec_heatdays': 'mittleren Anzahl aufeinanderfolgender Hitzetage',
                          'n_consec_summerdays': 'mittleren Anzahl aufeinanderfolgender Sommertage',
                          'n_consec_droughtdays': 'mittleren Anzahl aufeinanderfolgender Tage, unter Bodenfeuchtedürre 0-30cm',
                          'recharge_20perc': '20. Perzentil Grundwasserneubildungssumme',
                          'recharge_sum': 'mittleren Grundwasserneubildungssumme (GWN)',
                          'recharge_adjust_20perc': '20. Perzentil Grundwasserneubildungssumme (GWN)',
                          'recharge_adjust_20perc_avg': '20 % mittleren Grundwasserneubildungssumme (GWN)',
                          'recharge_adjust_sum': 'mittleren Grundwasserneubildungssumme (GWN)',
                          'pre_sum': 'mittleren Niederschlagssumme',
                          'tavg_mean': 'mittleren Tagesdurchschnittstemperatur',
                          'Qrouted_sum': 'Mittlere Talsperrenzuflusssummen',
                          'Qrouted_daily_sum': 'Mittlere Talsperrenzuflusssummen'
                          }
eval_periods_de = {"year": "Jahr",
                   "summer": "Sommer",
                   "winter": "Winter",
                   "autumn": "Herbst",
                   "spring": "Frühling",
                   "veg4-10": "lange Veg.-periode",
                   "veg4-6": "Veg.-periode 1",
                   "veg7-9": "Veg.-periode 2"
                   }
eval_periods_adj_de = {"year": "jährliche",
                       "summer": "sommerliche",
                       "winter": "winterliche",
                       "autumn": "herbstliche",
                       "spring": "Frühling",
                       "veg4-10": "lange Veg.-periode",
                       "veg4-6": "Veg.-periode 1",
                       "veg7-9": "Veg.-periode 2"
                       }

if __name__ == '__main__':
    if var_type == "abs" or var_type == "abs-abs_change" or var_type == "abs-rel_change":
        if do_periods:
            title_warm = title_periods
            title_units = ['[{:}]'.format(indicator_units[indicator])]
            if var_type == "abs":
                title_units = 4*[vt_abs]
            elif var_type == "abs-abs_change":
                title_units.extend(
                    3*['[${\\Delta}$ ' + indicator_units[indicator] + ']'])
                title_units = [tt.replace('${\\Delta}$ °C', 'K')
                               for tt in title_units]
                print(3*['[${\\Delta}$ ' + indicator_units[indicator] + ']'])
                print(title_units)
            elif var_type == "abs-rel_change":
                title_units.extend(3*['[\%]'])
    else:
        if do_periods:
            title_warm = title_periods[1:]
            if var_type == "abs_change":
                title_units = 3 * \
                    ['[${\\Delta}$ ' + indicator_units[indicator] + ']']
                title_units = [tt.replace('${\\Delta}$ °C', 'K')
                               for tt in title_units]
            elif var_type == "rel_change":
                title_units = 3*['[\%]']
    print(title_units)
    var_type_name = var_type_longnames_de[var_type]
    indicator_name = indicator_longnames_de[indicator]
    var_type_name = var_type_name.replace('${\Delta}$ °C', 'K')
    eval_period_name = eval_periods_de[eval_period]
    ncvarname = indicator_ncvarnames[indicator]
    colorbarlabel = indicator_name + ' im ' + eval_period_name + \
        ' für Talsperren, die ein Einzugsgebiet größer als $50 km^2$ aufweisen. Die Einzugsgebietsgrößen (EZG) können von den tatsächlichen EZG abweichen, da kleine Zuflüsse eventuell nicht berücksichtigt werden bzw. Kanalbauten in stark anthropogen überprägten Gebieten nicht erfasst sind. Es werden ' + var_type_name

    inpath = "final_dam_csvs_corrected/decimal_corrected/daily/"
    outpath = "final_dam_csvs_corrected/decimal_corrected/daily/"

    if eval_stat == "ensemble":
        table_header = colorbarlabel + \
            " sowie statistische Kennzahlen (Minimum, 25. Perzentil, Median, arithmet. Mittel, 75. Perzentil, Maximum)' über die Teilensembles unter RCP 2.6 (21 Klima-Hydrologie-Simulationen) und RCP 8.5 (49 Klima-Hydrologie-Simulationen) gezeigt."

        types = ["_greater50facc", "_less50facc"]

        for t in types:
            latex_label = indicator + "_Talsperren" + t
            file = inpath+"Qrouted_sum_year_abs-rel_change_ensstats_updated_forlatex"+t+"_updated.csv"
            print(file)

            texfile = outpath + indicator + '_' + eval_period + \
                '_' + var_type+"_" + eval_stat+'_stat'+t+'.tex'

            th = open(texfile, 'w')
            columns = ["min", "p25", "median", "p75",
                       "max", "min", "p25", "median", "p75", "max"]
            # --------------------------------------------------
            #  -- WRITING TABLE --------------------------------
            # --------------------------------------------------

            th.write('\\renewcommand{\\arraystretch}{1.2}')
            th.write('\n')
            th.write('\\addtolength{\\tabcolsep}{-5.9pt}')
            # th.write('\setlength\\tabcolsep{0.1pt}')
            th.write('\n')
            th.write('\scriptsize')
            th.write('\n')
            th.write(
                '\\begin{longtable}{@{\extracolsep{\\fill}}lc|ccccc||ccccc}')
            th.write('\n')
            th.write('\caption{'+table_header+'}\\\\  \hline')
            #  -- write rcp column -----------------------------

            th.write('\n')

            th.write('\\multicolumn{2}{c}{} & ')
            th.write('\\multicolumn{5}{c||}{RCP 2.6}  & ')
            th.write('\\multicolumn{5}{c}{RCP 8.5}')
            th.write('\\' + '\\ \hline')
            th.write('\n')

            #  -- write columns of metrics ---------------------

            th.write('\\multicolumn{2}{c|}{} & ')
            for col in np.arange(len(columns)):
                if col == (len(columns) - 1):
                    th.write(str(columns[col]))
                else:
                    th.write(str(columns[col]) + " & ")
            # file=inpath+"Qrouted_sum_year_abs-rel_change_ensstats_updated_forlatex.csv"
            #  file="/work/malla/meteo_germany/DE_indicatorsdata/facc/write_latex/Qrouted_sum_year_abs-rel_change_ensstats_updated_forlatex_greater50facc.csv"
            with open(file, 'r', encoding="utf-8-sig") as f:
                reader = csv.reader(f,  delimiter=";")
                next(reader, None)  # ignores header in csv
                i = 4
                j = 3
                for line in reader:

                    th.write("\\\\ \n")
                    if i % 4 == 0:
                        th.write("\hline \n")
                    if j % 4 == 0:
                        th.write("\cline{2-12} \n")
                    i += 1
                    j += 1
                    for k in range(1, 13):
                        if k == range(1, 13)[-1]:
                            th.write(line[k])
                        else:
                            th.write(line[k]+" & ")

            th.write('\\' + '\\')
            th.write('\\hline')
            th.write('\n')
            th.write('\\label{' + latex_label + '}')
            th.write('\n')
            th.write('\\end{longtable}')
            th.write('\n')
            th.write('\\addtolength{\\tabcolsep}{5.9pt}')

            th.write('\n')
            th.close()
