# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 20:51:35 2015

@author: Matthew
"""

from __future__ import print_function

# Imports Bokeh
from bokeh.io import vplot
from bokeh.models.glyphs import Circle, Patches
from bokeh.models import (GMapPlot, Range1d, ColumnDataSource, PanTool, \
                          WheelZoomTool, BoxSelectTool, BoxSelectionOverlay, \
                          ResetTool, GMapOptions, HoverTool)
from bokeh.plotting import output_file, save

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
    
    # Sets Hover Tools
    hover = HoverTool(tooltips=[("State", "@name"), ("Shootings", "@shts"),
                                ("Injuries", "@injs")])

    # Sets Law Shading Data for each State 
    patch = Patches(xs="lng", ys="lat", fill_alpha=0.5, fill_color="clr")
    plot.add_glyph(sourceLaw, patch)
        
    # Create Injuries Ratio Circles on Plot
    circle = Circle(x="lng", y="lat", size=15, fill_color="clr", \
                    line_color="black")
    plot.add_glyph(sourceSh, circle)

    # Create Tools
    pan = PanTool()
    wheel_zoom = WheelZoomTool()
    box_select = BoxSelectTool()
    reset = ResetTool()
    plot.add_tools(pan, wheel_zoom, box_select, reset, hover)
    overlay = BoxSelectionOverlay(tool=box_select)
    plot.add_layout(overlay)

    return plot


""" main: Downloads all Laws & Coordinate Data ------------------------------"""
# Gets State Coordinates
stateBorder = gdt.loadBorder()
name = [item for item in sorted(stateBorder)]
lats = [stateBorder[item]['lat'] for item in sorted(stateBorder)]
lngs = [stateBorder[item]['lng'] for item in sorted(stateBorder)]

# Downloads Legal Data
laws = ldt.loadLaw()
laws = laws.sort_index()
laws = laws.drop('DC')


""" main: Allocates Lists for Data, Output Files, & Color Choices -----------"""
# Creates Output File
output_file("RatioPopulation.html", title="Ratio Population Shootings")
plots = []

# Loads Injuries & Shootings per State
stateInjuries, stateShootings = gdt.loadGun(False)

# Loads State Populations
statePop = gdt.loadPop()

# Loads State Midpoint Coordinates & Name
midpoint = ldt.loadMid()
name2 = []
lats2 = []
lngs2 = []

# Allocates 2 lists for state shootings & injured each, first w. HI & AK
shts = []
shts2 = []
injs = []
injs2 = []

# Set Color Options & Allocates Color List
attkColors = {3:'#CCE0FF', 6:'#99C2FF', 9:'#66A3FF', 12:'#3385FF', \
              15:'#0066FF', 19:'#0052CC', 23:'#003D99', 27:'#002966', \
              31:'#001433', 75:'#000A1A', 150:'#000000'}
#attkColors = {10:'#CCE0FF', 15:'#99C2FF', 20:'#66A3FF', 25:'#3385FF', \
#              30:'#0066FF', 40:'#0052CC', 50:'#003D99', 60:'#002966', \
#              80:'#001433', 100:'#000A1A', 150:'#000000'}
clrs2 = []


""" main: Sets colors for the quantity of ratio shootings per State ---------"""
# Loops between each State, even if there are no shootings, to set colors
for location in name:
    # Calculates Ratio per State
    try:
        injured = stateInjuries[location]
        shootings = stateShootings[location]
        ratio = injured/(statePop[location]/1000000)
        #shootings = stateInjuries[location]/3.21 #321000000 US Population
    except:
        injured = 0.0
        shootings = 0.0
        ratio = 0.0
        color = 'White'
    
    # Calculates Colors for states with a ratio
    if ratio is not 0.0:
        for minimum in sorted(attkColors):
            if ratio <= minimum:
                break
            else:
                color = attkColors[minimum]
    
    # Adds the shooting values to a list for the 'state law shades' in the plot
    shts.append(str(shootings))
    injs.append(str(injured))
    
    # Adds all values to lists to create the 'shooting circles' in the plot
    try:
        lats2.append(midpoint[location]['y'])
        lngs2.append(midpoint[location]['x'])
        clrs2.append(color)
        name2.append(location)
        shts2.append(str(shootings))
        injs2.append(str(injured))
    except:
        print(location)

# Zips Data for Shootings per State 
sourceRaw = ColumnDataSource(data=dict(name=name2, shts=shts2, injs=injs2, 
                                       lat=lats2, lng=lngs2, clr=clrs2))


""" main: Plots for each type of law ----------------------------------------"""
# Plots CarryHG Laws
CarryHGLaw = laws['CarryHG'].tolist()
sourceLaw = ColumnDataSource(data=dict(name=name, shts=shts, injs=injs, 
                                       lat=lats, lng=lngs, clr=CarryHGLaw))
CarryHG = plotLaw(sourceLaw, sourceRaw, 'Carry Handgun Laws vs. Shootings')

# Plots CarryLG Laws
CarryLGLaw = laws['CarryLG'].tolist()
sourceLaw = ColumnDataSource(data=dict(name=name, shts=shts, injs=injs, 
                                       lat=lats, lng=lngs, clr=CarryLGLaw))
CarryLG = plotLaw(sourceLaw, sourceRaw, 'Carry Longgun Laws vs. Shootings')

# Plots PurchaseHG Laws
PurchaseHGLaw = laws['PurchaseHG'].tolist()
sourceLaw = ColumnDataSource(data=dict(name=name, shts=shts, injs=injs, 
                                       lat=lats, lng=lngs, clr=PurchaseHGLaw))
PurchHG = plotLaw(sourceLaw, sourceRaw, 'Purchase Handgun Laws vs. Shootings')

# Plots PurchaseLG Laws
PurchaseLGLaw = laws['PurchaseLG'].tolist()
sourceLaw = ColumnDataSource(data=dict(name=name, shts=shts, injs=injs, 
                                       lat=lats, lng=lngs, clr=PurchaseLGLaw))
PurchLG = plotLaw(sourceLaw, sourceRaw, 'Purchase Longgun Laws vs. Shootings')

# Plots ShootFirst Laws
ShootFirstLaw = laws['ShootFirst'].tolist()
sourceLaw = ColumnDataSource(data=dict(name=name, shts=shts, injs=injs, 
                                       lat=lats, lng=lngs, clr=ShootFirstLaw))
ShootFirst = plotLaw(sourceLaw, sourceRaw, 'Shoot First Laws vs. Shootings')

# Plots GunShow Laws
GunShowLaw = laws['GunShow'].tolist()
sourceLaw = ColumnDataSource(data=dict(name=name, shts=shts, injs=injs, 
                                       lat=lats, lng=lngs, clr=GunShowLaw))
GunShow = plotLaw(sourceLaw, sourceRaw, 'Gun Show Laws vs. Shootings')

# Plots Safety Laws
SafetyLaw = laws['Safety'].tolist()
sourceLaw = ColumnDataSource(data=dict(name=name, shts=shts, injs=injs, 
                                       lat=lats, lng=lngs, clr=SafetyLaw))
Safety = plotLaw(sourceLaw, sourceRaw, 'Safety Laws vs. Shootings')

# Plots Restrict Laws
RestrictLaw = laws['Restrict'].tolist()
sourceLaw = ColumnDataSource(data=dict(name=name, shts=shts, injs=injs, 
                                       lat=lats, lng=lngs, clr=RestrictLaw))
Restrict = plotLaw(sourceLaw, sourceRaw, 'Gun Restriction Laws vs. Shootings')

# Saves Plot
listPlots = vplot(CarryHG, CarryLG, PurchHG, PurchLG, ShootFirst, GunShow,
                  Safety, Restrict)
save(listPlots)