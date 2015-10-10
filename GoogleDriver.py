# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 20:51:35 2015

@author: Matthew
"""

from __future__ import print_function

# Imports Google Maps stuff
from bokeh.models.glyphs import Circle, Patches
from bokeh.models import (GMapPlot, Range1d, ColumnDataSource, PanTool, \
                          WheelZoomTool, BoxSelectTool, BoxSelectionOverlay, \
                          ResetTool, GMapOptions)

# Imports Bokeh Libraries
from bokeh.plotting import output_file, save

# Imports Other Libraries
import pandas as pd

# Imports other inhouse functions
import GunData as gdt
import LawData as ldt

# Creates Output File
output_file("maps.html", title="Number of People Shot")

# Sets Google Map for America in Bokeh
x_range = Range1d()
y_range = Range1d()
map_options = GMapOptions(lat=39.50, lng=-98.35, map_type="roadmap", zoom=4)
plot = GMapPlot(x_range=x_range, y_range=y_range, map_options=map_options, \
                plot_width=1100, plot_height=650, title="United States")


""" main: Downloads all Laws & Coordinate Data ------------------------------"""
# Gets State Coordinates
stateBorder = gdt.loadBorder()
lats = [stateBorder[item]['lat'] for item in sorted(stateBorder)]
lngs = [stateBorder[item]['lng'] for item in sorted(stateBorder)]

# Downloads Legal Data
laws = ldt.loadLaw()
laws = laws.sort_index()
laws = laws.drop('DC')

# Sets Color List
clrs = laws['CarryHG'].tolist()

# Zips Coordinates & Colors together
data = zip(lats, lngs, clrs)

# Sets Data for each State 
#for st in data:
source = ColumnDataSource(data=dict(lat=lats, lng=lngs, clr=clrs))
patch = Patches(xs="lng", ys="lat", fill_alpha=0.5, fill_color="clr")
plot.add_glyph(source, patch)


""" main: Creates plot for shootings per county -----------------------------"""
# Loads DataFrame from DownloadGoogle with City, Shootings, Lat, & Long.
inFile = '/Users/Matthew/Github/Crime2015/MyData/ShootingData2.csv'
inData = pd.read_csv(inFile, index_col='City')

# Groups all entries by counties
inData = inData.groupby(['Cty']).sum()

# Set Color Options
attkColors = {5:'#CCE0FF', 10:'#99C2FF', 20:'#66A3FF', 30:'#3385FF', \
              40:'#0066FF', 50:'#0052CC', 60:'#003D99', 70:'#002966', \
              85:'#001433', 100:'#000A1A', 300:'#000000'}
clrs = []

# Sets Color for each County
for location in inData.index:
    shootings = inData.loc[location, 'Shooting']
    color = '#CCE0FF'
    for maximum in sorted(attkColors):
        if shootings <= maximum:
            clrs.append(color)
            break
        else:
            color = attkColors[maximum]

# Sets Data for Shots 
source = ColumnDataSource(data=dict(lat=inData.Lat, lng=inData.Lng, clr=clrs))

# Create Circles on Plot
circle = Circle(x="lng", y="lat", size=15, fill_color="clr", line_color="black")
plot.add_glyph(source, circle)


""" main: Renders & Saves Plot ----------------------------------------------"""
# Create Tools
pan = PanTool()
wheel_zoom = WheelZoomTool()
box_select = BoxSelectTool()
reset = ResetTool()
plot.add_tools(pan, wheel_zoom, box_select, reset)
overlay = BoxSelectionOverlay(tool=box_select)
plot.add_layout(overlay)

# Saves Plot
save(plot)