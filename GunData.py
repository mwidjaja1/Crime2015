""" GunData -------------------------------------------------------------------
    Goal: Loads the CSV Files to get Mass Shooting data
    
    Input:  CSV Files for 2013, 2014, and 2015 in a directory
    Output: A dictionary with {state: Shootings} 
----------------------------------------------------------------------------"""

import glob
import pandas as pd


inDir = '/Users/Matthew/Github/Crime2015/Data/'
shooterDf = pd.DataFrame()


for csvFile in glob.glob(inDir + '*.csv'):
    csvDF = pd.read_csv(csvFile, sep=',', header=0)
    shooterDf = shooterDf.append(csvDF)