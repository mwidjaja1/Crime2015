# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 20:51:35 2015

@author: Matthew
"""

from __future__ import print_function

# Imports Google Maps stuff
from bokeh.models.glyphs import Circle
from bokeh.models import (
    GMapPlot, Range1d, ColumnDataSource,
    PanTool, WheelZoomTool, BoxSelectTool,
    BoxSelectionOverlay, GMapOptions)

# Imports Bokeh Libraries
from bokeh.plotting import output_file, save

# Imports Other Libraries
import pandas as pd

# Imports other inhouse functions
import GunData as gdt
import LawData as ldt
import PlotData as pdt

x_range = Range1d()
y_range = Range1d()

# Creates Output File
output_file("maps.html", title="Number of People Shot")

# Sets Google Map for America in Bokeh
map_options = GMapOptions(lat=39.50, lng=-98.35, map_type="roadmap", zoom=4)
plot = GMapPlot(x_range=x_range, y_range=y_range, map_options=map_options, \
                plot_width=1100, plot_height=650, title="United States")

# Loads DataFrame from DownloadGoogle with City, Shootings, Lat, & Long.
inFile = '/Users/Matthew/Github/Crime2015/MyData/ShootingData.csv'
inData = pd.read_csv(inFile, index_col='City')

# Set Color Options
attkColors = {5:'#CCE0FF', 10:'#99C2FF', 15:'#66A3FF', 20:'#3385FF', \
              25:'#0066FF', 30:'#0052CC', 40:'#003D99', 50:'#002966', \
              60:'#001433', 70:'#000A1A', 200:'#000000'}
clrs = []

# Gets Coordinates & Color for each City
for location in inData.index:
    shootings = inData.loc[location, 'Shootings']
    color = '#CCE0FF'
    for maximum in sorted(attkColors):
        if shootings <= maximum:
            clrs.append(color)
            break
        else:
            color = attkColors[maximum]

# Sets Data for Shots 
source = ColumnDataSource(
    data=dict(
        lat=inData.Lat,
        lon=inData.Lng,
        clr=clrs
    )
)

# Create Circle Plot
circle = Circle(x="lon", y="lat", size=15, fill_color="clr", line_color="black")
plot.add_glyph(source, circle)

# Create Tools
pan = PanTool()
wheel_zoom = WheelZoomTool()
box_select = BoxSelectTool()
plot.add_tools(pan, wheel_zoom, box_select)
overlay = BoxSelectionOverlay(tool=box_select)
plot.add_layout(overlay)

# Saves Plot
save(plot)