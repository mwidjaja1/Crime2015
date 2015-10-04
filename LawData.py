import glob
import pandas as pd

""" loadMid --------------------------------------------------------------------
    Goal:   Loads & sets the midpoint in each state using Bokeh's coordinates.
            We set all continental 48 states & DC here.
    From:   Main Function
    
    Input:  Nothing. 
    Output: Dictionary with each state's midpoint
-----------------------------------------------------------------------------"""
def loadMid():
    midpoint= {'AL': {'x':-86.8, 'y':32.9},
               'AR': {'x':-92.6, 'y':34.7},
               'AZ': {'x':-112, 'y':34.3},
               'CA': {'x':-119, 'y':37.1},
               'CO': {'x':-105.5, 'y':38.9},
               'CT': {'x':-72.6, 'y':41.5},
               'DC': {'x':-77.1, 'y':38.7},
               'DE': {'x':-75.4, 'y':38.9},
               'FL': {'x':-81.7, 'y':28},
               'GA': {'x':-83.5, 'y':32.9},
               'IA': {'x':-93.5, 'y':42},
               'ID': {'x':-114.4, 'y':44.1},
               'IL': {'x':-89, 'y':40},
               'IN': {'x':-86.2, 'y':40.0},
               'KS': {'x':-98.3, 'y':38.6},
               'KY': {'x':-85.6, 'y':37.4},
               'LA': {'x':-92.4, 'y':31},
               'MA': {'x':-71.8, 'y':42.3},
               'MD': {'x':-76.3, 'y':38.5},
               'ME': {'x':-69, 'y':45},
               'MI': {'x':-84.9, 'y':44.3},
               'MN': {'x':-94.4, 'y':45.9},
               'MO': {'x':-92.6, 'y':38.4},
               'MS': {'x':-89.8, 'y':32.8},
               'MT': {'x':-109.2, 'y':46.9},
               'NC': {'x':-78.8, 'y':35.4},
               'ND': {'x':-100.5, 'y':47.5},
               'NE': {'x':-100, 'y':41.4},
               'NH': {'x':-71.7, 'y':43.2},
               'NJ': {'x':-74.3, 'y':40},
               'NM': {'x':-106.1, 'y':34.5},
               'NV': {'x':-117, 'y':39},
               'NY': {'x':-75.6, 'y':43},
               'OH': {'x':-82.8, 'y':40.4},
               'OK': {'x':-97.4, 'y':35.3},
               'OR': {'x':-120.7, 'y':43.8},
               'PA': {'x':-77.8, 'y':40.8},
               'RI': {'x':-71.4, 'y':41.5},
               'SC': {'x':-81, 'y':33.8},
               'SD': {'x':-100.2, 'y':44.2},
               'TN': {'x':-86.4, 'y':35.7},
               'TX': {'x':-99, 'y':31.1},
               'UT': {'x':-111.5, 'y':39.1},
               'VA': {'x':-78.2, 'y':37.5},
               'VT': {'x':-72.7, 'y':44.2},
               'WA': {'x':-120.6, 'y':47.3},
               'WI': {'x':-89.9, 'y':44.2},
               'WV': {'x':-80.7, 'y':38.5},
               'WY': {'x':-107.7, 'y':43}}
              
    # Creates list of coordinates from dictionary
    #state_xs_mid = [midpoint[state]['x'] for state in midpoint]
    #state_ys_mid = [midpoint[state]['y'] for state in midpoint]
    
    return midpoint
    

""" loadLaw --------------------------------------------------------------------
    Goal:   Loads the CSV Files to get how many people were shot or injured
            per state from http://shootingtracker.com.
    From:   Main Function
    
    Input:  (Not explicitly) CSV Files current gun laws from inDir
    Output: A Data Frame with the gun laws
-----------------------------------------------------------------------------"""
def loadLaw():
    # Set Input Paths & Dataframe
    inDir = '/Users/Matthew/Github/Crime2015/Laws/'
    lawDF = pd.DataFrame()
    
    # Concats each year Dataframe into one
    for csvFile in glob.glob(inDir + '*.csv'):
        csvDF = pd.read_csv(csvFile, sep=',', header=0)
        lawDF = lawDF.append(csvDF)
        
    # Sets index
    lawDF = lawDF.set_index('State')
    
    # Converts DataFrame to Dictionary
    #sumStateDict = sumStateDf.to_dict()
    #sumStateDict = sumStateDict['All']

    return lawDF