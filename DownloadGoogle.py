# -*- coding: utf-8 -*-
""" DownloadGoogle -------------------------------------------------------------
    Goal:   Using the us_shot dictionary of {city: <shootings>}, we parse each
            city for its coordinates and zip it up to a data frame.
-----------------------------------------------------------------------------"""

import geocoder
import GunData as gd
import pandas as pd

us_shot, us_attk= gd.loadGun(True)
lats = []
lngs = []

for location in us_shot:
    # Sets Coordinates
    lat = geocoder.google(location).lat
    lng = geocoder.google(location).lng
    lats.append(lat)
    lngs.append(lng)
    
outData = zip(us_shot, [us_shot[key] for key in us_shot], lats, lngs)
outDf = pd.DataFrame(outData, columns=['City', 'Shootings', 'Lat', 'Lng'])
outDf = outDf.set_index(outDf.City, drop=True)
outDf.to_csv('ShootingData.csv')