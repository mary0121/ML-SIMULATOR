#%%
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt

#%%

def CleanData(table):
    table.pop('Y complement')
    table.pop('R complement')
    table.pop('O complement')
    table.drop('orange distance', axis = 1)
    table.drop('red distance (km)', axis = 1)

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

def pearsonCorr(table) :
    corr_matrix = table.corr(method='pearson')
    corr_matrix.style.background_gradient(cmap='coolwarm').set_precision(2)

#%%

# -------------- MULTILAYER PERCEPTRON MODEL ----------------

# Load database
data = pd.read_csv('derrame_cloro.csv')

#data conditioning
data = CleanData(data)
data = generateDummies(data)  

# Creating labelEncoder
lab = preprocessing.LabelEncoder()
##data['yellow distance'] = lab.fit_transform(data['yellow distance'])
##print(data['yellow distance'])

# Spliting data into Feature and labels
y = np.array(data['yellow distance'])
X = data.drop('yellow distance', axis = 1)

# Split dataset into training set and test set
train_features, test_features, train_labels, test_labels = train_test_split(X, y, test_size=0.2,)

#MLP PARAMETERS
layers = 1
neuroms = 3
activation = 'relu'
solver = 'lbfgs'

rmse = []
for i in range (neuroms, 11):
    # Create model object
    mlp = MLPRegressor( hidden_layer_sizes= (layers,i), activation= activation, solver = solver )
    # Fit data into the model
    mlp.fit(train_features,train_labels)
    # Make prediction on test dataset
    ypred = mlp.predict(test_features)
    # rmse
    mse = mean_squared_error(ypred, test_labels)
    rmse.append(sqrt( mse))

print(rmse)
plt.xlabel('Neuroms')
plt.ylabel('RMSE')
plt.plot(np.arange(neuroms,neuroms+10,1) ,rmse)


# %%

## best result

bestRMSE = rmse[0]
for x in range(1,len(rmse)):
    if rmse[x] < bestRMSE:
        bestRMSE=rmse[x]

index = rmse.index(bestRMSE) + 1
print(index)

mlp = MLPRegressor( hidden_layer_sizes= (1,index), solver = 'lbfgs')
    # Fit data into the model
mlp.fit(train_features,train_labels)
    # Make prediction on test dataset
ypred = mlp.predict(test_features)
plt.plot( test_labels, 'b-', label = 'actual')
# Plot the predicted values
plt.plot( ypred, 'ro', label = 'prediction')
plt.xticks(rotation = '60'); 
plt.legend()
# %%
