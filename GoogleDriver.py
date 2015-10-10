# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 20:51:35 2015

@author: Matthew
"""

from __future__ import print_function

# Imports Bokeh
from bokeh.embed import autoload_static, components, notebook_div
from bokeh.io import vplot
from bokeh.models.glyphs import Circle, Patches
from bokeh.models import (GMapPlot, Range1d, ColumnDataSource, PanTool, \
                          WheelZoomTool, BoxSelectTool, BoxSelectionOverlay, \
                          ResetTool, GMapOptions)
from bokeh.plotting import output_file, save
from bokeh.resources import CDN

# Imports other inhouse functions
import GunData as gdt
import LawData as ldt


""" plotLaw --------------------------------------------------------------------
    Goal:   Creates a plot where law intensity is shaded on each state & each
            county recieves a dot where the darker colors means more shootings.
            
    Input:  (1) A source dict for law info per state, (2) a source dict for
            shooting quantity per county, & (3) a title for the plot
    Output: A Bokeh Plot
-----------------------------------------------------------------------------"""
def plotLaw(sourceLaw, sourceSh, title):
    # Creates Google Maps Plot
    x_range = Range1d()
    y_range = Range1d()
    map_options = GMapOptions(lat=39.50, lng=-98.35, map_type="roadmap", zoom=4)
    plot = GMapPlot(x_range=x_range, y_range=y_range, map_options=map_options, \
                plot_width=800, plot_height=600, title=title)
    
    # Sets Law Shading Data for each State 
    patch = Patches(xs="lng", ys="lat", fill_alpha=0.5, fill_color="clr")
    plot.add_glyph(sourceLaw, patch)
        
    # Create Circles on Plot
    circle = Circle(x="lng", y="lat", size=15, fill_color="clr", \
                    line_color="black")
    plot.add_glyph(sourceSh, circle)

    # Create Tools
    pan = PanTool()
    wheel_zoom = WheelZoomTool()
    box_select = BoxSelectTool()
    reset = ResetTool()
    plot.add_tools(pan, wheel_zoom, box_select, reset)
    overlay = BoxSelectionOverlay(tool=box_select)
    plot.add_layout(overlay)

    return plot


""" main: Sets colors for the quantity of Raw shootings per county ----------"""
"""
# Creates Output File
output_file("RawPopulation.html", title="Raw Population Shootings")
plots = []

# Loads DataFrame from DownloadGoogle with City, Shootings, Lat, & Long.
inFile = '/Users/Matthew/Github/Crime2015/MyData/ShootingData2.csv'
shQty = pd.read_csv(inFile, index_col='City')

# Groups all entries by counties
shQty = shQty.groupby(['Cty']).sum()

# Set Color Options
attkColors = {5:'#CCE0FF', 10:'#99C2FF', 20:'#66A3FF', 30:'#3385FF', \
              40:'#0066FF', 50:'#0052CC', 60:'#003D99', 70:'#002966', \
              85:'#001433', 100:'#000A1A', 300:'#000000'}
clrs = []

# Loops between county to set colors
for location in shQty.index:
    shootings = shQty.loc[location, 'Shooting']
    color = '#CCE0FF'
    for maximum in sorted(attkColors):
        if shootings <= maximum:
            clrs.append(color)
            break
        else:
            color = attkColors[maximum]

# Zips Data for Shootings per County 
sourceRaw = ColumnDataSource(data=dict(lat=shQty.Lat, lng=shQty.Lng, clr=clrs))
"""


""" main: Sets colors for the quantity of ratio shootings per State ---------"""
# Creates Output File
output_file("RatioPopulation.html", title="Ratio Population Shootings")
plots = []

# Loads Injuries & Shootings per State
stateInjuries, stateShootings = gdt.loadGun(False)

# Loads State Midpoint Coordinates
midpoint = ldt.loadMid()
lats = []
lngs = []

# Set Color Options
attkColors = {2:'#CCE0FF', 4:'#99C2FF', 8:'#66A3FF', 12:'#3385FF', \
              16:'#0066FF', 20:'#0052CC', 30:'#003D99', 40:'#002966', \
              50:'#001433', 75:'#000A1A', 100:'#000000'}
clrs = []

# Loops between county to set colors
for location in stateShootings.keys():
    # Calculates Colors
    shootings = stateShootings[location]/3.21  #321000000 Population
    color = '#CCE0FF'
    for maximum in sorted(attkColors):
        if shootings <= maximum:
            break
        else:
            color = attkColors[maximum]
    
    # Determines Midpoint
    try:
        lats.append(midpoint[location]['y'])
        lngs.append(midpoint[location]['x'])
        clrs.append(color)
    except:
        print(location)

# Zips Data for Shootings per County 
sourceRaw = ColumnDataSource(data=dict(lat=lats, lng=lngs, clr=clrs))


""" main: Downloads all Laws & Coordinate Data ------------------------------"""
# Gets State Coordinates
stateBorder = gdt.loadBorder()
state = [item for item in sorted(stateBorder)]
lats = [stateBorder[item]['lat'] for item in sorted(stateBorder)]
lngs = [stateBorder[item]['lng'] for item in sorted(stateBorder)]

# Downloads Legal Data
laws = ldt.loadLaw()
laws = laws.sort_index()
laws = laws.drop('DC')


""" main: Plots for each type of law ----------------------------------------"""
# Plots CarryHG Laws
CarryHGLaw = laws['CarryHG'].tolist()
sourceLaw = ColumnDataSource(data=dict(lat=lats, lng=lngs, clr=CarryHGLaw))
CarryHG = plotLaw(sourceLaw, sourceRaw, 'Carry Handgun Laws vs. Shootings')

# Plots CarryLG Laws
CarryLGLaw = laws['CarryLG'].tolist()
sourceLaw = ColumnDataSource(data=dict(lat=lats, lng=lngs, clr=CarryLGLaw))
CarryLG = plotLaw(sourceLaw, sourceRaw, 'Carry Longgun Laws vs. Shootings')

# Plots PurchaseHG Laws
PurchaseHGLaw = laws['PurchaseHG'].tolist()
sourceLaw = ColumnDataSource(data=dict(lat=lats, lng=lngs, clr=PurchaseHGLaw))
PurchaseHG = plotLaw(sourceLaw, sourceRaw, 'Purchase Handgun Laws vs. Shootings')

# Plots PurchaseLG Laws
PurchaseLGLaw = laws['PurchaseLG'].tolist()
sourceLaw = ColumnDataSource(data=dict(lat=lats, lng=lngs, clr=PurchaseLGLaw))
PurchaseLG = plotLaw(sourceLaw, sourceRaw, 'Purchase Longgun Laws vs. Shootings')

# Plots ShootFirst Laws
ShootFirstLaw = laws['ShootFirst'].tolist()
sourceLaw = ColumnDataSource(data=dict(lat=lats, lng=lngs, clr=ShootFirstLaw))
ShootFirst = plotLaw(sourceLaw, sourceRaw, 'Shoot First Laws vs. Shootings')

# Plots GunShow Laws
GunShowLaw = laws['GunShow'].tolist()
sourceLaw = ColumnDataSource(data=dict(lat=lats, lng=lngs, clr=GunShowLaw))
GunShow = plotLaw(sourceLaw, sourceRaw, 'Gun Show Laws vs. Shootings')

# Plots Safety Laws
SafetyLaw = laws['Safety'].tolist()
sourceLaw = ColumnDataSource(data=dict(lat=lats, lng=lngs, clr=SafetyLaw))
Safety = plotLaw(sourceLaw, sourceRaw, 'Safety Laws vs. Shootings')

# Plots Restrict Laws
RestrictLaw = laws['Restrict'].tolist()
sourceLaw = ColumnDataSource(data=dict(lat=lats, lng=lngs, clr=RestrictLaw))
Restrict = plotLaw(sourceLaw, sourceRaw, 'Gun Restriction Laws vs. Shootings')

# Saves Plot
listPlots = vplot(CarryHG, CarryLG, PurchaseHG, PurchaseLG, ShootFirst, GunShow,
                  Safety, Restrict)
save(listPlots)

div = notebook_div(Restrict)
