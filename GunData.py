import glob
import pandas as pd

""" loadGun -------------------------------------------------------------------
    Goal:   Loads the CSV Files to get how many people were shot or injured
            per state.
    
    Input:  (Not explicitly) CSV Files for 2013, 2014, & 2015 in a directory
            specifed as inDir below. 
    Output: A dictionary with {state: <sum of all people shot & injured>} 
----------------------------------------------------------------------------"""
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

