#%%

from doepy import build, read_write
import pandas as pd
import numpy as np
import random

#%%

d =  {

    ##'Building': ['Enclosed office', 'Enclosed office', 'Double storied'],
    'Wind speed':[3,6],
    ##'Wind is from':['NE'],
    ##'Mesurement height':[3],
    ##'Ground roughtness':['Urban or forest', 'open country'],
    'Cloud cover':[0,10],
    'Air themperature':[18,35],
    'Humidity':[77,87],
    #'Source': ['Instantaneous', 'Continue'],
    #'Amount pollutant entering the atmospher': [],
    'Duration (For)': [1,60],
    'Lenght': [0.665,1,8],
}


x = build.build_lhs(d, num_samples=300)
print(len(x))

### transform data

x['Cloud cover'] = x['Cloud cover'].round(decimals = 0)
x['Wind speed'] = x['Wind speed'].round(decimals = 0)
x['Air themperature'] = x['Air themperature'].round(decimals = 0)
x['Humidity'] = x['Humidity'].round(decimals = 0)
x['Lenght'] = x['Lenght'].round(decimals = 2)
x['Duration (For)'] = x['Duration (For)'].round(decimals = 0)
#x['Building surrounding']
### fill static or string columns

chemical = ['']*len(x)
mesurementHeigth = [0]*len(x)
windIsFrom = ['']*len(x)
building = ['']*len(x)
groundRoughtness = ['']*len(x)
source = ['']*len(x)
amountPollutant = [0]*len(x)
buildingSurr = ['']*len(x)

for i in range(len(x)):
    chemical[i] = 'Chlorine'
    mesurementHeigth[i] = 3
    windIsFrom[i] = 'NE'
    building[i] = random.choice(['Enclosed office', 'Single office', 'Double storied'])
    groundRoughtness[i] = random.choice(['Urban or forest', 'open country'])
    source[i] = random.choice(['Instantaneous', 'Continue'])
    if source[i] == 'Instantaneous':
        x['Duration (For)'][i] = 0
        amountPollutant[i] = random.choice([1000,68])
    else:
        amountPollutant[i] = random.choice([1000,68])/x['Duration (For)'][i]

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
x['Source'] = source
x['Amount pollutant entering the atmospher'] = amountPollutant
x['Amount pollutant entering the atmospher'] = x['Amount pollutant entering the atmospher'].round(decimals = 2)
x['Building surrounding'] = buildingSurr
print(x)

### one-hot encoding implementation

#y = pd.get_dummies(x.Building, prefix='test', columns=2)
#print(y)

## save data

read_write.write_csv(x,'AlohaDB2')
# %%

def histogram_intersection(a, b):
    v = np.minimum(a, b).sum().round(decimals=1)
    return v
df = pd.DataFrame([(.2, .3), (.0, .6), (.6, .0), (.2, .1)],
                  columns=['dogs', 'cats'])
df.corr(method=histogram_intersection)

# %%
