# -*- coding: utf-8 -*-
"""Stock Price Prediction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eaiN5Tn5xeChYbZld8U8LxYmaI8O4taw
"""

#importing libraries

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")

dataset = pd.read_csv("MARUTI3.csv", index_col='Date', parse_dates=["Date"]) 
dataset.head(5)

"""# New Section"""

# to know the shape of the data set
dataset.shape

# spliting the values train and test dataset for analysing the the given data
train_cols = ["Open","High","Low","Close","VWAP","Volume"]
train = dataset[:'2017'].loc[:,train_cols].values
test = dataset['2018':].loc[:,train_cols].values
print(train.shape)
print(test.shape)
print(train[1],train[2],train[3])

# visualization of "VWAP" attribute of the dataset

dataset["VWAP"][:'2017'].plot(figsize=(16,4), legend=True)
dataset["VWAP"]["2018":].plot(figsize=(16,4), legend=True)
plt.legend(["Training set (before 2017)", "Test set (from 2017)"])
plt.title("MARUTI stock prices")
plt.show()

# importing other libraries

import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")

from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.optimizers import SGD

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

import math

# scaling the training set

sc = MinMaxScaler(feature_range=(0,1))
train_scaled = sc.fit_transform(train)

# Since LSTMs store long term memory state, we create a data structure with 80 timesteps and 1 output
# So for each element of training set, we have 80 previous training set elements

x_train = []
y_train = []

for i in range(80,3604):
    x_train.append(train_scaled[i-80:i, ])
    y_train.append(train_scaled[i,0])

x_train, y_train = np.array(x_train), np.array(y_train)

# reshaping x_train for efficient modelling

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# LSTM architecture

regressor = Sequential()

# add first layer with dropout

regressor.add(LSTM(units=100, return_sequences=True, input_shape=(x_train.shape[1],1)))
regressor.add(Dropout(0.2))

# add second layer

regressor.add(LSTM(units=80, return_sequences=True))
regressor.add(Dropout(0.2))

# add third layer

regressor.add(LSTM(units=60, return_sequences=True)) 
regressor.add(Dropout(0.2))

# add fourth layer

regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))

# the output layer

regressor.add(Dense(units=1))

# compiling the LSTM RNN network

regressor.compile(optimizer='rmsprop', loss='mean_squared_error')

# fit to the training set

history=regressor.fit(x_train, y_train, epochs=40, batch_size=32)

# Now to get the test set ready in a similar way as the training set.
# The following has been done so first 80 entries of test set have 80 previous values which is impossible to get unless we take the whole 'VWAP' attribute data for processing

dataset_total = pd.concat((dataset[:'2017'].loc[:,train_cols], dataset['2018':].loc[:,train_cols]), axis=0)
print(dataset_total.shape)

inputs = dataset_total[len(dataset_total)-len(test)-80 : ].values
print(inputs.shape)
inputs = inputs.reshape(-1,1)
print(inputs.shape)
inputs = sc.transform(inputs)
print(inputs.shape)

# preparing x_test

x_test = []
for i in range(80,701):
    x_test.append(inputs[i-80:i, 0])
    
x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
x_test

# predicting the stock prices for test set

predicted = regressor.predict(x_test)
predicted = sc.inverse_transform(predicted)

# function which plots MARUTI stock prices: real and predicted both

def plot_predictions(test, predicted):
    plt.plot(test, color="red", label="real MARUTI stock price")
    plt.plot(predicted, color="blue", label="predicted stock price")
    plt.title("MARUTI stock price prediction")
    plt.xlabel("time")
    plt.ylabel("MARUTI stock price")
    plt.legend()
    plt.show()

# visualizing the results: predicted vs test

plot_predictions(test, predicted)

def return_rmse(test, predicted):
    rmse = math.sqrt(mean_squared_error(test, predicted))
    print("the root mean squared error is : {}.".format(rmse))

# evaluating the model

y=return_rmse(test, predicted)
y