""" PlotDriver -----------------------------------------------------------------
    Goal: Driver script to plot the data
-----------------------------------------------------------------------------"""

# Needed on first run: from bokeh import sampledata; sampledata.download()

# Imports Bokeh Libraries
from bokeh.io import gridplot, vplot
from bokeh.plotting import output_file, save
from bokeh.sampledata import us_states, us_counties

# Imports other inhouse functions
import GunData as gd
import LawData as ld
import PlotData as pd

# Download State & County Data
us_states = us_states.data.copy()
us_counties = us_counties.data.copy()

# Loads Gun Data
us_shot, us_attk= gd.loadGun()
us_pop = gd.loadPop()

# Loads Laws per state
us_law = ld.loadLaw()

# Deletes HI & AK and sets a list of states we won't plot
del us_states["HI"]
del us_states["AK"]
banState = ["HI", "PR", "GU", "VI", "MP", "AS", "US"]

# Sorts all lists by state alphabetical order
#us_shot = [us_shot[state] for state in sorted(us_shot)]
#us_pop = [us_pop[state] for state in sorted(us_pop)]

# Gets coordinates for each state's borders
state_xs = [us_states[state]["lons"] for state in us_states]
state_ys = [us_states[state]["lats"] for state in us_states]

# Get coordinates for each state's midpoint
midpoint = ld.loadMid()
state_xs_mid = [midpoint[state]['x'] for state in midpoint]
state_ys_mid = [midpoint[state]['y'] for state in midpoint]

# Sets colors where the keys are the 'Maximum' people shot in that range
popColors = {40:'#CCE0FF', 80:'#99C2FF', 120:'#66A3FF', 160:'#3385FF', \
             200:'#0066FF', 300:'#0052CC', 400:'#003D99', 500:'#002966', \
             600:'#001433', 700:'#000A1A', 800:'#000000'}
ratColors = {3:'#CCE0FF', 6:'#99C2FF', 9:'#66A3FF', 12:'#3385FF', \
             15:'#0066FF', 18:'#0052CC', 21:'#003D99', 25:'#002966', \
             30:'#001433', 100:'#000A1A', 200:'#000000'}     
attkColors = {10:'#CCE0FF', 20:'#99C2FF', 30:'#66A3FF', 40:'#3385FF', \
              50:'#0066FF', 60:'#0052CC', 70:'#003D99', 80:'#002966', \
              90:'#001433', 100:'#000A1A', 200:'#000000'}
          
# Sets list of colors for raw population & ratios   
shotPopColors = []
shotRatColors = []
attkPopColors = []

# Plots Gun Shots based on Raw Population
# Loops through each state. We note how many people were shot in each state.
#   We compare that to the colors table & save the proper color for the state.
for state in us_states:
    if state in banState: continue
    try:
        # Obtains color for raw populations
        peopleShot = us_shot[state]
        color = '#CCE0FF'
        for maximum in sorted(popColors):
            if peopleShot <= maximum:
                shotPopColors.append(color)
                break
            else:
                color = popColors[maximum]
        
        # Obtains color for state ratios
        ratio = int((us_shot[state]/us_pop[state]) * 1000000)
        color = '#CCE0FF'
        for maximum in sorted(ratColors):
            if ratio <= maximum:
                shotRatColors.append(color)
                break
            else:
                color = ratColors[maximum]
    except KeyError:
        shotRatColors.append("white")
        shotPopColors.append("white")

# Plots Gun Shots based on Raw Population
# Loops through each state. We note how many people were shot in each state.
#   We compare that to the colors table & save the proper color for the state.
for state in us_states:
    if state in banState: continue
    try:
        # Obtains color for raw populations
        peopleShot = us_attk[state]
        color = '#CCE0FF'
        for maximum in sorted(attkColors):
            if peopleShot <= maximum:
                attkPopColors.append(color)
                break
            else:
                color = attkColors[maximum]
    except KeyError:
        attkPopColors.append("white")

# Create output file for plot
output_file("usShot.html", title="Number of People Shot")

# 1>> Does generic plot
standPlot = pd.gridData(state_xs, state_ys, shotPopColors, shotRatColors, \
                        None, None, '(Gun Shot) Victims', \
                        'Gun Shot Victims vs. State Population (Ratio)')

# Does carrying handgun plot
carryHGPlot = pd.gridData(state_xs, state_ys, shotPopColors, shotRatColors, \
                          us_law.CarryHG, midpoint, \
                          'Victims vs. HG Carry Laws', \
                          'Ratio vs. HG Carry Laws')

# Does carrying longgun plot
carryLGPlot = pd.gridData(state_xs, state_ys, shotPopColors, shotRatColors, \
                          us_law.CarryLG, midpoint, \
                          'Victims vs. LG Carry Laws', \
                          'Ratio vs. LG Carry Laws')
                       
 # Does purchasing handgun plot
purchHGPlot = pd.gridData(state_xs, state_ys, shotPopColors, shotRatColors, \
                          us_law.PurchaseHG, midpoint, \
                          'Victims vs. HG Purchase Laws', \
                          'Ratio vs. HG Purchase Laws')

# Does purchasing longgun plot
purchLGPlot = pd.gridData(state_xs, state_ys, shotPopColors, shotRatColors, \
                          us_law.PurchaseLG, midpoint, \
                          'Victims vs. LG Purchase Laws', \
                          'Ratio vs. LG Purchase Laws')

# Does shoot first plot
firstPlot = pd.gridData(state_xs, state_ys, shotPopColors, shotRatColors, \
                        us_law.ShootFirst, midpoint, \
                        'Victims vs. Shoot First Laws', \
                        'Ratio vs. Shoot First  Laws')

# Does gunshow plot
gshowPlot = pd.gridData(state_xs, state_ys, shotPopColors, shotRatColors, \
                        us_law.GunShow, midpoint, 'Victims vs. Gunshow Laws', \
                        'Ratio vs. Gunshow Laws')

# Does safety plot
safesPlot = pd.gridData(state_xs, state_ys, shotPopColors, shotRatColors, \
                        us_law.ShootFirst, midpoint, \
                        'Victims vs. Shoot First Laws', \
                        'Ratio vs. Shoot First  Laws')

# Does restrictions plot
restrPlot = pd.gridData(state_xs, state_ys, shotPopColors, shotRatColors, \
                        us_law.Restrict, midpoint, 'Victims vs. Restrictions', \
                        'Ratio vs. Restrictions')

# Saves plot as a vertically stacked page
p = gridplot([standPlot, carryHGPlot, carryLGPlot, purchHGPlot, purchLGPlot, \
              firstPlot, gshowPlot, safesPlot, restrPlot])
save(p)

# Create output file for plot
output_file("usAttk.html", title="Number of Attacks")

# 2>> Does generic plot
standPlot = pd.plotData(state_xs, state_ys, attkPopColors, None, None, \
                        'Gun Shootings')

# Does carrying handgun plot
carryHGPlot = pd.plotData(state_xs, state_ys, attkPopColors, us_law.CarryHG, 
                          midpoint, 'Shootings vs. HG Carry Laws')

# Does carrying longgun plot
carryLGPlot = pd.plotData(state_xs, state_ys, attkPopColors, us_law.CarryLG, \
                          midpoint, 'Shootings vs. LG Carry Laws')
                       
 # Does purchasing handgun plot
purchHGPlot = pd.plotData(state_xs, state_ys, attkPopColors, us_law.PurchaseHG,\
                          midpoint, 'Shootings vs. HG Purchase Laws')

# Does purchasing longgun plot
purchLGPlot = pd.plotData(state_xs, state_ys, attkPopColors, us_law.PurchaseLG,\
                          midpoint, 'Shootings vs. LG Purchase Laws')

# Does shoot first plot
firstPlot = pd.plotData(state_xs, state_ys, attkPopColors, us_law.ShootFirst, \
                        midpoint, 'Shootings vs. Shoot First Laws')

# Does gunshow plot
gshowPlot = pd.plotData(state_xs, state_ys, attkPopColors, us_law.GunShow, \
                        midpoint, 'Shootings vs. Gunshow Laws')

# Does safety plot
safesPlot = pd.plotData(state_xs, state_ys, attkPopColors, us_law.ShootFirst, \
                        midpoint, 'Shootings vs. Shoot First Laws')

# Does restrictions plot
restrPlot = pd.plotData(state_xs, state_ys, attkPopColors, us_law.Restrict, \
                        midpoint, 'Shootings vs. Restrictions')

# Saves plot as a vertically stacked page
p = vplot(standPlot, carryHGPlot, carryLGPlot, purchHGPlot, purchLGPlot, \
           firstPlot, gshowPlot, safesPlot, restrPlot)
save(p)
