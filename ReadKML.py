# %%
from fastkml import kml
import numpy as np
import pandas as pd
from doepy import build, read_write
from math import *

redV = [0]*300
redH = [0]*300
orangeV = [0]*300
orangeH = [0]*300
yellowV= [0]*300
yellowH= [0]*300
originV = [0]*300
originH = [0]*300

data = pd.read_csv('Piscina_metanol.csv')

def haversine(lon1, lat1, lon2, lat2): 
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

#Read file into string and convert to UTF-8 (Python3 style)
for y in range(3, 203):

  #def getCoord(path):
  with open("KMLS/KML Report Piscina Metanol/"+str(y)+".kml", 'rb') as myfile:
    doc=myfile.read()
  # Create the KML object to store the parsed result
  k = kml.KML()
  k.from_string(doc)
  features = list(k.features())
  f2 = list(features[0].features())
  placemark =list(f2[0].features())
  for x in range(0,len(placemark)):

    coordinates = placemark[x].geometry._exterior.coords
    dataList = list(coordinates)
    df = pd.DataFrame(dataList, columns=['x', 'y'])
    lat = df['x']
    lon = df['y']
    ##lat2 max, (Lat, Long)
    latmax = lat.max()
    idlatmax = lat.idxmax()
    maxlatpair = lon[idlatmax]
    
    ##Lat 1 min, (Lat, long)
    latmin = lat.min()
    idlatmin = lat.idxmin()
    minlatpair = lon[idlatmin]
    
    ##Lon 2 max
    lonmax = lon.max()
    idlonmax = lon.idxmax()
    maxlonpair = lat[idlonmax]
  
    ##Lon 1 min
    lonmin = lon.min()
    idlonmin = lon.idxmin()
    minlonpair = lat[idlonmin]
    
    ##lat distance horizontal
    dh = haversine(minlatpair, latmin, maxlatpair, latmax)
    
    ##Lon distance vertical
    dv = haversine(lonmin, minlonpair, lonmax, maxlonpair)
    if "Yellow" in placemark[x].name:
      yellowV[y-3] = dv
      yellowH[y-3] = dh
      originH[y-3] = (dh - data['yellow distance'][y-3])
    if "Orange" in placemark[x].name:
      orangeV[y-3] = dv
      orangeH[y-3] = dh
    if "Red" in placemark[x].name:
      redV[y-3] = dv
      redH[y-3] = dh

data['Red Vertical distane'] = redV
data['Yellow Vertical distane'] = yellowV
data['Orange Vertical distane'] = orangeV
data['Red Horizontal distane'] = redH
data['Yellow Horizontal distane'] = yellowH
data['Orange Horizontal distane'] = orangeH
data['Origin'] = originH

read_write.write_csv(data,'Piscina_metanol')

# %%
with open("KMLS/KML Report Piscina Metanol/52.kml", 'rb') as myfile:
  doc=myfile.read()
  # Create the KML object to store the parsed result
  k = kml.KML()
  k.from_string(doc)
  features = list(k.features())
  f2 = list(features[0].features())
  placemark =list(f2[0].features())
  for x in range(0,len(placemark)):

    coordinates = placemark[x].geometry._exterior.coords
    dataList = list(coordinates)
    df = pd.DataFrame(dataList, columns=['x', 'y'])
    lat = df['x']
    lon = df['y']
    ##lat2 max, (Lat, Long)
    latmax = lat.max()
    idlatmax = lat.idxmax()
    maxlatpair = lon[idlatmax]
    
    ##Lat 1 min, (Lat, long)
    latmin = lat.min()
    idlatmin = lat.idxmin()
    minlatpair = lon[idlatmin]
    
    ##Lon 2 max
    lonmax = lon.max()
    idlonmax = lon.idxmax()
    maxlonpair = lat[idlonmax]
  
    ##Lon 1 min
    lonmin = lon.min()
    idlonmin = lon.idxmin()
    minlonpair = lat[idlonmin]
    
    ##lat distance horizontal
    dh = haversine(minlatpair, latmin, maxlatpair, latmax)
    print("dh",dh)
    
    ##Lon distance vertical
    dv = haversine(lonmin, minlonpair, lonmax, maxlonpair)
    print("dv",dv)
# %%
