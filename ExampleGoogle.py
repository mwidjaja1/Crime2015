# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 20:51:35 2015

@author: Matthew
"""

from __future__ import print_function

from bokeh.browserlib import view
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.models.glyphs import Circle
from bokeh.models import (
    GMapPlot, Range1d, ColumnDataSource,
    PanTool, WheelZoomTool, BoxSelectTool,
    BoxSelectionOverlay, GMapOptions)
from bokeh.resources import INLINE

x_range = Range1d()
y_range = Range1d()

# JSON style string taken from: https://snazzymaps.com/style/1/pale-dawn
map_options = GMapOptions(lat=39.50, lng=-98.35, map_type="roadmap", zoom=4)

plot = GMapPlot(
    x_range=x_range, y_range=y_range,
    map_options=map_options,
    plot_width=1100, plot_height=650,
    title="United States"
)

source = ColumnDataSource(
    data=dict(
        lat=[30.2861, 30.2855, 30.2869],
        lon=[-97.7394, -97.7390, -97.7405],
        fill=['orange', 'blue', 'green']
    )
)

circle = Circle(x="lon", y="lat", size=15, fill_color="fill", line_color="black")
plot.add_glyph(source, circle)

pan = PanTool()
wheel_zoom = WheelZoomTool()
box_select = BoxSelectTool()

plot.add_tools(pan, wheel_zoom, box_select)
overlay = BoxSelectionOverlay(tool=box_select)
plot.add_layout(overlay)

doc = Document()
doc.add(plot)

if __name__ == "__main__":
    filename = "maps.html"
    with open(filename, "w") as f:
        f.write(file_html(doc, INLINE, "Google Maps Example"))
    print("Wrote %s" % filename)
    view(filename)