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
    'Lenght': [20,60],
    'Diameter': [9,27],
    'Lenght': [0.665,1,8],
    'Percentage Mass in Fireball': [1,100],
    'Liquid Volume':[10,100],
}


x = build.build_lhs(d, num_samples=300)
print(len(x))

### transform data

x['Cloud cover'] = x['Cloud cover'].round(decimals = 0)
x['Wind speed'] = x['Wind speed'].round(decimals = 0)
x['Air themperature'] = x['Air themperature'].round(decimals = 0)
x['Humidity'] = x['Humidity'].round(decimals = 0)
x['Lenght'] = x['Lenght'].round(decimals = 2)

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

for i in range(len(x)):
    chemical[i] = 'Benzene'
    mesurementHeigth[i] = 3
    windIsFrom[i] = random.choice(['NE', 'NNE', 'ENE', 'ESE'])
    building[i] = random.choice(['Enclosed office', 'Single office', 'Double storied'])
    groundRoughtness[i] = random.choice(['Urban or forest', 'open country'])
    tankType[i] = 'Vertical'
    typeTankFailure[i] = 'BLEVE'
    tempTank[i] = random.uniform(x['Air themperature'][i], x['Air themperature'][i]+5)
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

print(x)

### one-hot encoding implementation

#y = pd.get_dummies(x.Building, prefix='test', columns=2)
#print(y)

## save data

read_write.write_csv(x,'AlohaDB1Benzene')
# %%
