#! /usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import ufz
from ufz import fread,readnc, position, get_brewer, abc2plot, astr
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr
import geopandas as gpd
import datetime
#import palettable as pb
from matplotlib import colors
from matplotlib.colors import ListedColormap, BoundaryNorm
import optparse






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






indicator= "n_heatdays"




if indicator == 'pre_sum':
    colors_rel_change    = colors_Reds9[::-1] + whitewhite + colors_Blues9
    levels      = np.arange(400,2000,100)

if indicator == 'recharge_adjust_sum':
    colors_abs              = colors_recharge_bgr
    levels            = np.array([0,25,50,75,100,150,200,300,350,500,10000])

if indicator == "n_heatdays":
    colors_abs  = colors_abs_values
    levels            = np.arange(0,30,2)

    
cmap = mpl.colors.ListedColormap(colors_abs)
for i in range(cmap.N):
    rgba = cmap(i)
    # rgb2hex accepts rgb or rgba
    print(mpl.colors.rgb2hex(rgba))


    
fig, ax = plt.subplots(figsize=(6, 1))
fig.subplots_adjust(bottom=0.5)

norm = mpl.colors.BoundaryNorm(levels, cmap.N)    #, extend='both'
print(norm)
fig.colorbar(mpl.cm.ScalarMappable(norm=norm,cmap=cmap),
             cax=ax, orientation='horizontal', label='Some Units')
plt.show()



