import glob
import pandas as pd

""" loadGun --------------------------------------------------------------------
    Goal:   Loads the CSV Files to get how many people were shot or injured
            per state from http://shootingtracker.com.
    From:   Main Function
    
    Input:  (Not explicitly) CSV Files for 2013, 2014, & 2015 in a directory
            specifed as inDir below. 
    Output: A dict with {stateSymbol: <sum of all people shot & injured>} 
-----------------------------------------------------------------------------"""
def loadGun():
    # Set Input Paths & Dataframe
    inDir = '/Users/Matthew/Github/Crime2015/Data/'
    shooterDf = pd.DataFrame()
    
    # Concats each year Dataframe into one
    for csvFile in glob.glob(inDir + '*.csv'):
        csvDF = pd.read_csv(csvFile, sep=',', header=0)
        shooterDf = shooterDf.append(csvDF)
    
    # Replace States in list
    replaceDict = {'Illinois': 'IL', 'KA':'KS', 'Kansas':'KS', 'Louisiana':'LA', 'Mo':'MO', 'Ohio':'OH',\
                   'Puerto Rico':'PR', 'Tennessee':'TN'}
    shooterDf.replace(replaceDict, regex=True, inplace=True)
    
    # Saves State in Location Column
    location = pd.DataFrame(shooterDf.Location.str.split(', ').tolist(),columns=['City', 'State'])
    shooterDf['Location'] = location['State']
    
    # Calculates new Data Frame with summed up values for each state
    sumStateDf = shooterDf.groupby(['Location']).sum()
    sumStateDf['All'] = sumStateDf.sum(axis=1)
    
    # Converts DataFrame to Dictionary
    sumStateDict = sumStateDf.to_dict()
    sumStateDict = sumStateDict['All']

    return sumStateDict

""" loadPop --------------------------------------------------------------------
    Goal:   Loads the CSV Files which contains 2014 predicted population per
            state from http://www.census.gov/popest/data/datasets.html.
    From:   Main Function
    
    Input:  (Not explicitly) CSV File for 2014 in a directory specified below
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

