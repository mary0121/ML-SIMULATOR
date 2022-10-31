#%%

from doepy import build, read_write
import pandas as pd
import numpy as np
import random

d =  {
    'Wind speed':[3.7,6],
    'Cloud cover':[0,10],
    'Air themperature':[18,35],
    'Humidity':[77,87],
    'Liquid Volume':[0,95],
    'Opening diameter (inches)': [6,24],
    'Bottom of the leak': [0,100],
    'Max avg release time (g)': [700,8800] 
}

x = build.build_lhs(d, num_samples=300)
print(len(x))

### transform data

x['Cloud cover'] = x['Cloud cover'].round(decimals = 0)
x['Wind speed'] = x['Wind speed'].round(decimals = 0)
x['Air themperature'] = x['Air themperature'].round(decimals = 0)
x['Humidity'] = x['Humidity'].round(decimals = 0)


#x['Building surrounding']
### fill static or string columns

chemical = ['']*len(x)
typeTankFailure = ['']*len(x)
mesurementHeigth = [0]*len(x)
windIsFrom = ['']*len(x)
building = ['']*len(x)
groundRoughtness = ['']*len(x)
tankType = ['']*len(x)
buildingSurr = ['']*len(x)
tempTank = ['']*len(x)
openingShape = ['']*len(x)
holeOrShort = ['']*len(x)
groundtype = ['']*len(x)
Inputgroundtempeture = ['']*len(x)
InputmaxPuddle = ['']*len(x)
ReleaseTime = ['']*len(x)

for i in range(len(x)):
    chemical[i] = 'Benzene'
    openingShape[i] = 'Circular opening'
    holeOrShort[i] = 'hole'
    ReleaseTime[i] = '1 minuto'
    groundtype[i] = 'Concrete'
    InputmaxPuddle[i] = 'Unknown'
    mesurementHeigth[i] = 3
    windIsFrom[i] = random.choice(['NE', 'NNE', 'ENE', 'ESE'])
    building[i] = random.choice(['Enclosed office', 'Single office', 'Double storied'])
    groundRoughtness[i] = random.choice(['Urban or forest', 'open country'])
    tankType[i] = 'Horizontal'
    typeTankFailure[i] = 'Leaking Tank, not burning'
    tempTank[i] = x['Air themperature'][i]
    if building[i] == 'Enclosed office':
        buildingSurr[i] = 'NA'
    else:
        buildingSurr[i] = random.choice(['Sheltered', 'Unsheltered'])

x['Chemical'] = chemical
x['Mesurement Heigth'] = mesurementHeigth
x['Wind is from'] = windIsFrom
x['Chemical state'] = chemical
x['Building'] = building
x['Ground roughtness'] = groundRoughtness
x['Tank type'] = tankType
x['Building surrounding'] = buildingSurr
x['Temperature within tank'] = tempTank
x['Input maximum puddle dm or area'] = InputmaxPuddle
x['Release time'] = ReleaseTime

print(x)

### one-hot encoding implementation

#y = pd.get_dummies(x.Building, prefix='test', columns=2)
#print(y)

## save data

read_write.write_csv(x,'AlohaDB1Propane')
# %%
