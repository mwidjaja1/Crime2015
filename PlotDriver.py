""" PlotDriver ----------------------------------------------------------------
    Goal: Driver script to plot the data
----------------------------------------------------------------------------"""

# Needed on first run: from bokeh import sampledata; sampledata.download()

# Imports Bokeh Libraries
from bokeh.models import HoverTool
from bokeh.sampledata import us_states, us_counties
from bokeh.plotting import ColumnDataSource, figure, save, output_file, vplot
import GunData as gd
import numpy as np

# Download State & County Data
us_states = us_states.data.copy()
us_counties = us_counties.data.copy()

# Loads Gun Data and determines ratio based on population
us_shot = gd.loadGun()
us_pop = gd.loadPop()

# Deletes HI & AK and sets a list of states we won't plot
del us_states["HI"]
del us_states["AK"]
banState = ["HI", "PR", "GU", "VI", "MP", "AS", "US"]

# Gets coordinates for each state's borders
state_xs = [us_states[code]["lons"] for code in us_states]
state_ys = [us_states[code]["lats"] for code in us_states]

# Get coordinates for each state's midpoint
state_xs_mid = [np.mean(state) for state in state_xs]
state_ys_mid = [np.mean(state) for state in state_ys]

# Sets colors where the keys are the 'Maximum' people shot in that range
popColors = {40:'#FFE6E6', 80:'#FFB2B2', 120:'#FF8080', 160:'#FF4D4D', \
             200:'#FF1919', 300:'#E60000', 400:'#B20000', 500:'#800000', \
             600:'#4C0000', 700:'#1A0000', 800:'#000000'}
ratColors = {3:'#FFE6E6', 6:'#FFB2B2', 9:'#FF8080', 12:'#FF4D4D', \
             15:'#FF1919', 18:'#E60000', 21:'#B20000', 25:'#800000', \
             30:'#4C0000', 100:'#1A0000', 200:'#000000'}     
          
# Sets list of colors for raw population & ratios   
statePopColors = []
stateRatColors = []

# Plots Gun Shots based on Raw Population
# Loops through each state. We note how many people were shot in each state.
#   We compare that to the colors table & save the proper color for the state.
for state in us_states:
    if state in banState: continue
    try:
        # Obtains color for raw populations
        peopleShot = us_shot[state]
        color = '#FFE6E6'
        for maximum in sorted(popColors):
            if peopleShot <= maximum:
                statePopColors.append(color)
                break
            else:
                color = popColors[maximum]
        
        # Obtains color for state ratios
        ratio = int((us_shot[state]/us_pop[state]) * 1000000)
        color = '#FFE6E6'
        for maximum in sorted(ratColors):
            if ratio <= maximum:
                stateRatColors.append(color)
                break
            else:
                color = ratColors[maximum]
    except KeyError:
        statePopColors.append("white")

# Create output file for plot
output_file("usShot.html", title="Number of People Shot")

# Add Hover Tool
"""
source = ColumnDataSource(
        data=dict(
            x=state_xs,
            y=state_ys,
            shot=statePopColors,
        )
    )
    
hover = HoverTool(
        tooltips=[
            ("Index", "$index"),
            ("Coordinates", "($x, $y)"),
            ("Shot", "statePopColors[$index]"),
        ]
    )
"""

# Create figure & plot for Raw Population
p1 = figure(title="People Shot in 2013-15 vs. Raw Populations", toolbar_location="left", \
            plot_width=1100, plot_height=700)
p1.patches(state_xs, state_ys, fill_color=statePopColors, line_color="#884444", line_width=2)
p1.circle(state_xs_mid, state_ys_mid, size=5, color="navy", alpha=0.8)


# Create figure & plot for Ratios
p2 = figure(title="People Shot 2013-15 as a Ratio vs. State Populations", toolbar_location="left", \
            plot_width=1100, plot_height=700)
p2.patches(state_xs, state_ys, fill_color=stateRatColors, line_color="#884444", line_width=2)

# Saves plot as a vertically stacked page
p = vplot(p1, p2)
save(p)