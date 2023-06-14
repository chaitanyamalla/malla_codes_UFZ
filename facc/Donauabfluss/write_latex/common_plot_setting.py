#!/usr/bin/env python

import pandas as pd
import numpy as np
from ufz import fread,readnc, position, get_brewer, abc2plot, astr  #dumpnetcdf, 
#  COMMAND LINE ARGUMENTS ###################
pdffile  = ''
pngbase  = ''
eval_period= ''
eval_rcp=''
# ncvarname=''

var_type=''
mask_region=''
language='German'
indicator=''
import optparse
parser  = optparse.OptionParser(usage='%prog [options]',
                               description="Plotting of SMI for drought monitor.")
parser.add_option('-p', '--pdffile', action='store', dest='pdffile', type='string',
                  default=pdffile, metavar='File',
                  help='Name of pdf output file (default: open X-window).')
parser.add_option('-g', '--pngbase', action='store',
                    default=pngbase, dest='pngbase', metavar='pngbase',
                    help='Name basis for png output files (default: open screen window).')



parser.add_option('-e', '--eval_period', action='store',
                    default=eval_period, dest='eval_period', metavar='eval_period',
                    help='evaluation period (spring, winter, summer, autumn, fullyears)')

parser.add_option('-t', '--var_type', action='store',
                    default=var_type, dest='var_type', metavar='var_type',
                    help='var_types (abs, abs_change, abs-abs, abs-rel)')
parser.add_option('-r', '--eval_rcp', action='store',
                    default=eval_rcp, dest='eval_rcp', metavar='eval_rcp',
                    help='type of indicator')
parser.add_option('-i', '--indicator', action='store',
                    default=indicator, dest='indicator', metavar='indicator',
                    help='type of indicator')
parser.add_option('-m', '--mask_region', action='store',
                    default=mask_region, dest='mask_region', metavar='mask_region',
                    help='mask of region.')
parser.add_option('-l', '--language', action='store',
                    default=language, dest='language', metavar='language',
                    help='label language.')
parser.add_option('-s', '--ens_stat', action='store',
                    default=language, dest='ens_stat', metavar='ens_stat',
                    help='Statistic over ensemble.')

(opts, args) = parser.parse_args()

pdffile     = opts.pdffile
pngbase     = opts.pngbase
eval_period = opts.eval_period
eval_rcp    = opts.eval_rcp
# ncvarname   = opts.ncvarname
var_type    = opts.var_type
indicator   = opts.indicator
mask_region = opts.mask_region
language    = opts.language
ens_stat    = opts.ens_stat

del parser, opts, args

if (pdffile != '') & (pngbase != ''):
    raise ValueError('PDF and PNG are mutually exclusive. Only either -p or -g possible.')

if (pdffile == ''):
    if (pngbase == ''):
        outtype = 'x'
    else:
        outtype = 'png'
else:
    outtype = 'pdf'
indicator_options =['pre','pre_sum', 'n_heatdays','n_summerdays', 'n_consec_heatdays',
                    'n_consec_summerdays','recharge_adjust_sum','recharge_sum',
                    'recharge_adjust_20perc','recharge_adjust_20perc_avg','recharge_20perc',
                    'tavg_mean', 'n_consec_droughtdays','n_droughtdays_0_30cm','aET_sum','PET_sum',"Qrouted_p10",
                    'pre_gt10', 'pre_gt20','pre_90p','pre_95p','pre_99p',
"pre_gt0p1_R90p","pre_gt0p1_R95p","pre_gt0p1_R99p","pre_gt1_R90p","pre_gt1_R95p","pre_gt1_R99p",
                   ]
if indicator not in indicator_options:
    raise IOError('***ERROR: define indicator by setting -i to: {:}'.format(str(indicator_options)) )
# var_options =['pre', 'tmax','recharge_adjust','recharge']
# if ncvarname not in var_options:
#     raise IOError('***ERROR: define ncvarname by setting -v to: {:}'.format(str(var_options)) )
var_type_options =['rel_change', 'abs_change', 'abs', 'abs-abs_change', 'abs-rel_change']
if var_type not in var_type_options:
    raise IOError('***ERROR: define var_type by setting -t to: {:}'.format(str(var_type_options)) )
eval_options=["summer", "winter", "spring", "autumn", "year","veg4-10","veg4-6","veg7-9","shy","why"]
if eval_period not in eval_options:
    raise IOError('***ERROR: define eval_period by setting -e to: {:}'.format(str(eval_options)) )
rcp_options =['rcp26', 'rcp45', 'rcp85','rcpall']
if eval_rcp not in rcp_options:
    raise IOError('***ERROR: define rcp_eval by setting -r to: {:}'.format(str(rcp_options)) )
region_options =['de_hicam', 'germany', 'MDR','TH','BY','SN',"ww_leipzig_ug"]
if mask_region not in region_options:
    raise IOError('***ERROR: define mask_region by setting -m to: {:}'.format(str(region_options)) )
language_options       = ['German', 'English']
if language not in language_options:
    raise IOError('***ERROR: language not available, set to: {:}'.format(str(language_options)) )
ens_stat_options       = ['ensmedian', 'ensminimum','ensp90','ensmaximum','worstcase']
if ens_stat not in ens_stat_options:
    raise IOError('***ERROR: ensemble statistics not available, set to: {:}'.format(str(ens_stat_options)) )

# Main plot
textsize   = 12          # standard text size
hspace     = 0.01        # x-space between subplots
wspace     = 0.15       # y-space between subplots
dxabc      = 0.05        # % of (max-min) shift to the right from left y-axis for a,b,c,... labels
dyabc      = 0.90        # % of (max-min) shift up from lower x-axis for a,b,c,... labels

lwidth     = 0.5         # linewidth
elwidth    = 1.0         # errorbar line width
alwidth    = 1.0         # axis line width
msize      = 1.0         # marker size
mwidth     = 0.5         # marker edge width
# color: 'b'|'g'|'r'|'c'|'m'|'y'|'k'|'w'
#        'blue'|'green'|'red'|'cyan'|'magenta'|'yellow'|'black'|'white'
#        hex string '#eeefff' | RGB tuple (1,0.5,1) | html names 'burlywod', 'chartreuse', ...
#        grayscale intensity, e.g. '0.7', 'k'='0.0'
myBlue          = '#00589C'
myLightBlue     = '#E5F4FF'
FigLightBlue    = '#6FA6B9'
otherBlue       = '#6FA6FF'     # rgb = 111,166,255
myRed           = '#CA373B'
myOrange        = '#FDAE61'
mcol1      = (202/255.,0/255.,32/255.)     # primary marker colour
mcol2      = '0.0'       # color of second markers
mcol3      = '0.0'       # color of third markers
lcol1      = (5/255.,113/255.,176/255.)       # primary line colour
lcol2      = '0.0'       # color of second lines
lcol3      = '0.0'       # color of third lines

# Legend
llxbbox    = -0.01       # y-anchor legend bounding box
llybbox    = 0.04        # y-anchor legend bounding box
llrspace   = 0.          # spacing between rows in legend
llcspace   = 1.0         # spacing between columns in legend
llhtextpad = 0.4         # the pad between the legend handle and text
llhlength  = 1.5         # the length of the legend handles
frameon    = False       # if True, draw a frame around the legend. If None, use rc
llxbbox2    = 0.60       # Tight bounding of symbol and text (w/o lines)
llhtextpad2 = 0.         #                   "
llhlength2  = 1.0        #                   "

grid = "2x2"
if ((var_type == "abs-rel_change") or (var_type ==  "abs-abs_change")):
    if grid == "2x2":
        if mask_region == "ww_leipzig_ug":

            figsize=(8,8)
        else:
            figsize=(8,10)
        nrow       = 2
        ncol       = 2
        left_plot  = 0.05
        top_plot   = 0.95
    else:
        figsize=(10,4)
        nrow       = 1
        ncol       = 4
        left_plot  = 0.08
        top_plot   = 0.95
else:
    figsize=(10,6)
    nrow       = 1
    ncol       = 4
    left_plot  = 0.05
    top_plot   = 0.95

# PNG
dpi         = 300
transparent = False
bbox_inches = 'tight'
pad_inches  = 0
import matplotlib as mpl
import matplotlib.pyplot as plt

if (outtype == 'pdf'):
    mpl.use('PDF') # set directly after import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    # Customize: http://matplotlib.sourceforge.net/users/customizing.html
    mpl.rc('ps', papersize='a4', usedistiller='xpdf') # ps2pdf
elif (outtype == 'png'):
    mpl.use('Agg') # set directly after import matplotlib
    import matplotlib.pyplot as plt
    # mpl.rc('text.latex', unicode=True)
    mpl.rc('savefig', dpi=dpi, format='png')
else:
    import matplotlib.pyplot as plt

#mpl.rc('font',       **{'family':'serif','serif':['times']})
mpl.rcParams['text.latex.preamble']=r'\usepackage{wasysym}' 
mpl.rc('font',       size=textsize)
mpl.rc('lines',      linewidth=lwidth, color='black')
mpl.rc('axes',       linewidth=alwidth, labelcolor='black')
mpl.rc('path',       simplify=False) # do not remove
#mpl.rc('figure',      figsize=(11.69,8.27)) # a4 landscape
mpl.rc('figure',      figsize=(8.27,11.69/2.75))
mpl.rc('legend',     fontsize=textsize)
#mpl.rc('text',       usetex=True)
#mpl.rc('text.latex', unicode=True)

# -----------------------------------------------------------------------------
# PLOT natural features
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# geographical features
ocean         = cfeature.NaturalEarthFeature(category='physical', name='ocean',
                                             scale='50m',
                                             facecolor=cfeature.COLORS['water'])
state_borders = cfeature.NaturalEarthFeature(category='cultural', name='admin_0_countries',
                                             scale='10m',
                                             edgecolor='0.2',
                                             facecolor=cfeature.COLORS['land'])


import cartopy.feature as cfeature
from cartopy.feature import ShapelyFeature
import cartopy.io.shapereader as shpreader

shpf_fedcon = '/data/hydmet/WIS_D/shapes/BuLaender.shp'
reader    = shpreader.Reader(shpf_fedcon)
fed_count = ShapelyFeature(reader.geometries(), ccrs.PlateCarree())



#  -- main catchments of Germany -------------------

shp_file = '/data/hydmet/WIS_D/shapes/main_catch_ger_epsg4326.shp'
mask_main_catch_path="/data/hydmet/WIS_D/masks/mask_main_river/mask_main_catchments_ger.nc"
reader    = shpreader.Reader(shp_file)
main_catch_ger = ShapelyFeature(reader.geometries(), ccrs.PlateCarree())
main_catch_names=["Maas","Donau","Rhein","Oder","Weser","Warnow-Peene","Eider","Elbe","Schlei-Trave","Ems"]

crs_latlon = ccrs.PlateCarree()
projection = ccrs.Miller(central_longitude=10.0)
        

#  -- latlon file ----------------------------------

# read latitude and longitude
# file containing latitude and longitude grid
latlon_file   = '/data/hicam/data/processed/mhm_input/de_hicam/latlon/latlon_0p015625.nc'
# latlon_file   = './latlon_0p015625.nc'
lats          = readnc(latlon_file, var='lat')
lons          = readnc(latlon_file, var='lon')


facc_file="/data/hicam/data/processed/mhm_output/de_hicam/v2/calib151/restart/mRM_restart_001.nc"
facc = readnc(facc_file, 'L11_fAcc')
facc_mask = (facc < 350)

# map_extent    = [-10, 28, 34.5, 70] # for LambertAzimuthalEqualArea
map_extent    = [5.7, 15.1, 47.2, 55]
BL = {
    'HH' : ('Hamburg'),
    'NI' : ('Niedersachsen'),
    'HB' : ('Bremen'),
    'NRW' : ('Nordrhein-Westfalen'),
    'HE' : ('Hessen'),
    'RP' : ('Rheinland-Pfalz'),
    'BW' : ('Baden-Württemberg'),
    'BY' : ('Bayern'),
    'SL' : ('Saarland'),
    'BE' : ('Berlin'),
    'BB' : ('Brandenburg'),
    'MV' : ('Mecklenburg-Vorpommern'),
    'SN' : ('Sachsen'),
    'ST' : ('Sachsen-Anhalt'),
    'TH' : ('Thüringen'),
    'SH' : ('Schleswig-Holstein'),
    'NDR' : ('Hamburg','Niedersachsen','Bremen','Mecklenburg-Vorpommern','Schleswig-Holstein'),
    'MDR' :  ('Sachsen','Sachsen-Anhalt','Thüringen'),
    'BE-BB' : ('Berlin', 'Brandenburg'),
    'SH-HH' : ('Schleswig-Holstein', 'Hamburg'),
    'NI-HB' : ('Niedersachsen', 'Bremen'),
    'RP-SL' : ('Rheinland-Pfalz', 'Saarland'),
    }

# region                  = "germany"
# region                  = "de_hicam"
# region                  = "MDR"
if mask_region == "germany":
    mask_path               = "/data/hicam/data/processed/dem_OR/mask_hicam_1km_g_inv.nc"
    extent                  = [5.7, 15.1, 47.2, 55]
elif mask_region == "de_hicam":
    mask_path               = "/data/hicam/data/processed/dem_OR/mask_hicam_1km_ghw_inv.nc"
    extent                  = [5.0, 20.0, 46.0, 56.0]

elif mask_region == "ww_leipzig_ug":
    mask_path               = "/data/hydmet/WIS_D/ww_leipzig/input/masks/mask_untersuchungsgebiet_grid.nc"
    extent                  = pd.read_csv("/data/hydmet/WIS_D/ww_leipzig/input/masks/extent_untersuchungsgebiet",header=1,
                                          )
    extent                  =[np.float(ex) for ex in extent]
    file_ug                 = "/data/hydmet/WIS_D/ww_leipzig/input/shapes/Abfragerahmen33N_epsg4326.shp"
    reader    = shpreader.Reader(file_ug)
    shape_ug                = ShapelyFeature(reader.geometries(), ccrs.PlateCarree())
    file_vg                 = "/data/hydmet/WIS_D/ww_leipzig/input/shapes/WA_Versorgungsgebiet_epsg4326.shp"
    reader    = shpreader.Reader(file_vg)
    shape_vg                = ShapelyFeature(reader.geometries(), ccrs.PlateCarree())
    projection = ccrs.UTM(33)
    print(extent)
else:
    mask_path  = "/data/hydmet/WIS_D/masks/mask_ger_{:}.nc".format(mask_region)
    def sel_region(x):
        """Subregion selection for printing: ax.set_extent """
        return{
            'BRD': [5.75, 15.25, 47.25, 55],
            'TH': [9.7, 12.8, 50.1, 51.7],
            'ST': [10, 13.7, 50.8, 53.2],
            'BB': [11, 15, 51.3, 53.6],
            'HE': [7, 11, 49, 52],
            'SN': [11.8, 15.1, 50.15, 51.72],
            'MDR': [9.7, 15.1, 50, 53.3],
            'SH': [7.5, 12, 53.3, 55.2],
            'NRW': [5.75, 9.5, 50.3, 52.55],
            'NDR': [5.75, 15.25, 51.2, 55.2],
            'NI': [6.5, 11.75, 51.2, 54],
            'HH' : [8.27, 10.47, 53.29, 54.06],
            'HB' : [8.33, 9.13, 52.91, 53.71],
            'MV': [10.44, 14.56, 53.02, 54.78],
            'NRW' : [5.72, 9.6, 50.22, 52.63],
            'RP' : [5.97, 8.66, 48.87, 51.04],
            'SL': [6.21, 7.55, 49.01, 49.74],
            'BW' : [7.36, 10.64, 47.43, 49.89],
            'BY' : [8.83, 13.99, 47.17, 50.66],
            'ST' : [10.41, 13.34, 50.84, 53.14],
            'BE' : [12.94, 13.91, 52.24, 52.77],
            'BE-BB': [11, 15, 51.3, 53.6],
            'SH-HH': [7.5, 12, 53.3, 55.2],
            'NI-HB': [6.5, 11.75, 51.2, 54],
            'RP-SL': [5.97, 8.66, 48.87, 51.04]
        }.get(x, [5.75, 15.25, 47.25, 55])
    extent = sel_region(mask_region)

language_ending={'German' : 'de',
                 'English' : 'en'}
indicator_units   ={ 'n_heatdays'             : "d/a",
                     'n_summerdays'           : "d/a",
                     'n_consec_summerdays'    : "d/a",
                     'n_consec_heatdays'      : "d/a",
                     'n_consec_droughtdays'   : "d",
                     'n_droughtdays_0_30cm'   : "d",
                     'pre_sum'                : 'mm',
                     'PET_sum'                : 'mm',
                     'aET_sum'                : 'mm',
                     'recharge_sum'           : 'mm',
                     'recharge_adjust_sum'    : 'mm',
                     'recharge_20perc'        : 'mm',
                     'recharge_adjust_20perc' : 'mm',
                     'recharge_adjust_20perc_avg' : 'mm',
                     'recharge_20perc'        : 'mm',
                     'tavg_mean'              : '°C',
                     'Qrouted_p10'            : 'Q/s',
                     'pre_gt10'              : 'd/year',
                     'pre_gt20'              : 'd/year',
                     'pre_90p'                : 'mm/day',
                     'pre_95p'                : 'mm/day',
                     'pre_99p'                : 'mm/day',
                     'pre_gt0p1_R90p'         : 'mm/day',
                     'pre_gt0p1_R95p'         : 'mm/day',
                     'pre_gt0p1_R99p'         : 'mm/day',
                     'pre_gt1_R90p'           : 'mm/day',
                     'pre_gt1_R95p'           : 'mm/day',
                     'pre_gt1_R99p'           : 'mm/day',
                     
                     }
indicator_ncvarnames  ={ 'n_heatdays'         : "tmax",
                     'n_summerdays'           : "tmax",
                     'n_consec_heatdays'      : "tmax",
                     'n_consec_summerdays'    : "tmax",
                     'n_consec_droughtdays'    : "SMI",
                     'n_droughtdays_0_30cm'    : "SMI",
                     'pre_sum'                : 'pre',
                     'aET_sum'                : 'aET',
                     'PET_sum'                : 'pet',
                     'recharge_sum'           : 'recharge',
                     'recharge_adjust_sum'    : 'recharge_adjust',
                     'recharge_20perc'        : 'recharge',
                     'recharge_adjust_20perc' : 'recharge_adjust',
                     'recharge_adjust_20perc_avg' : 'recharge_adjust',
                     'recharge_20perc'        : 'recharge',
                     'tavg_mean'              : 'tavg',
                     'Qrouted_p10'            : 'Qrouted',
                     'pre_gt10'               : 'pre_gt10',
                     'pre_gt20'               : 'pre_gt20',
                     'pre_90p'                : 'pre_90p',
                     'pre_95p'                : 'pre_95p',
                     'pre_99p'                : 'pre_99p',
                     'pre_gt0p1_R90p'         : 'pre_gt0p1_R90p',
                     'pre_gt0p1_R95p'         : 'pre_gt0p1_R95p',
                     'pre_gt0p1_R99p'         : 'pre_gt0p1_R99p',
                     'pre_gt1_R90p'           : 'pre_gt1_R90p',
                     'pre_gt1_R95p'           : 'pre_gt1_R95p',
                     'pre_gt1_R99p'           : 'pre_gt1_R99p' ,
                     
                     }
var_type_units   ={'abs'            : indicator_units[indicator],
                   'abs_change'     : u'Δ {:}'.format(indicator_units[indicator]),
                   'rel_change'     : '[%]',
                   'abs-rel_change' : '1971-2000 ' + indicator_units[indicator] + '[%]',
                   'abs-abs_change' : indicator_units[indicator]}
var_type_longnames_en={'abs'        : "[{:}]".format(indicator_units[indicator]),
                       'abs_change'     : u'absolute change to 1971-2000 [Δ {:}]'.format(indicator_units[indicator]),
                       'rel_change'     : 'relative change to 1971-2000 [%]',
                       'abs-rel_change'     : '1971-2000 [{:}] and relative change to 1971-2000 [%]'.format(indicator_units[indicator]),
                       'abs-abs_change'     : '1971-2000 [{:}] and absolute change to 1971-2000 [Δ {:}]'.format(indicator_units[indicator],indicator_units[indicator])}


var_type_longnames_de={'abs'        : "[{:}]".format(indicator_units[indicator]),
                       'abs_change'     : 'absolute Änderung zu 1971-2000 [Δ {:}]'.format(indicator_units[indicator]),
                       'rel_change'     : 'relative Änderung zu 1971-2000 [%]',
                       'abs-rel_change'     : '1971-2000 [{:}] und relative Änderung zu 1971-2000 [%]'.format(indicator_units[indicator]),
                       'abs-abs_change'     : u'1971-2000 [{:}] und absolute Änderung zu 1971-2000 [Δ {:}]'.format(indicator_units[indicator],indicator_units[indicator])}
indicator_longnames_en={'n_heatdays'             : 'number of heatdays',
                        'n_summerdays'           : 'number of summerdays',
                        'n_consec_heatdays'      : 'number of consecutive heatdays',
                        'n_consec_summerdays'    : 'number of consecutive summerdays',
                        'n_consec_droughtdays'   : 'number of consecutive days under SM drought',
                        'n_droughtdays_0_30cm'   : 'number of days under SM drought (0-30cm)',
                        'recharge_20perc'        : '20th percentile recharge sum',
                        'recharge_adjust_20perc' : '20th percentile recharge sum',
                        'recharge_adjust_20perc_avg' : '20 % of avg. recharge sum',
                        'recharge_sum'           : 'average recharge sum',
                        'pre_sum'                : 'average precipitation sum',
                        'PET_sum'                : 'average actual ET sum',
                        'aET_sum'                : 'average potential ET sum',
                        'recharge_adjust_sum'    : 'average recharge sum',
                        'Qrouted_p10'    : '',
                        'tavg_mean'              : 'average Temperature',
                        'pre_gt10'              : 'average days above 10 mm rain per year',
                        'pre_gt20'              : 'average days above 20 mm rain per year',
                        'pre_90p'                : '90th percentile of daily rain sums',
                        'pre_95p'                : '95th percentile of daily rain sums',
                        'pre_99p'                : '98th percentile of daily rain sums',
                        'pre_gt0p1_R90p'         : '90th percentiles of daily precip above 0.1 mm',
                        'pre_gt0p1_R95p'         : '95th percentiles of daily precip above 0.1 mm',
                        'pre_gt0p1_R99p'         : '99th percentiles of daily precip above 0.1 mm',
                        'pre_gt1_R90p'           : '90th percentiles of daily precip above 1 mm',
                        'pre_gt1_R95p'           : '95th percentiles of daily precip above 1 mm',
                        'pre_gt1_R99p'           : '99th percentiles of daily precip above 1 mm',
                       }
                        

indicator_longnames_de={'n_heatdays'             : 'mittl. Anzahl Hitzetage',
                        'n_summerdays'           : 'mittl. Anzahl Sommertage',
                        'n_consec_heatdays'      : 'mittl. Anzahl aufeinanderfolgender Hitzetage',
                        'n_consec_summerdays'    : 'mittl. Anzahl aufeinanderfolgender Sommertage',
                        'n_consec_droughtdays'    : 'mittlere Anzahl aufeinanderfolgender Tage unter Bodenfeuchtedürre 0-30cm',
                        'n_droughtdays_0_30cm'    : 'mittlere Anzahl Tage unter Bodenfeuchtedürre (0-30cm),',
                        'recharge_20perc'        : '20. Perzentil Grundwasserneubildungssumme',
                        'recharge_sum'           : 'mittl. Grundwasserneubildungssumme',
                        'recharge_adjust_20perc' : '20. Perzentil Grundwasserneubildungssumme',
                        'recharge_adjust_20perc_avg' : '20 % mittl. Grundwasserneubildungssumme',
                        'recharge_adjust_sum'    : 'mittlere Grundwasserneubildungssumme',
                        'pre_sum'                : 'mittl. Niederschlagssumme',
                        'aET_sum'                : 'mittl. aktuelle Evapotranspirationssumme',
                        'PET_sum'                : 'mittl. potentielle Evapotranspirationssumme',
                        'tavg_mean'              : 'mittl. Tagesdurchschnittstemperatur',
                        'Qrouted_p10'    : '10-Perzentil des Abfluss',
                        'pre_gt10'              : 'Tage über 10 mm Niederschlag',
                        'pre_gt20'              : 'Tage über 20 mm Niederschlag',
                        'pre_90p'                : '90 Perzentil der täglichen Niederschlagssummen',
                        'pre_95p'                : '95 Perzentil der täglichen Niederschlagssummen',
                        'pre_99p'                : '98 Perzentil der täglichen Niederschlagssummen',
                        'pre_gt0p1_R90p'         : '90 Perzentil der täglichen Niederschlagssummen über 0,1mm Niederschlag',
                        'pre_gt0p1_R95p'         : '95 Perzentil der täglichen Niederschlagssummen über 0,1mm Niederschlag',
                        'pre_gt0p1_R99p'         : '99 Perzentil der täglichen Niederschlagssummen über 0,1mm Niederschlag',
                        'pre_gt1_R90p'           : '90 Perzentil der täglichen Niederschlagssummen über 1mm Niederschlag',
                        'pre_gt1_R95p'           : '95 Perzentil der täglichen Niederschlagssummen über 1mm Niederschlag',
                        'pre_gt1_R99p'           : '99 Perzentil der täglichen Niederschlagssummen über 1mm Niederschlag',
                    
                     }
rcp_titles={'rcp26' : 'RCP 2.6',
            'rcp45' : 'RCP 4.5',
            'rcp85' : 'RCP 8.5',
            'rcpall' : 'RCP all'
            }
eval_periods_de={"year"      : "im Jahr",
                 "summer"    : "Sommer",
                 "winter"    : "Winter",
                 "autumn"    : "Herbst",
                 "spring"    : "Frühling",
                 "veg4-10"   : "lange Veg.-periode",
                 "veg4-6"    : "Veg.-periode 1",
                 # "veg7-9"    : "Veg.-periode 2",
                 "veg7-9"    : "Juli - September",
                 "shy"       : "Sommerhalbjahr",
                 "why"       : "Winterrhalbjahr",
                 }
ens_stat_titles={"ensmedian"  : "Ensemble Median",
                 "ensminimum" : "Ensemble Minimum",
                 "ensmaximum"  : "Ensemble Maximum"}
#  -- colormaps ------------------------------------

colors_Blues9    = get_brewer('Blues9',rgb=True)
colors_Reds9     = get_brewer('Reds9',rgb=True)
colors_Greens9   = get_brewer('Greens9',rgb=True)
whitewhite     = [(1.0,1.0,1.0),(1.0,1.0,1.0)]
white          = [(1.0,1.0,1.0)]

colors_PuBuGn9   = get_brewer('PuBuGn9'   ,rgb=True)
colors_YlOrRd9   = get_brewer('YlOrRd9'   ,rgb=True)
colors_PuRd9     = get_brewer('PuRd9'     ,rgb=True)
colors_PuBu9     = get_brewer('PuBu9'     ,rgb=True)
colors_Spectral11= get_brewer('Spectral11',rgb=True)



colors_1 = get_brewer('PuRd9',rgb=True)[3:6][::-1]
colors_2 = get_brewer('Spectral11',rgb=True)[:8:][::-1]
colors_3 = get_brewer('Blues9',rgb= True)[::2]
colors_abs_values = colors_Blues9[::2] + colors_Spectral11[:8:][::-1] + colors_PuRd9[3:6][::-1]

colors_recharge_bgr=["#fb8144","#ffb976" ,"#ffd57f","#fff157","#bbd67a",
                     "#8eca94", "#78cbbe","#55bac8","#32a9b8", "#009eab"  ]


colors_precip    = get_brewer('WhiteBlueGreenYellowRed',rgb=True)[45:-90:][::-1]

colors_drought1    = ["#8fb935", "#abd15c", "#c9e888", "#e8b888", "#d1985c",
                      "#b97a35", "#a25f15", "#ffb9b9", "#e88888", "#b93535"]
colors_drought2    = ['#ffffff','#f7fbff','#deebf7','#c6dbef','#9ecae1',
                      '#6baed6','#4292c6','#2171b5','#08519c','#08306b']

colors_drought1    = ["#005a32", "#238443", "#8fb935", "#abd15c", "#c9e888",
                      "#d1985c", "#a25f15", "#ffb9b9", "#e88888", "#b93535"]
colors_drought1p1    = [ "#ffb9b9", "#e88888", "#b93535"]
colors_4 = get_brewer('Greens9',rgb= True)
colors_5 = get_brewer('BrBG11',rgb= True)[:5:]
colors_5 = get_brewer('Reds9',rgb= True)[:6:]
colors_drought_rel_change = colors_drought2[::-1] + colors_drought1
colors_drought_rel_change = colors_4[::-1] + whitewhite + colors_5 + colors_drought1p1
colors_drought_rel_change = ["#1e3338", "#225979", "#10839e", "#00a8b1", "#80d4bf",
 "#007837", "#35b63f", "#80cc28", "#d1edb0", "#ffffff",
 "#ffffff", "#f1e37e", "#fbc25c", "#c68c5a", "#896042",
 "#502e24", "#f9a6b7", "#f4698c", "#c23962", "#8f113d"]
colors_drought_rel_change = ["#1e3338", "#225979", "#10839e", "#00a8b1", "#80d4bf",
 "#007837", "#35b63f", "#80cc28", "#d1edb0", "#ffffff",
 "#ffffff", "#f1e37e", "#fbc25c", "#c68c5a", "#896042",
 "#502e24",  "#8f113d", "#c23962", "#f4698c", "#f9a6b7"]
colors_drought_rel_change = [
 "#007837", "#35b63f", "#80cc28", "#d1edb0","#1e3338", "#225979", "#10839e", "#00a8b1", "#80d4bf",
  "#ffffff","#ffffff", "#f1e37e", "#fbc25c", "#c68c5a", "#896042",
 "#502e24",  "#8f113d", "#c23962", "#f4698c", "#f9a6b7"]
colors_drought_rel_change = [
  "#d1edb0", "#80cc28", "#35b63f","#007837",
    "#1e3338", "#225979", "#10839e", "#00a8b1", "#80d4bf","#bde5db",
"#f1ecc6", "#f1e37e", "#fbc25c", "#c68c5a", "#896042",
 "#502e24",  "#8f113d", "#c23962", "#f4698c", "#f9a6b7"]
# colors_drought_rel_change = ["#1e3338", "#225979", "#10839e", "#00a8b1", "#80d4bf",
#  "#007837", "#35b63f", "#80cc28", "#d1edb0", "#ffffff",
#  "#ffffff", "#ffffc8", "#feee2c", "#ffd500", "#896042",
#  "#502e24",  "#8f113d", "#c23962", "#f4698c", "#f9a6b7"]

# --------------------------------------------------
#  -- INDICATOR SETTINGS ---------------------------
# --------------------------------------------------

if language == "German":
    var_type_name=var_type_longnames_de
    indicator_name=indicator_longnames_de[indicator]
    eval_period_name=eval_periods_de[eval_period]
elif language == "English":
    var_type_name=var_type_longnames_en
    indicator_name=indicator_longnames_en[indicator]
    eval_period_name=eval_period
#  -- relative change settings ---------------------

# if var_type == 'rel_change':
colorbarlabel_rel_change  = indicator_name +' ' + eval_period_name  + ',  \n'+ var_type_name['rel_change']
if indicator == "n_heatdays":
    colors_rel_change              = colors_Blues9[::-1] + whitewhite + colors_Reds9
    levels_rel_change            = np.arange(-100,110,10)
if indicator == "n_summerdays":
    colors_rel_change              = colors_Blues9[::-1] + whitewhite + colors_Reds9
    levels_rel_change            = np.arange(-100,110,10)
if indicator == "n_consec_heatdays":
    colors_rel_change              = colors_Blues9[::-1] + whitewhite + colors_Reds9
    levels_rel_change            = np.arange(-100,110,10)
if indicator == "n_consec_summerdays":
    colors_rel_change              = colors_Blues9[::-1] + whitewhite + colors_Reds9
    levels_rel_change            = np.arange(-100,110,10)
if indicator == "n_consec_droughtdays":

    colors_rel_change              = colors_Blues9[::-1] + whitewhite + colors_Reds9
    levels_rel_change            = np.arange(-100,110,10)
if indicator == "n_droughtdays_0_30cm":

    colors_rel_change              = colors_Greens9[::-1] + whitewhite + colors_Reds9
    colors_rel_change              = colors_drought_rel_change
    levels_rel_change            = np.arange(-100,110,10)
    # colors_rel_change              = colors_drought1
    # levels_rel_change            = np.arange(-100,110,20)
if indicator == "tavg_mean":
    colors_rel_change              = colors_Blues9[::-1] + whitewhite + colors_Reds9
    levels_rel_change            = np.arange(-100,110,10)
if indicator == 'pre_sum':
    colors_rel_change              = colors_Reds9[::-1] + whitewhite + colors_Blues9
    colors_rel_change              = colors_Reds9[1::][::-1] + whitewhite + colors_Blues9[1::]
    levels_rel_change            = np.arange(-30,33,3)
    levels_rel_change            = np.arange(-45,50,5)

if indicator == 'recharge_adjust_sum':
    colors_rel_change              = colors_Reds9[::-1] + whitewhite + colors_Blues9
    levels_rel_change            = np.arange(-100,110,10)
if indicator == 'recharge_adjust_20perc':
    colors_rel_change              = colors_Reds9[::-1] + whitewhite + colors_Blues9
    levels_rel_change            = np.arange(-100,110,10)
if indicator == 'recharge_adjust_20perc_avg':
    colors_rel_change              = colors_Reds9[::-1] + whitewhite + colors_Blues9
    levels_rel_change            = np.arange(-100,110,10)
if indicator == 'recharge_sum':
    colors_rel_change              = colors_Reds9[::-1] + whitewhite + colors_Blues9
    levels_rel_change            = np.arange(-100,110,10)
if indicator == 'recharge_20perc':
    colors_rel_change              = colors_Reds9[::-1] + whitewhite + colors_Blues9
    levels_rel_change            = np.arange(-100,110,10)
if indicator == 'PET_sum':
    colors_rel_change              = colors_Reds9[::-1] + whitewhite + colors_Blues9
    levels_rel_change            = np.arange(-100,110,10)
if indicator == 'aET_sum':
    colors_rel_change              = colors_Reds9[::-1] + whitewhite + colors_Blues9
    levels_rel_change            = np.arange(-100,110,10)
if indicator == 'Qrouted_p10':
    colors_rel_change              = colors_Reds9[2::][::-1] + colors_Blues9[2::]
    levels_rel_change            = np.arange(-15.,15.1,2.5)
if indicator in ["pre_90p", "pre_95p", "pre_99p", "pre_gt20", "pre_gt10"]:
    colors_rel_change              = colors_Reds9[2::][::-1] + colors_Blues9[2::]
    levels_rel_change            = np.arange(-15.,15.1,2.5)
if indicator in ["pre_gt0p1_R90p","pre_gt0p1_R95p","pre_gt0p1_R99p","pre_gt1_R90p","pre_gt1_R95p","pre_gt1_R99p"]:
    colors_rel_change              = colors_Reds9[2::][::-1] + colors_Blues9[2::]
    levels_rel_change            = np.arange(-15.,15.1,2.5)

# colors_rel_change=mpl.colors.ListedColormap(colors_rel_change)

#  -- absolute change settings ---------------------

# if var_type == 'abs_change':
colorbarlabel_abs_change  = indicator_name +' ' + eval_period_name  + ', \n'+ var_type_name['abs_change']
if indicator == "n_heatdays":
    # colors_abs_change              = colors_PuBuGn9[::-1] + whitewhite + colors_YlOrRd9
    # levels_abs_change            = np.arange(-30,33,3)
    colors_abs_change              = white + colors_YlOrRd9
    levels_abs_change            = np.arange(0,33,3)
if indicator == "n_summerdays":
    # colors_abs_change              = colors_PuBuGn9[::-1] + whitewhite + colors_YlOrRd9
    # levels_abs_change            = np.arange(-50,55,5)
    colors_abs_change              = white + colors_YlOrRd9
    levels_abs_change            = np.arange(0,55,5)
if indicator == "n_consec_droughtdays":

    colors_abs_change              = colors_PuBuGn9[::-1] + whitewhite + colors_YlOrRd9
    # levels_abs_change            = np.arange(-50,55,5)
    # colors_abs_change              = white + colors_YlOrRd9
    if eval_period == "veg4-10":
        levels_abs_change            = np.arange(-50,55,5)
    if eval_period == "veg4-6":
        levels_abs_change            = np.arange(-50,55,5)
    if eval_period == "veg7-9":
        levels_abs_change            = np.arange(-50,55,5)
    if eval_period == "year":
        levels_abs_change            = np.arange(-50,55,5)
    if mask_region == "ww_leipzig_ug":
        levels_abs_change =levels_abs_change*0.2
if indicator == "n_droughtdays_0_30cm":

    colors_abs_change              = colors_PuBuGn9[::-1] + whitewhite + colors_YlOrRd9
    # levels_abs_change            = np.arange(-50,55,5)
    # colors_abs_change              = white + colors_YlOrRd9
    if eval_period == "veg4-10":
        levels_abs_change            = np.arange(-50,55,5)
    if eval_period == "veg4-6":
        levels_abs_change            = np.arange(-50,55,5)
    if eval_period == "veg7-9":
        levels_abs_change            = np.arange(-50,55,5)
    if eval_period == "year":
        levels_abs_change            = np.arange(-50,55,5)
    if mask_region == "ww_leipzig_ug":
        levels_abs_change =levels_abs_change*0.2
if indicator == "n_consec_heatdays":
    colors_abs_change              = white + colors_YlOrRd9
    levels_abs_change            = np.arange(0,5.5,0.5)
    levels_abs_change            = np.arange(0,7.6,0.75)
    # levels_abs_change            = np.arange(0,10.5,1)
if indicator == "n_consec_summerdays":
    colors_abs_change              = white + colors_YlOrRd9
    levels_abs_change            = np.arange(0,22,2)
if indicator == 'pre_sum':
    colors_abs_change              = colors_YlOrRd9[::-1] + whitewhite + colors_PuBuGn9
    levels_abs_change            = np.arange(-200,220,20)
    if eval_period != "year":
        levels_abs_change        = levels_abs_change /4
if indicator == 'aET_sum':
    colors_abs_change              = colors_YlOrRd9[::-1] + whitewhite + colors_PuBuGn9
    levels_abs_change            = np.arange(-100,110,10)
    if eval_period != "year":
        levels_abs_change        = levels_abs_change /4
if indicator == 'PET_sum':
    colors_abs_change              = colors_YlOrRd9[::-1] + whitewhite + colors_PuBuGn9
    levels_abs_change            = np.arange(-100,110,10)
    if eval_period != "year":
        levels_abs_change        = levels_abs_change /4
if indicator == 'recharge_adjust_sum':
    colors_abs_change              = colors_YlOrRd9[::-1] + whitewhite + colors_PuBuGn9
    levels_abs_change            = np.arange(-50,55,5)*2
    colors_abs_change              = get_brewer('Blues6',rgb= True)[::-1] + whitewhite + colors_PuBuGn9[::2]
    colors_abs_change              = colors_YlOrRd9[::-1][::2] + whitewhite + colors_PuBuGn9[::2]
    colors_abs_change              = get_brewer('YlOrRd9',rgb= True)[::-1] + get_brewer('PuBuGn9',rgb= True)
    colors_abs_change              = get_brewer('YlOrRd9',rgb= True)[1::][::-1] +whitewhite + get_brewer('PuBuGn9',rgb= True)[1::]
    levels_abs_change            = np.array([-1000,-40,-30,-20,-10,-5,0,5,10,20,30,40,1000])
    levels_abs_change            = np.arange(-90,91,10)

    if eval_period in ["shy", "why"]:
        levels_abs_change        = levels_abs_change /2
        print("seasonal recharge sum")
    elif eval_period != "year":
        levels_abs_change        = levels_abs_change /4
        print("seasonal recharge sum")
if indicator == 'recharge_adjust_20perc':
    colors_abs_change              = colors_YlOrRd9[::-1] + whitewhite + colors_PuBuGn9
    levels_abs_change            = np.arange(-10,11,1)
if indicator == 'recharge_adjust_20perc_avg':
    colors_abs_change              = colors_YlOrRd9[::-1] + whitewhite + colors_PuBuGn9
    levels_abs_change            = np.arange(-25,30,5)
    levels_abs_change            = np.arange(-12.5,15,2.5)
if indicator == 'recharge_sum':
    colors_abs_change              = colors_YlOrRd9[::-1] + whitewhite + colors_PuBuGn9
    levels_abs_change            = np.arange(-30,33,3)
if indicator == 'recharge_20perc':
    colors_abs_change              = colors_YlOrRd9[::-1] + whitewhite + colors_PuBuGn9
    levels_abs_change            = np.arange(-10,11,1)
if indicator == 'tavg_mean':
    colors_abs_change              = colors_Blues9[1:2][::-1] + whitewhite + colors_Reds9 #+colors_PuRd9[6:-1][::-1]
    levels_abs_change            = np.arange(-1,5.1,0.5)
if indicator in ["pre_gt20", "pre_gt10"]:
    colors_abs_change              = colors_YlOrRd9[::-1] + whitewhite + colors_PuBuGn9
    levels_abs_change            = np.arange(-5,5.1,0.5)
if indicator in ["pre_90p", "pre_95p", "pre_99p"]:
    colors_abs_change              = colors_YlOrRd9[::-1] + whitewhite + colors_PuBuGn9
    levels_abs_change            = np.arange(-5,5.1,0.5)
if indicator in ["pre_gt0p1_R90p","pre_gt0p1_R95p","pre_gt0p1_R99p","pre_gt1_R90p","pre_gt1_R95p","pre_gt1_R99p"]:
    colors_abs_change             = colors_YlOrRd9[::-1] + whitewhite + colors_PuBuGn9
    levels_abs_change            = np.arange(-5,5.1,0.5)

# colors_abs_change=mpl.colors.ListedColormap(colors_abs_change)

#  -- vartype absolute values ----------------------

# if var_type == 'abs':
colorbarlabel_abs  = indicator_name +' ' + eval_period_name  + ', \n' + var_type_name['abs'] 
if indicator == "n_heatdays":
    colors_abs              = colors_abs_values
    levels_abs            = np.arange(0,30,2)
if indicator == "n_summerdays":
    colors_abs              = colors_abs_values
    levels_abs            = np.arange(0,74,5)
if indicator == "n_consec_heatdays":
    colors_abs              = colors_abs_values
    levels_abs            = np.arange(0,15,1)
    levels_abs            = np.arange(0,10.6,0.75)
if indicator == "n_consec_summerdays":
    colors_abs              = colors_abs_values
    levels_abs            = np.arange(0,30,2)
if indicator == "n_consec_droughtdays":

    colors_abs              = colors_Spectral11[:8:][::-1] + colors_PuRd9[3:6][::-1]
    # levels_abs_change            = np.arange(-50,55,5)
    # colors_abs_change              = white + colors_YlOrRd9
    if eval_period == "veg4-10":
        levels_abs            = np.arange(25,35,1)
    if eval_period == "veg4-6":
        levels_abs            = np.arange(10,20,1)
    if eval_period == "veg7-9":
        levels_abs            = np.arange(10,20,1)
    if eval_period == "year":
        levels_abs            = np.arange(45,55,1)
if indicator == "n_droughtdays_0_30cm":

    colors_abs              = colors_Spectral11[:8:][::-1] + colors_PuRd9[3:6][::-1]
    # levels_abs_change            = np.arange(-50,55,5)
    # colors_abs_change              = white + colors_YlOrRd9
    if var_type == "abs-abs_change" or var_type == "abs-rel_change":
        if eval_period == "veg4-10":
            levels_abs            = np.arange(33.5,38.6,0.5)
        if eval_period == "veg4-6":
            levels_abs            = np.arange(13.5,18.6,0.5)
        if eval_period == "veg7-9":
            levels_abs            = np.arange(13.5,18.6,0.5)
        if eval_period == "year":
            levels_abs            = np.arange(58,69,1)
    else:
        if eval_period == "veg4-10":
            levels_abs            = np.arange(33.5,93.6,6)
        if eval_period == "veg4-6":
            levels_abs            = np.arange(13.5,93.6,8)
        if eval_period == "veg7-9":
            levels_abs            = np.arange(0,54,5)
        if eval_period == "year":
            levels_abs            = np.arange(58,119,6)
if indicator == 'pre_sum':
    colors_abs              = colors_precip
    if eval_period == "year":
        levels_abs            = np.arange(400,2000,100)
    else:
        levels_abs            = np.arange(40,400,20)
if indicator == 'aET_sum':
    colors_abs              = colors_precip
    if eval_period == "year":
        levels_abs            = np.arange(300,760,30)
    else:
        levels_abs            = np.arange(40,400,20)
if indicator == 'PET_sum':
    colors_abs              = colors_precip
    if eval_period == "year":
        levels_abs            = np.arange(700,1010,20)
    else:
        levels_abs            = np.arange(40,400,20)

if indicator == 'recharge_adjust_sum':
    colors_abs              = colors_recharge_bgr
    if eval_period == "year":
        levels_abs            = np.array([0,25,50,75,100,150,200,300,350,500,10000])
    elif eval_period in ["shy", "why"]:
        levels_abs            = np.array([0,25,50,75,100,150,200,300,350,500,10000])
    else:
        levels_abs            = np.array([0,5,10,25,50,75,100,150,200,300,10000])
if indicator == 'recharge_sum':
    colors_abs              = colors_recharge_bgr
    levels_abs            = np.arange(0,275,25)
if indicator == 'recharge_20perc':
    colors_abs              = colors_abs_values
    levels_abs            = np.arange(1,12,1)
if indicator == 'recharge_adjust_20perc':
    colors_abs              = colors_abs_values
    levels_abs            = np.arange(1,12,1)
if indicator == 'recharge_adjust_20perc_avg':
    colors_abs              = colors_recharge_bgr
    levels_abs            = np.array([0,5,10,25,50,100,150,200,300,500,10000]) *0.2
    levels_abs            = np.array([0,5,10,25,50,100,150,200,300,500,10000]) *0.2
if indicator == 'tavg_mean':
    colors_abs              = colors_abs_values
    levels_abs            = np.arange(-3,30,3)
    colors_tavg           = get_brewer('WhiteBlueGreenYellowRed',rgb=True)[5::] 
    # colors_abs              = colors_abs_values
    colors_abs              = colors_tavg
    # levels_abs            = np.arange(-3,30,3)
    levels_abs            = np.arange(-3,23,1)
if indicator in ["pre_gt20", "pre_gt10"]:
    colors_abs              = colors_PuBu9
    levels_abs            = np.arange(0,50,5)
if indicator in ["pre_90p", "pre_95p", "pre_99p"]:
    colors_abs              = colors_PuBu9
    levels_abs            = np.arange(0,50,5)
if indicator in ["pre_gt0p1_R90p","pre_gt0p1_R95p","pre_gt0p1_R99p","pre_gt1_R90p","pre_gt1_R95p","pre_gt1_R99p"]:
    colors_abs              = colors_PuBu9
    levels_abs            = np.arange(0,50,5)
# colors_abs=mpl.colors.ListedColormap(colors_abs)
    # if ncvarname == 'tmax':
    #     colorbarlabel = 'Temperature [°C]'
    #     levels        = np.arange(12,34.5,2)
    #     levels        = np.arange(10,42.5,2)


# create colormap
if var_type == 'abs':
    colorbarlabel=colorbarlabel_abs
elif var_type == 'abs_change':
    colorbarlabel=colorbarlabel_abs_change
elif var_type == 'rel_change':
    colorbarlabel=colorbarlabel_rel_change
elif var_type =="abs-rel_change":  #
    colorbarlabel=colorbarlabel_rel_change
elif var_type =="abs-abs_change":  #
    colorbarlabel=colorbarlabel_abs_change

