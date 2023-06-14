#! /usr/bin/env python
# -*- coding: utf-8 -*-



from sqlite3 import Row
import numpy as np                       # array manipulation
import ufz
import matplotlib as mpl
from matplotlib.patches import Rectangle
import datetime
from matplotlib.dates import YearLocator, DateFormatter, MonthLocator, YearLocator
from cftime import num2date, date2num
import pandas as pd
import glob 



# -------------------------------------------------------------------------
# Command line arguments
#
#infile  = '/data/klimabuero/GDM/data/smi/SMI_L02.nc'
#infile   = '/data/klimabuero/DWD/drought_monitor/smi_output/mSMI.nc'
pdffile  = ''
pngbase  = ''
#pngbase  = '/data/klimabuero/GDM/tmp/area_under drought'
import optparse
parser  = optparse.OptionParser(usage='%prog [options]',
                               description="Plotting of SMI for drought monitor.")
parser.add_option('-i', '--infile', action='store', dest='infile', type='string',
                  default=infile, metavar='File',
                  help='Name of NetCDF input file (no default).')
parser.add_option('-p', '--pdffile', action='store', dest='pdffile', type='string',
                  default=pdffile, metavar='File',
                  help='Name of pdf output file (default: open X-window).')
parser.add_option('-g', '--pngbase', action='store',
                    default=pngbase, dest='pngbase', metavar='pngbase',
                    help='Name basis for png output files (default: open screen window).')
(opts, args) = parser.parse_args()

infile   = opts.infile
pdffile  = opts.pdffile
pngbase  = opts.pngbase
del parser, opts, args

if (pdffile != '') & (pngbase != ''):
    raise ValueError('PDF and PNG are mutually exclusive. Only either -p or -g possible.')

# -------------------------------------------------------------------------

# CONFIGURATIONS 
var        = 'SMI'

# -------------------------------------------------------------------------
# Customize plots
#
if (pdffile == ''):
    if (pngbase == ''):
        outtype = 'x'
    else:
        outtype = 'png'
else:
    outtype = 'pdf'

remove_warning_class = True # if set True only the drought classes < 0.2 are shown

# Plot - paper_plots, but also all if not otherwise defined
nrow       = 1           # # of rows per figure
ncol       = 1           # # of columns per figure
hspace     = 0.12        # x-space between plots
wspace     = 0.02        # y-space between plots
textsize   = 20          # Standard text size
dt         = 4           # # of hours between tick marks on plots
dxabc      = 0.90        # % shift from left y-axis of a,b,c,... labels
dyabc      = 0.90        # % shift from lower x-axis of a,b,c,... labels
dyabcdown  = 0.05        # y-shift if abc in lower right corner
lwidth     = 0.5         # linewidth
elwidth    = 1.0         # errorbar line width
alwidth    = 1.0         # axis line width
msize      = 10.         # marker size
mwidth     = 4           # marker edge width
bxwidth    = 0.85        # boxlplot width
# color: 'b'|'g'|'r'|'c'|'m'|'y'|'k'|'w'
#        'blue'|'green'|'red'|'cyan'|'magenta'|'yellow'|'black'|'white'
#        hex string '#eeefff' | RGB tuple (1,0.5,1) | html names 'burlywod', 'chartreuse', ...
#        grayscale intensity, e.g. '0.7', 'k'='0.0'
mcol1      = '#67A9CF'   # color of second markers
mcol2      = '#A1D99B'   # color of third markers
mcol3      = '#EF8A62'         # primary line colour
mcol4      = 'r'
lcol2      = '0.5'       # color of second lines
lcol3      = '0.0'       # color of third lines

llxbbox    = 0.5        # x-anchor legend bounding box
llybbox    = 0.87        # y-anchor legend bounding box
llrspace   = 0.02        # spacing between rows in legend
llcspace   = 1.0         # spacing between columns in legend
llhtextpad = 0.2         # the pad between the legend handle and text
llhlength  = 0.9         # the length of the legend handles
frameon    = True        # if True, draw a frame around the legend. If None, use rc
llxbbox2   = 0.60        # Tight bounding of symbol and text (w/o lines)
llhtextpad2= 0.          #                   "
llhlength2 = 1.0         #                   "

# PNG
dpi         = 72 #300
cdo selyear,${start_range}/${end_range} ./data/${bling}_1951_202306_daily.nc ./tmp/${bling}_${start_range}_${end_range}_daily.nctransparent = False
bbox_inches = 'tight'
pad_inches  = 0.1
#
if (outtype == 'pdf'):
    mpl.use('PDF') # set directly after import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    # Customize: http://matplotlib.sourceforge.net/users/customizing.html
    mpl.rc('ps', papersize='a4', usedistiller='xpdf') # ps2pdf
elif (outtype == 'png'):
    #mpl.use('Agg') # set directly after import matplotlib
    import matplotlib.pyplot as plt
    #mpl.rc('text.latex', str=True)
    #mpl.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'
    #plt.rcParams['text.usetex'] = True


else:
    import matplotlib.pyplot as plt
#
# mpl.rc('figure',     figsize=( 8, 5)) # for AGU 2012 Poster
# one column of 2 column paper - for paper half of the size because of 2 columns
#mpl.rc('figure',     figsize=( 8.27/2., 8.27/2./1.618)) # half side A4potrait, golden ratio
#mpl.rc('figure',     figsize=( 8.27, 11.69)) # a4 portrait
#mpl.rc('figure',     figsize=( 9, 11.69)) # a4 portrait
mpl.rc('figure',     figsize=(11.69,  6)) # a4 landscape
mpl.rc('font',       **{'family':'serif','serif':['times']})
mpl.rc('font',       size=textsize)
mpl.rc('legend',     fontsize=textsize)
mpl.rc('lines',      linewidth=lwidth, color='black')
mpl.rc('axes',       linewidth=alwidth, labelcolor='black')
mpl.rc('path',       simplify=False) # do not remove
#mpl.rc('text',       usetex=False)
#plt.rcParams['text.usetex'] = True

##############################################################################################
if (outtype == 'pdf'):
    print('Plot PDF ', pdffile)
    pdf_pages = PdfPages(pdffile)
elif (outtype == 'png'):
    print(('Plot PNG ', pngbase))
else:
    print('Plot X')

figsize = mpl.rcParams['figure.figsize']
ifig = 0

# data PROCESSING #############################################################
smi       = ufz.readnetcdf(infile, var=var)
# times

timeunit  = ufz.readnetcdf(infile, var='time', attributes=True)['units']
times     = ufz.readnetcdf(infile, var='time')
datetimes=num2date(times,units=timeunit,only_use_cftime_datetimes=False)
#print(datetimes)
timeunit  = ufz.readnetcdf(infile, var='time', attributes=True)['units'].split()[0]
if (timeunit == 'months'):
    years = np.array([d.year for d in datetimes])
    months = np.array([d.month for d in datetimes])
elif (timeunit == 'days'):
    years = np.array([d.year for d in datetimes])
    months = np.array([d.month for d in datetimes])
    days = np.array([d.day for d in datetimes])
else:
    print('***ERROR: time unit fron NetCDF not known!')
    stop

datetimes = [datetime.datetime(years[i],months[i],days[i]) for i in np.arange(times.shape[0])]
# dates       = [datetime.datetime(int( year1[(julianday1>=minjulday) & (julianday1<=maxjulday)][i]),
#                                  int(month1[(julianday1>=minjulday) & (julianday1<=maxjulday)][i]),
#                                  int(  day1[(julianday1>=minjulday) & (julianday1<=maxjulday)][i])) for i in np.arange(len(year1[(julianday1>=minjulday) & (julianday1<=maxjulday)]))]

    
# MAPPLOT #########################################
# bound and labeling for colorbar
if remove_warning_class:
    bounds     = np.array([0.20, 0.10, 0.05, 0.02])
    colors     = ['#FCD37F','#FFAA00','#E60000','#730000'] # usdm 
    txt_format = '%2d %6.2f %6.2f %6.2f %6.2f %6.2f %6.4f'
else:
    bounds     = np.array([0.30, 0.20, 0.10, 0.05, 0.02])
    colors     = ['#FFFF00', '#FCD37F','#FFAA00','#E60000','#730000'] # usdm 
    txt_format = '%4d %2d %6.2f %6.2f %6.2f %6.2f %6.2f %6.4f'
fig        = plt.figure(ifig)
ax         = fig.add_axes(ufz.position(nrow,ncol, 1, bottom=0.08, top=0.97, left=0.08, right=0.98))

area_per_class  = np.ones((smi.shape[0],len(bounds)))

for iclass in range(len(bounds)):
    
    # drought_area = number of cells lower/equal threshold devided by total number of valid cells
    drought_area   = np.ma.sum(smi<=bounds[iclass], axis=(1,2)).astype(np.float) / np.float(np.sum(~smi[0,:,:].mask))
    area_per_class[:,iclass] = drought_area
    print('drought class:', iclass, 'current area under drought: ', drought_area[-1])
    lp           = ax.fill_between(datetimes, 0, drought_area * 100, color=colors[iclass])


        
    ax.xaxis.set_major_formatter( DateFormatter('%Y') )    # 2018
    ax.tick_params(axis='x',which='major',length=5)
    ax.tick_params(axis='x',which='minor',length=3) # set minor ticks to length of the major ticks
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=15)
    # axis labels 

    #ax.set_ylabel(r'Fl\"ache unter D\"uerre in Deutschland [\%]')
    #ax.set_xlabel("")
    ax.set_ylabel('Fläche unter Düerre in Deutschland [%]', fontsize=14)
    ax.set_ylim(0,100)
    #ax.margins(x=0)


if (outtype == 'pdf'):
    pdf_pages.savefig(fig)
    plt.close()
elif (outtype == 'png'):
    figname =  pngbase
    #fig.savefig(figname, dpi=300, transparent=transparent, bbox_inches=bbox_inches, pad_inches=pad_inches)
    #plt.show()
    plt.close(fig)
else:
    print("not plotting, only table generation")
    plt.close(fig)



# if (outtype == 'pdf'):
#     pdf_pages.close()
# elif (outtype == 'png'):
#     pass

# output = np.array(np.append (years[:,np.newaxis], months[:,np.newaxis], axis=1))
# output = np.append(output, area_per_class*100, axis=1)


# drought_intensity   = np.ma.sum(np.ma.where(smi<=0.2, 0.2 - smi, 0), 
#                                 axis=(1,2)).astype(np.float) / np.float(np.sum(~smi[0,:,:].mask))

# output = np.column_stack([output,np.array(drought_intensity)])
# print(output.shape)
# def print_file(filename,array):
#     f = open(filename, 'w')
#     header = 'year month ' + ' '.join(ufz.astr(bounds, prec=2)) + ' droughtintensity \n'
#     f.write(header)
#     np.savetxt(f, array, fmt=txt_format)
#     f.close()

# fout   = '/'.join(pdffile.split('/')[:-1]) + './area_under_drought.txt'
# print_file(fout,output)

# # sort values by drought class:
# output_sort = pd.DataFrame(output[:,:],columns=['year','month']+ 
# ['{:}'.format(b) for b in bounds]+ ['drought intensity']).sort_values(by="0.02",ascending=False) 
# fout   = '/'.join(pdffile.split('/')[:-1]) + './area_under_drought_sort0p02.txt'
# print_file(fout,output_sort)
