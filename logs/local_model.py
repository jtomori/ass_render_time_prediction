from __future__ import absolute_import, division, print_function

import pathlib
import pandas as pd
import seaborn as sns
import tensorflow as tf
print(tf.__version__)
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

column_names = ['/render/frame time/rendering/microseconds','ar_GI_diffuse_depth','ar_AA_samples','ar_GI_specular_samples','ar_GI_transmission_samples',
                'ar_GI_diffuse_samples', 'ar_GI_specular_depth', 'ar_bucket_size']


raw_dataset = pd.read_csv("output_data.csv", usecols=column_names, sep=",", skipinitialspace=True)

dataset = raw_dataset.copy()

dataset = dataset.astype("float64")

dataset.tail()

dataset.isnull().sum()


train_dataset = dataset.sample(frac=0.8,random_state=0)
test_dataset = dataset.drop(train_dataset.index)


sns.pairplot(train_dataset[column_names], diag_kind="kde")

train_stats = train_dataset.describe()
#print (column_names[0])
train_stats.pop("/render/frame time/rendering/microseconds")
train_stats = train_stats.transpose()
train_stats

#test_dataset.tail()
train_labels = train_dataset.pop("/render/frame time/rendering/microseconds")
test_labels = test_dataset.pop("/render/frame time/rendering/microseconds")
print (20*"#", train_labels)
def norm(x):
  return (x - train_stats['mean']) / train_stats['std']

normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)

def build_model():
  print (len(train_dataset.keys()))
  model =  keras.Sequential([
    layers.Dense(64, activation=tf.nn.relu, input_shape=[len(train_dataset.keys())]),
    layers.Dense(64, activation=tf.nn.relu),
    layers.Dense(1)
  ])

  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
  return model

model = build_model()
model.summary()


example_batch = normed_train_data[:10]
example_batch
example_result = model.predict(example_batch)


# Display training progress by printing a single dot for each completed epoch
class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

EPOCHS = 1000

history = model.fit(
  normed_train_data, train_labels,
  epochs=EPOCHS, validation_split = 0.2, verbose=0,
  callbacks=[PrintDot()])


hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
hist.tail()


def plot_history(history):
  hist = pd.DataFrame(history.history)
  hist['epoch'] = history.epoch
  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Abs Error [MPG]')
  plt.plot(hist['epoch'], hist['mean_absolute_error'],
           label='Train Error')
  plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
           label = 'Val Error')
  plt.legend()
  
  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Square Error [$MPG^2$]')
  plt.plot(hist['epoch'], hist['mean_squared_error'],
           label='Train Error')
  plt.plot(hist['epoch'], hist['val_mean_squared_error'],
           label = 'Val Error')
  plt.legend()
  plt.show()

plot_history(history)
