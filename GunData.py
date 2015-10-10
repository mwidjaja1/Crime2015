import glob
import pandas as pd
import xml.etree.ElementTree as et

""" loadGun --------------------------------------------------------------------
    Goal:   Loads the CSV Files to get how many people were shot or injured
            per state from http://shootingtracker.com.
    From:   Main Function
    
    Input:  (Not explicitly) CSV Files for 2013, 2014, & 2015 in a directory
            specifed as inDir below. Also set (1) True = Save City, State vs. 
            False = Save State only
    Output: Two dicts where one counts how many people were shot/injured per
            state as {stateSymbol: <sum of all people shot & injured>} & the 
            other counts shootings per state as {stateSymbol: <sum of attacks>}
-----------------------------------------------------------------------------"""
def loadGun(saveCity):
    # Set Input Paths & Dataframe
    inDir = '/Users/Matthew/Github/Crime2015/Data/'
    shooterDf = pd.DataFrame()
    
    # Concats each year Dataframe into one
    for csvFile in glob.glob(inDir + '*.csv'):
        csvDF = pd.read_csv(csvFile, sep=',', header=0)
        shooterDf = shooterDf.append(csvDF)
    
    # Replace States in list
    replaceDict = {'Illinois': 'IL', 'KA':'KS', 'Kansas':'KS', 'Louisiana':'LA',
                   'Mo':'MO', 'Ohio':'OH', 'Puerto Rico':'PR', 'Tennessee':'TN'}
    shooterDf.replace(replaceDict, regex=True, inplace=True)
    
    # Saves State in Location Column
    if saveCity is False:
        location = pd.DataFrame(shooterDf.Location.str.split(', ').tolist(), \
                                columns=['City', 'State'])
        shooterDf['Location'] = location['State']
    
    # Calculates new Data Frame with summed up values for each state
    sumStateDf = shooterDf.groupby(['Location']).sum()
    sumStateDf['All'] = sumStateDf.sum(axis=1)
    
    # Converts DataFrame to Dictionary
    sumStateDict = sumStateDf.to_dict()
    sumStateDict = sumStateDict['All']

    # Creates second dictioanry for how many shootings were done per state
    allStateDict = shooterDf.Location.value_counts().to_dict()

    return sumStateDict, allStateDict

""" loadPop --------------------------------------------------------------------
    Goal:   Loads the CSV Files which contains 2014 predicted population per
            state from http://www.census.gov/popest/data/datasets.html.
    From:   Main Function
    
    Input:  (Not explicitly) CSV File for 2014 in a directory specified below.
    Output: A dict with {stateSymbol: <population>} 
-----------------------------------------------------------------------------"""
def loadPop():
    # Set Input Paths & Dataframe
    inDir = '/Users/Matthew/Github/Crime2015/Population/'
    populationDf = pd.DataFrame()
    
    # Concats each year Dataframe into one
    for csvFile in glob.glob(inDir + '*.csv'):
        csvDF = pd.read_csv(csvFile, sep=',', header=0)
        populationDf = populationDf.append(csvDF)
    
    # Replace States in list
    replaceDict = {'United States':'US', 'Alaska':'AK', 'Alabama':'AL', 
                   'Arkansas':'AR', 'Arizona':'AZ', 'California':'CA',
                   'Colorado':'CO', 'Connecticut':'CT', 
                   'District of Columbia':'DC', 'Delaware':'DE', 
                   'Florida':'FL', 'Georgia':'GA', 'Hawaii':'HI',
                   'Iowa':'IA', 'Idaho':'ID', 'Illinois':'IL', 
                   'Indiana':'IN', 'Kansas':'KS', 'Kentucky':'KY', 
                   'Louisiana':'LA', 'Massachusetts':'MA', 'Maryland':'MD', 
                   'Maine':'ME', 'Michigan':'MI', 'Minnesota':'MN',
                   'Missouri':'MO', 'Mississippi':'MS', 'Montana':'MT', 
                   'North Carolina':'NC', 'North Dakota':'ND',
                   'Nebraska':'NE', 'New Hampshire':'NH', 'New Jersey':'NJ',
                   'New Mexico':'NM', 'Nevada':'NV', 'New York':'NY',
                   'Ohio':'OH', 'Oklahoma':'OK', 'Oregon':'OR',
                   'Pennsylvania':'PA', 'Puerto Rico Commonwealth':'PR',
                   'Rhode Island':'RI', 'South Carolina':'SC',
                   'South Dakota':'SD', 'Tennessee':'TN', 'Texas':'TX',
                   'Utah':'UT', 'Virginia':'VA', 'Virgin Islands':'VI',
                   'Vermont':'VT', 'Washington':'WA', 'Wisconsin':'WI',
                   'West Virginia':'WV', 'Wyoming':'WY',}
    populationDf.replace(replaceDict, regex=True, inplace=True) 
    
    # Gets US Population & sets index for DF based on state
    populationDf = populationDf.set_index('NAME')
    
    # Converts DataFrame to Dictionary
    populationDf = populationDf['POPESTIMATE2014'].divide(1)
    populationDict = populationDf.to_dict()

    return populationDict


""" loadBorder -----------------------------------------------------------------
    Goal:   Loads the XML file with state boundaries and parses it into a dict
            of {state:{lat:<lat>, lng:<long>}}
    From:   Main Function
    
    Input:  (Not explicitly) XML File for state boundary coordinates in a dir
            specified below.
    Output: A dict with {state:{lat:<lat>, lng:<long>}}
-----------------------------------------------------------------------------"""
def loadBorder():
    # Set Input Paths & Dictionary
    inDir = '/Users/Matthew/Github/Crime2015/MyData/'
    outDict = {}

    # Finds Root of XML file
    tree = et.parse(glob.glob(inDir + '*.xml')[0])
    root = tree.getroot()
    
    # Stores Abbreviation to Full Name Table
    replaceDict = {'United States':'US', 'Alaska':'AK', 'Alabama':'AL', 
                   'Arkansas':'AR', 'Arizona':'AZ', 'California':'CA',
                   'Colorado':'CO', 'Connecticut':'CT', 
                   'District of Columbia':'DC', 'Delaware':'DE', 
                   'Florida':'FL', 'Georgia':'GA', 'Hawaii':'HI',
                   'Iowa':'IA', 'Idaho':'ID', 'Illinois':'IL', 
                   'Indiana':'IN', 'Kansas':'KS', 'Kentucky':'KY', 
                   'Louisiana':'LA', 'Massachusetts':'MA', 'Maryland':'MD', 
                   'Maine':'ME', 'Michigan':'MI', 'Minnesota':'MN',
                   'Missouri':'MO', 'Mississippi':'MS', 'Montana':'MT', 
                   'North Carolina':'NC', 'North Dakota':'ND',
                   'Nebraska':'NE', 'New Hampshire':'NH', 'New Jersey':'NJ',
                   'New Mexico':'NM', 'Nevada':'NV', 'New York':'NY',
                   'Ohio':'OH', 'Oklahoma':'OK', 'Oregon':'OR',
                   'Pennsylvania':'PA', 'Puerto Rico Commonwealth':'PR',
                   'Rhode Island':'RI', 'South Carolina':'SC',
                   'South Dakota':'SD', 'Tennessee':'TN', 'Texas':'TX',
                   'Utah':'UT', 'Virginia':'VA', 'Virgin Islands':'VI',
                   'Vermont':'VT', 'Washington':'WA', 'Wisconsin':'WI',
                   'West Virginia':'WV', 'Wyoming':'WY',}
    
    # Finds each State
    for state in root.findall('state'):
        name = state.attrib['name']
        name = replaceDict[name]
        lat = []
        lng = []
        
        # Finds the coordinates for each state
        for point in state.iter('point'):
            lat.append(point.attrib['lat'])
            lng.append(point.attrib['lng'])
        
        # Adds entry for the state to the dictionary
        outDict[name] = {'lat':lat, 'lng':lng}
    
    return outDict