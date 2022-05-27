


from textwrap import indent
from Fundamentals import Fundamentals
import tensorflow as tf
keras = tf.keras
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import json

# class TrainForecastTimeSeries:

#     def __init__(self, fundamentals: Fundamentals) -> None:
#         self.fundamentals = fundamentals

#     def forecast(self) -> float:
        
#         return 0
    
# apiKey = 'IM95A052KPC7DLUE'

# def getConsumerSentiment(apiKey):
#     url = f'https://www.alphavantage.co/query?function=CONSUMER_SENTIMENT&apikey={apiKey}'
#     apiReturn = requests.get(url)
#     return apiReturn.json()

# data = getConsumerSentiment(apiKey=apiKey)

# jsonData = data['data']

# # open('consumerSentimentData.json', "w").close()

# with open('consumerSentimentData.json', 'w', encoding='utf-8') as f:
#     json.dump(jsonData, f, ensure_ascii=False, indent=4)

# with open('consumerSentimentData.json', encoding='utf-8') as inputFile:
#     df = pd.read_json(inputFile)

# df.to_csv('consumerSentimentData.csv', encoding='utf-8', index=False)

df = pd.read_csv('consumerSentimentData.csv')
series = df['value'].values
time = df['date'].values

def plotSeries(time, series, format="-", start=0, end=None, label=None):
    plt.plot(time[start:end], series[start:end], format, label=label)
    plt.xlabel("Time")
    plt.ylabel("Value")
    if label:
        plt.legend(fontsize=14)
    plt.grid(True)              

def createDatasetWindow(series, windowSize, batchSize=64, shuffleBuffer=1000):
    dataset = tf.data.Dataset.from_tensor_slices(series)
    dataset = dataset.window(windowSize + 1, shift=1, drop_remainder=True)
    dataset = dataset.flat_map(lambda window: window.batch(windowSize + 1))
    dataset = dataset.shuffle(shuffleBuffer)        
    dataset = dataset.map(lambda window: (window[:-1], window[-1]))
    dataset = dataset.batch(batchSize).prefetch(1)
    return dataset

splitTIme = 1000
trainTime = time[:splitTIme]
trainX = series[:splitTIme]
validationTime = time[splitTIme:]
validationX = series[splitTIme:]

tf.random.set_seed(42)
np.random.seed(42)

windowSize = 21
trainDataset = createDatasetWindow(trainX, windowSize)
validationDataset = createDatasetWindow(validationX, windowSize)

# Linear

# model = keras.models.Sequential([
#     keras.layers.Dense(1, input_shape=[windowSize])
# ])

# Dense

model = keras.models.Sequential([
  keras.layers.Dense(10, activation="relu", input_shape=[windowSize]),
  keras.layers.Dense(10, activation="relu"),
  keras.layers.Dense(1)
])

# learningRateScheduler = keras.callbacks.LearningRateScheduler(lambda epoch: 1e-6 * 10**(epoch / 30))

optimiser = keras.optimizers.SGD(learning_rate=8e-6, momentum=0.9)

# optimiser = keras.optimizers.SGD(learning_rate=6e-5, momentum=0.9)

model.compile(optimizer=optimiser, loss=keras.losses.Huber(), metrics=['mae'])

# history = model.fit(trainDataset, epochs=150, callbacks=[learningRateScheduler])

# plt.semilogx(history.history["lr"], history.history["loss"])
# plt.axis([1e-7, 5e-3, 0, 30])
# plt.show()

earlyStopping = keras.callbacks.EarlyStopping(patience=10)

model.fit(trainDataset, epochs=500, validation_data=validationDataset, callbacks=[earlyStopping])

def forecast(model, series, windowSize):
    dataset = tf.data.Dataset.from_tensor_slices(series)
    dataset = dataset.window(windowSize, shift=1, drop_remainder=True)
    dataset = dataset.flat_map(lambda w: w.batch(windowSize))
    dataset = dataset.batch(32).prefetch(1)
    forecast = model.predict(dataset)
    return forecast

# Linea forecast

# linearForecast = forecast(model, series[splitTIme-windowSize:-1], windowSize)[:, 0]
# linearForecast.shape

# plt.figure(figsize=(10, 6))
# plotSeries(validationTime, validationX)
# plotSeries(validationTime, linearForecast)
# plt.show()

# print(keras.metrics.mean_absolute_error(validationX, linearForecast).numpy())

# Dense forecast

denseForecast = forecast(model, series[splitTIme - windowSize:-1], windowSize)[:, 0]

plt.figure(figsize=(10, 6))
plotSeries(validationTime, validationX)
plotSeries(validationTime, denseForecast)
plt.show()

print(keras.metrics.mean_absolute_error(validationX, denseForecast).numpy())

# Save to .h5 

# t = time.time()
# kerasExportPath = "./{}.h5".format(int(t))
# model.save(kerasExportPath)

# # Load from .h5

# loaded = tf.keras.models.load_model(kerasExportPath)
