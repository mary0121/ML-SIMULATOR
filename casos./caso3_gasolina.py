#%%

from doepy import build, read_write
import pandas as pd
import numpy as np
import random


d =  {
    'Wind speed':[3,10],
    'Cloud cover':[0,10],
    'Air themperature':[18,35],
    'Humidity':[77,87],
    'Puddle Diameter': [0,100],
    'Puddle volume': [0,1000]
}


x = build.build_lhs(d, num_samples=300)
print(len(x))

### transform data

x['Cloud cover'] = x['Cloud cover'].round(decimals = 0)
x['Wind speed'] = x['Wind speed'].round(decimals = 0)
x['Air themperature'] = x['Air themperature'].round(decimals = 0)
x['Humidity'] = x['Humidity'].round(decimals = 0)

### fill static or string columns

chemical = ['']*len(x)
mesurementHeigth = [0]*len(x)
windIsFrom = ['']*len(x)
building = ['']*len(x)
groundRoughtness = ['']*len(x)
buildingSurr = ['']*len(x)
initialpuddletem = ['']*len(x)
puddleType = ['']*len(x)


for i in range(len(x)):
    chemical[i] = 'N-Octane'
    mesurementHeigth[i] = 3
    windIsFrom[i] = random.choice(['NE', 'NNE', 'ENE', 'ESE'])
    building[i] = random.choice(['Enclosed office', 'Single office', 'Double storied'])
    groundRoughtness[i] = random.choice(['Urban or forest', 'open country'])
    initialpuddletem[i] = x['Air themperature'][i]
    puddleType[i] = 'Burning Puddle (poolfire)'
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
x['Building surrounding'] = buildingSurr
x['Initial Puddle Temperature'] = initialpuddletem

print(x)


read_write.write_csv(x,'AlohaDB3Gasolina')



# %%
