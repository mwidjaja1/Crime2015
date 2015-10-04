import glob
import pandas as pd

""" loadGun -------------------------------------------------------------------
    Goal: Loads the CSV Files to get Mass Shooting data
    
    Input:  CSV Files for 2013, 2014, and 2015 in a directory
    Output: A dictionary with {state: Shootings} 
----------------------------------------------------------------------------"""
def loadGun(inPath):
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
    location = pd.DataFrame(shooterDf.Location.str.split(',').tolist(),columns=['City', 'State'])
    shooterDf['Location'] = location['State']
    
    # Calculates Data Frame with summed up values for each state
    sumStateDf = shooterDf.groupby(['Location']).sum()

    return sumStateDf

