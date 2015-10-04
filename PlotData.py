#from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource, figure

""" plotData -------------------------------------------------------------------
    Goal:   Creates 2 Bokeh plots on a map of America for raw populations and
            ratios for gun shot victims & laws.
    From:   Main Function
    
    Input:  Each State's (1) xCoordinates, (2) yCoordinates, (3) shaded colors
            for raw populations, & (4) shaded colors for ratios.
            
            If applicable, (5) a list of booleans for each state noting if the 
            circle dot above it should be marked and this circle will be saved
            on each state's midpoint based on a (6) dictionary of midpoints like
            {state: {x:<x>, y:<y>}. Set these to None if this isn't applicable.
            
            Finally, provide a title for the (7) raw plot & (8) ratios plot
    Output: A list of the two plots.
-----------------------------------------------------------------------------"""
def plotData(x, y, colors1, colors2, laws1, midpt, pTitle1, pTitle2):
    # Default Tools
    toolbar = "pan,wheel_zoom,box_zoom,reset,resize"
        
    # Create figure & shades for shots vs raw population
    p1 = figure(title=pTitle1, tools=toolbar, toolbar_location="above", \
                plot_width=625, plot_height=400)
    p1.patches(x, y, fill_color=colors1, line_color="#884444", line_width=2)
    
    # Create figure & plot for Ratios
    p2 = figure(title=pTitle2, tools=toolbar, toolbar_location="above", \
                plot_width=625, plot_height=400)
    p2.patches(x, y, fill_color=colors2, line_color="#884444", line_width=2)
    
    # Adds shapes to symbolize a state's laws
    if midpt:    
        for state in midpt:
            p1.circle(midpt[state]['x'], midpt[state]['y'], color="navy", \
                      size=8, alpha=0.8)
            p2.circle(midpt[state]['x'], midpt[state]['y'], color="navy", \
                      size=8, alpha=0.8)
                  
    return [p1, p2]
    
    
""" SetsLaws -------------------------------------------------------------------
    Goal:   Determines the color the 'Law' circle should be based on the law
            data provided.
    From:   Main Function
    
    Input:  Each State's (1) xCoordinates, (2) yCoordinates, (3) shaded colors
            for raw populations, & (4) shaded colors for ratios.
            
            If applicable, (5) a list of booleans for each state noting if the 
            circle dot above it should be marked and this circle will be saved
            on each state's midpoint based on a (6) dictionary of midpoints like
            {state: {x:<x>, y:<y>}. Set these to None if this isn't applicable.
            
            Finally, provide a title for the (7) raw plot & (8) ratios plot
    Output: A list of the two plots.
-----------------------------------------------------------------------------"""