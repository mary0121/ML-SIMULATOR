#%%

from doepy import build, read_write
import pandas as pd
import numpy as np
import random
import math

d =  {
    'Wind speed':[3,6],
    'Cloud cover':[0,10],
    'Air themperature':[18,35],
    'Humidity':[77,87],
    'Lenght': [0.665,1,8],
    'Diameter': [0.25,0.35],
    'Liquid Volume':[10,100],
    'Bottom of the leak': [0,100]
}

print("Caso 1: Fuga de tanque de cloro")

x = build.build_lhs(d, num_samples=300)

### transform data

x['Cloud cover'] = x['Cloud cover'].round(decimals = 0)
x['Wind speed'] = x['Wind speed'].round(decimals = 0)
x['Air themperature'] = x['Air themperature'].round(decimals = 0)
x['Humidity'] = x['Humidity'].round(decimals = 0)
x['Lenght'] = x['Lenght'].round(decimals = 2)
x['Diameter'] = x['Diameter'].round(decimals = 2)
x['Liquid Volume'] = x['Liquid Volume'].round(decimals = 0)
x['Bottom of the leak'] = x['Bottom of the leak'].round(decimals = 0)

### fill static or string columns

mesurementHeigth = [0]*len(x)
windIsFrom = ['']*len(x)
chemicalState = ['']*len(x)
tankType = ['']*len(x)
building = ['']*len(x)
groundRoughtness = ['']*len(x)
holeOrValve = ['']*len(x)
shapeArea = ['']*len(x)
buildingSurr = ['']*len(x)

for i in range(len(x)):
    mesurementHeigth[i] = 3
    windIsFrom[i] = 'NE'
    chemicalState[i] = 'Liquid'
    tankType[i] = 'Horizontal Cylinder'
    building[i] = random.choice(['Enclosed office', 'Single storied', 'Double storied'])
    groundRoughtness[i] = random.choice(['Urban or forest', 'open country'])
    holeOrValve[i] = random.choice(['hole', 'valve'])
    shapeArea[i] = random.uniform(1.0, (math.pi*(x['Diameter'][i]/2)**2))
    if building[i] == 'Enclosed office':
        buildingSurr[i] = 'NA'
    else:
        buildingSurr[i] = random.choice(['Sheltered', 'Unsheltered'])

x['Mesurement Heigth'] = mesurementHeigth
x['Wind is from'] = windIsFrom
x['Chemical state'] = chemicalState
x['Tank type'] = tankType
x['Building'] = building
x['Ground roughtness'] = groundRoughtness
x['Hole or Valve'] = holeOrValve
x['Shape area'] = shapeArea
x['Building surrounding'] = buildingSurr

read_write.write_csv(x,'AlohaDB')
# %%
