# -*- coding: utf-8 -*-
""" DownloadGoogle -------------------------------------------------------------
    Goal:   Using the us_shot dictionary of {city: <shootings>}, we parse each
            city for its coordinates and zip it up to a data frame.
-----------------------------------------------------------------------------"""

import geocoder as gc
import GunData as gd
import pandas as pd

us_shot, us_attk= gd.loadGun(True)
ctys = []
lats = []
lngs = []

# Saves each city & shooting together
for location in us_shot:
    try:
        cty = gc.google(location).county + ', ' + gc.google(location).state
    except:
        print('Error at '+location)
        cty = location
    lat = gc.google(location).lat
    lng = gc.google(location).lng
    ctys.append(cty)
    lats.append(lat)
    lngs.append(lng)
    
outData = zip(us_shot, [us_shot[key] for key in us_shot], ctys, lats, lngs)
outDf = pd.DataFrame(outData, columns=['City', 'Shooting', 'Cty', 'Lat', 'Lng'])
outDf = outDf.set_index(outDf.City, drop=True)
outDf.to_csv('ShootingData2.csv')

