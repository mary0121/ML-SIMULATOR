from doepy import build, read_write
import pandas as pd
import numpy as np
import random
import math

d =  {
    ##'Building': ['Enclosed office', 'Enclosed office', 'Double storied'],
    'Wind speed':[3,6],
    ##'Wind is from':['NE'],
    ##'Mesurement height':[3],
    ##'Ground roughtness':['Urban or forest', 'open country'],
    'Cloud cover':[0,10],
    'Air themperature':[18,35],
    'Humidity':[77,100],
    ##'Tank type':['Horizontal Cylinder'],
    'Lenght': [20,60],
    'Diameter': [9,27],
    ##'Chemical state': ['Liquid'],
    'Liquid Volume':[0,100],
    #'Shape area':[1,0],
    ##'Hole or Valve': ['hole', 'valve'],
    'Bottom of the leak': [0,100]
}


x = build.build_lhs(d, num_samples=300)
print(len(x))

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
tempTank = ['']*len(x)
openingShape = ['']*len(x)
chemical = ['']*len(x)
tankFailure = ['']*len(x)
maxArea = ['']*len(x)
dowrinndDisp = ['']*len(x)

for i in range(len(x)):
    chemical[i] = 'N-Octane'
    tankFailure[i] = 'Leaking tank. burning'
    mesurementHeigth[i] = 3
    maxArea[i] = 'Unknown'
    dowrinndDisp[i] = 'Heavy Gas'
    windIsFrom[i] = random.choice(['NE', 'NNE', 'ENE', 'ESE'])
    openingShape[i] = random.choice(['Circular', 'Rectangular'])
    chemicalState[i] = 'Liquid'
    tankType[i] = 'vertical Cylinder'
    building[i] = random.choice(['Enclosed office', 'Single storied', 'Double storied'])
    groundRoughtness[i] = random.choice(['Urban or forest', 'open country'])
    holeOrValve[i] = 'hole'
    tempTank[i] = x['Air themperature'][i]
    shapeArea[i] = random.uniform(1.0, (math.pi*(x['Diameter'][i]/2)**2))##
    if building[i] == 'Enclosed office':
        buildingSurr[i] = 'NA'
    else:
        buildingSurr[i] = random.choice(['Sheltered', 'Unsheltered'])

x['Chemical'] = chemical
x['Mesurement Heigth'] = mesurementHeigth
x['Wind is from'] = windIsFrom
x['Chemical state'] = chemicalState
x['Tank type'] = tankType
x['Building'] = building
x['Ground roughtness'] = groundRoughtness
x['Hole or Valve'] = holeOrValve
x['Shape area'] = shapeArea
x['Building surrounding'] = buildingSurr
x['Temperature within tank'] = tempTank
x['Opening Shape'] = openingShape
x['Type of tank failure'] = tankFailure
x['Maximun puddle'] = maxArea
x['Dowrinnd Dispersion'] = dowrinndDisp


print(x)

read_write.write_csv(x,'AlohaDB2Gasolina')