""" PlotDriver ----------------------------------------------------------------
    Goal: Driver script to plot the data
----------------------------------------------------------------------------"""

# Needed on first run: from bokeh import sampledata; sampledata.download()

# Imports Bokeh Libraries
from bokeh.sampledata import us_states, us_counties
from bokeh.plotting import figure, save, output_file
import GunData as gd

# Download State & County Data
us_states = us_states.data.copy()
us_counties = us_counties.data.copy()

# Loads Gun Data and determines ratio based on population
us_shot = gd.loadGun()
us_pop = 

# Deletes HI & AK and sets a list of states we won't plot
del us_states["HI"]
del us_states["AK"]
banState = ["HI", "PR", "GU", "VI", "MP", "AS"]

# Gets coordinates for each state
state_xs = [us_states[code]["lons"] for code in us_states]
state_ys = [us_states[code]["lats"] for code in us_states]

# Sets colors where the keys are the 'Maximum' people shot in that range
colors = {40:'#FFE6E6', 80:'#FFB2B2', 120:'#FF8080', 160:'#FF4D4D', \
          200:'#FF1919', 300:'#E60000', 400:'#B20000', 500:'#800000', \
          600:'#4C0000', 700:'#1A0000', 800:'#000000'}
state_colors = []

# Loops through each state. We note how many people were shot in each state.
#   We compare that to the colors table & save the proper color for the state.
for state in us_states:
    if state in banState:
        continue
    try:
        peopleShot = us_shot[state]
        for maximum in sorted(colors):
            if peopleShot <= maximum:
                break
            else:
                color = colors[maximum]
        state_colors.append(color)
    except KeyError:
        state_colors.append("white")

# Create output file for plot
output_file("usShot.html", title="Number of People Shot")

# Create figure for plot
p = figure(title="Number of People Shot 2013-15", toolbar_location="left", plot_width=1100, plot_height=700)

# Color in the plot
p.patches(state_xs, state_ys, fill_color=state_colors, line_color="#884444", line_width=2)

# Save plot
save(p)