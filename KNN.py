#%%

## Primero importamos las librerías necesarias.

from copyreg import pickle
from tokenize import Double
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt
import pickle
import json
from matplotlib.patches import Ellipse
from math import *
from haversine import inverse_haversine, Direction
#%%

# Se definen las funciones a utilizar. CleanData sirve para el preprocesamiento del archivo, 
# csv, al igual que generateDummies. La función ellipse se utiliza para generar una lista de 
# puntos alrededor de la elipse definida con las distancias verticales y horizontales prefichas.
# La función angle_between sirve para encontrar el ángulo entre el origen y un punto para
# posteriormente convertir las coordenadas del punto en latitud y longitud.

def CleanData(table):
    table.pop('Y complement')
    table.pop('R complement')
    table.pop('O complement')
    sameColumns = table.loc[:,[(table[col] == table[col][0]).all() for col in table.columns]]
    for i in range(len(sameColumns.columns)):
        table.pop(sameColumns.columns[i])
    table = table.drop(range(190,len(table)))
    return table

def generateDummies(table) :
    dummieColumns = table.loc[:,(table.dtypes == 'object').values]
    for i in range(len(dummieColumns.columns)):
        dummieEncode = pd.get_dummies(table[dummieColumns.columns[i]], prefix='x')
        table.pop(dummieColumns.columns[i])
        table = table.join(dummieEncode)
    return table

def ellipse(width, height):

    ellipse = Ellipse(xy=(0, 0), width=width, height=height, 
                            edgecolor="r", fc="None", lw=2)
    plt.xlim([-(width + width/3), (width + width/3)])
    plt.ylim([-(width + width/3), (width + width/3)])
    plt.gca().add_patch(ellipse)
    p = []
    xmax = width/2
    x = 0
    interval = 0.002
    range = np.arange(0.0, xmax, interval)
    print(range)
    ## puntos lado derecho

    for x in range:
        y = (height/2)*pow((1-((x**2)/(width/2)**2)),0.5)
        p.append([x,y])
    for x in np.arange(len(p)-2,-1,-1):
        p.append([p[x][0],-p[x][1]])

    ## puntos lado izquierdo

    for x in np.arange(len(p)-2,0,-1):
        p.append([-p[x][0],p[x][1]])

    ## plot puntos
    for x in np.arange(0,len(p),1):
        plt.plot(p[x][0], p[x][1], marker="o", markersize=5, markeredgecolor="red", markerfacecolor="green")
    
    return p

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))

#%%

# -------------- KNN MODEL ----------------

# Load database
data = pd.read_csv('Piscina_metanol.csv')
data = CleanData(data)
data = generateDummies(data) 

X = data.drop([
    'red distance (km)', 
    'yellow distance', 
    'orange distance', 
    'Red Vertical distane',
    'Orange Vertical distane',
    'Yellow Vertical distane',
    'Red Horizontal distane',
    'Orange Horizontal distane',
    'Yellow Horizontal distane',
    'Origin'
], axis=1)
y1 = data['Red Vertical distane']
y2 = data['Orange Vertical distane']
y3 = data['Yellow Vertical distane']
y4 = data['Red Horizontal distane']
y5 = data['Orange Horizontal distane']
y6 = data['Yellow Horizontal distane']

y =np.stack((y1, y2, y3, y4, y5, y6), axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, )
knn_model = KNeighborsRegressor(n_neighbors=3)
knn_model.fit(X_train, y_train)

test_preds = knn_model.predict(X_test)
mse = mean_squared_error(y_test, test_preds)
rmse = sqrt(mse)
errors = abs(test_preds - y_test)
# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / y_test)
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
# save the model to disk
filename = 'finalized_model.pkl'
pickle.dump(knn_model, open(filename, 'wb'))

### json model
""" model_param = {}
model_param['coef'] = list(knn_model.)
print(model_param['coef']) """
# %%
import sys
import os

# open pickle file
with open(sys.argv[1], 'rb') as infile:
    obj = pickle.load(infile)

# convert pickle object to json object
json_obj = json.loads(json.dumps(obj, default=str))

# write the json file
with open(
        os.path.splitext(sys.argv[1])[0] + '.json',
        'w',
        encoding='utf-8'
    ) as outfile:
    json.dump(json_obj, outfile, ensure_ascii=False, indent=4)



#%%
# some time later...
# load the model from disk

###Variables
lat = 11.033333
lon = -74.816667
wind_speed = 7
cloud_cover = 6
Air_temp = 19
Humidity = 80
puddle_diameter = 38.15
puddle_volume = 415.3
Initial_puddle_Temp = 19

ENE = 1
ESE = 0
NE = 0
NNE = 0
Urban_or_forest = 1
Open_country = 0
Double_storied = 0
Enclosed_office = 0
Single_office = 1
Sheltered = 0
UnSheltered = 1

test = [
    wind_speed, 
    cloud_cover, 
    Air_temp, 
    Humidity, 
    puddle_diameter, 
    puddle_volume,
    Initial_puddle_Temp,
    ENE,
    ESE,
    NE,
    NNE,
    Urban_or_forest,
    Open_country,
    Double_storied,
    Enclosed_office,
    Single_office,
    Sheltered,
    UnSheltered
]

loaded_model = pickle.load(open(filename, 'rb'))
prediction = loaded_model.predict([test])
##red
puntosRed = ellipse(prediction[0][3], prediction[0][3])
coordsRed = []
for x in np.arange(0,len(puntosRed),1):
    sum = (0-puntosRed[x][0])**2 + (0-puntosRed[x][1])**2
    print(sum)
    dst = pow(sum, 0.5)
    print(dst)
    ang = angle_between((0,0), (puntosRed[x][0],puntosRed[x][1]))
    print(ang)
    p = inverse_haversine((lat,lon), dst, ang * (pi/180))
    coordsRed.append(p)

puntosOrange = ellipse(prediction[0][4], prediction[0][4])
coordsOrange = []
for x in np.arange(0,len(puntosOrange),1):
    sum = (0-puntosOrange[x][0])**2 + (0-puntosOrange[x][1])**2
    print(sum)
    dst = pow(sum, 0.5)
    print(dst)
    ang = angle_between((0,0), (puntosOrange[x][0],puntosOrange[x][1]))
    print(ang)
    p = inverse_haversine((lat,lon), dst, ang * (pi/180))
    coordsOrange.append(p)

puntosYellow = ellipse(prediction[0][5], prediction[0][5])
coordsYellow = []
for x in np.arange(0,len(puntosYellow),1):
    sum = (0-puntosYellow[x][0])**2 + (0-puntosYellow[x][1])**2
    print(sum)
    dst = pow(sum, 0.5)
    print(dst)
    ang = angle_between((0,0), (puntosYellow[x][0],puntosYellow[x][1]))
    print(ang)
    p = inverse_haversine((lat,lon), dst, ang * (pi/180))
    coordsYellow.append(p)



# %%
from fastkml import kml

RedCoord = ''
for x in np.arange(0,len(coordsRed),1):
    RedCoord = RedCoord+str(coordsRed[x][1])+','+str(coordsRed[x][0])+' '
RedCoord = RedCoord+str(coordsRed[0][1])+','+str(coordsRed[0][0])+' '

OrangeCoord = ''
for x in np.arange(0,len(coordsOrange),1):
    OrangeCoord = OrangeCoord+str(coordsOrange[x][1])+','+str(coordsOrange[x][0])+' '
OrangeCoord = OrangeCoord+str(coordsOrange[0][1])+','+str(coordsOrange[0][0])+' '

YellowCoord = ''
for x in np.arange(0,len(coordsYellow),1):
    YellowCoord = YellowCoord+str(coordsYellow[x][1])+','+str(coordsYellow[x][0])+' '
YellowCoord = YellowCoord+str(coordsYellow[0][1])+','+str(coordsYellow[0][0])+' '

## Create KML
lat = str(lat)
lon = str(lon)
kml_str = f"""<?xml version="1.0" encoding="utf-8" ?>
          <kml xmlns="http://www.opengis.net/kml/2.2">
            <Document> 
                <Folder> 
                    <name>Aloha Threat Zones</name>
                    <Placemark>
                        <name>Yellow Threat Zone</name>
                        <ExtendedData><Data name="MarplotID"><value>AAAAAAAAAAAAAA01</value></Data></ExtendedData>
                        <description><![CDATA[<b>Time:</b> August 6, 2022  2127 hours ST<br><b>Chemical Name:</b> METHANOL<br><b>Wind:</b> 7 meters/second from NNE at 3 meters<br><small><br></small><b>THREAT ZONE:</b><br><span style="background-color: rgb(255, 0, 0);">&nbsp;&nbsp;&nbsp;&nbsp;</span>&nbsp;Red   : 81 meters --- (10.0 kW/(sq m) = potentially lethal within 60 sec)<br><span style="background-color: rgb(255, 153, 0);">&nbsp;&nbsp;&nbsp;&nbsp;</span>&nbsp;Orange: 96 meters --- (5.0 kW/(sq m) = 2nd degree burns within 60 sec)<br><span style="background-color: rgb(255, 255, 0);">&nbsp;&nbsp;&nbsp;&nbsp;</span>&nbsp;Yellow: 125 meters --- (2.0 kW/(sq m) = pain within 60 sec)<br><br><br>Model: ALOHA Thermal radiation from pool fire<br>]]></description>
                        <drawOrder>1</drawOrder><Polygon><gx:drawOrder>1</gx:drawOrder><outerBoundaryIs><LinearRing><coordinates> {YellowCoord} </coordinates></LinearRing></outerBoundaryIs></Polygon>
                        <Style><LineStyle><color>00ffffff</color><width>3</width></LineStyle>  <PolyStyle><fill>1</fill><color>5535edff</color></PolyStyle></Style>
                    </Placemark> 
                    <Placemark>
                        <name>Orange Threat Zone</name>
                        <ExtendedData><Data name="MarplotID"><value>AAAAAAAAAAAAAA01</value></Data></ExtendedData>
                        <description><![CDATA[<b>Time:</b> August 6, 2022  2127 hours ST<br><b>Chemical Name:</b> METHANOL<br><b>Wind:</b> 7 meters/second from NNE at 3 meters<br><small><br></small><b>THREAT ZONE:</b><br><span style="background-color: rgb(255, 0, 0);">&nbsp;&nbsp;&nbsp;&nbsp;</span>&nbsp;Red   : 81 meters --- (10.0 kW/(sq m) = potentially lethal within 60 sec)<br><span style="background-color: rgb(255, 153, 0);">&nbsp;&nbsp;&nbsp;&nbsp;</span>&nbsp;Orange: 96 meters --- (5.0 kW/(sq m) = 2nd degree burns within 60 sec)<br><span style="background-color: rgb(255, 255, 0);">&nbsp;&nbsp;&nbsp;&nbsp;</span>&nbsp;Yellow: 125 meters --- (2.0 kW/(sq m) = pain within 60 sec)<br><br><br>Model: ALOHA Thermal radiation from pool fire<br>]]></description>
                        <drawOrder>1</drawOrder><Polygon><gx:drawOrder>1</gx:drawOrder><outerBoundaryIs><LinearRing><coordinates> {OrangeCoord} </coordinates></LinearRing></outerBoundaryIs></Polygon>
                        <Style><LineStyle><color>00ffffff</color><width>3</width></LineStyle>  <PolyStyle><fill>1</fill><color>55359aff</color></PolyStyle></Style>
                    </Placemark>
                    <Placemark>
                        <name>Red Threat Zone 10.0 kW/(sq m) = potentially lethal within 60 sec</name>
                        <ExtendedData><Data name="MarplotID"><value>AAAAAAAAAAAAAA03</value></Data></ExtendedData>
                        <description><![CDATA[<b>Time:</b> August 6, 2022  2147 hours ST<br><b>Chemical Name:</b> METHANOL<br><b>Wind:</b> 7 meters/second from ENE at 3 meters<br><small><br></small><b>THREAT ZONE:</b><br><span style="background-color: rgb(255, 0, 0);">&nbsp;&nbsp;&nbsp;&nbsp;</span>&nbsp;Red   : 36 meters --- (10.0 kW/(sq m) = potentially lethal within 60 sec)<br><span style="background-color: rgb(255, 153, 0);">&nbsp;&nbsp;&nbsp;&nbsp;</span>&nbsp;Orange: 43 meters --- (5.0 kW/(sq m) = 2nd degree burns within 60 sec)<br><span style="background-color: rgb(255, 255, 0);">&nbsp;&nbsp;&nbsp;&nbsp;</span>&nbsp;Yellow: 55 meters --- (2.0 kW/(sq m) = pain within 60 sec)<br><br><br>Model: ALOHA Thermal radiation from pool fire<br>]]></description>
                        <drawOrder>3</drawOrder><Polygon><gx:drawOrder>3</gx:drawOrder><outerBoundaryIs><LinearRing><coordinates>{RedCoord}</coordinates></LinearRing></outerBoundaryIs></Polygon>
                        <Style><LineStyle><color>00ffffff</color><width>3</width></LineStyle>  <PolyStyle><fill>1</fill><color>551717ff</color></PolyStyle></Style>
                    </Placemark>
                </Folder>
            </Document>
          </kml>"""


f = open("myTest2.kml", "a")
f.write(kml_str)
f.close()
# %%
