
from __future__ import absolute_import, division, print_function
import pathlib
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import os
import glob

EPOCHS = 1000


class PrintDot(keras.callbacks.Callback):
	def on_epoch_end(self, epoch, logs):
		if epoch % 100 == 0: print('')
		print('.', end='')

def norm(train_stats, x):
	return (x - train_stats['mean']) / train_stats['std']

def load_data(path_dir = "../datasets/dataset_a.csv", *args):
	column_names = ['/render/frame time/rendering/microseconds','ar_GI_diffuse_depth','ar_AA_samples',
									'ar_GI_specular_samples', 'ar_GI_diffuse_samples', "res_overridex", "res_overridey"]

	raw_dataset = pd.read_csv("../datasets/dataset_a.csv", usecols=column_names, sep=",", skipinitialspace=True)
	dataset = raw_dataset.copy()
	dataset = dataset.astype("float64")
	dataset.tail()

	dataset.isna().sum()

	dataset["ar_AA_samples"] = dataset["ar_AA_samples"]**2
	dataset["ar_GI_diffuse_samples"] = dataset["ar_GI_diffuse_samples"]**2
	dataset["ar_GI_specular_samples"] = dataset["ar_GI_specular_samples"]**2
	dataset["pixels"] = dataset["res_overridey"] * dataset["res_overridex"]
	dataset["render_seconds"] = dataset["/render/frame time/rendering/microseconds"]/(10**6)

	dataset = dataset.drop(columns=["res_overridey", "res_overridex", "/render/frame time/rendering/microseconds"])
	dataset.tail()

	dataset["render_seconds"] = np.log(dataset["render_seconds"])
	dataset.tail()
	return dataset

def load_train_data(dataset, *args):
	train_dataset = dataset.sample(frac=0.8,random_state=0)
	test_dataset_index = train_dataset.index
	train_stats = train_dataset.describe()
	train_stats.pop("render_seconds")
	train_stats = train_stats.transpose()
	train_labels = train_dataset.pop("render_seconds")
	normed_train_data = norm(train_stats, train_dataset)
	normed_train_data.tail()
	return (train_dataset, train_stats, train_labels, normed_train_data, test_dataset_index)

def load_test_data(dataset, index, train_stats, *args):
	test_dataset = dataset.drop(index)
	test_labels = test_dataset.pop("render_seconds")
	normed_test_data = norm(train_stats, test_dataset)
	return (normed_test_data, test_labels)

def create_model(train_dataset, summary = False, *args):
	print ("building model")
	model = keras.Sequential([
	tf.keras.layers.Dense(64, activation=tf.nn.relu, input_shape=[len(train_dataset.keys())]),
	tf.keras.layers.Dense(64, activation=tf.nn.relu),
	tf.keras.layers.Dense(1)
	])

	optimizer = tf.keras.optimizers.RMSprop(0.001)

	model.compile(loss='mse',
				optimizer=optimizer,
				metrics=['mae', 'mse'])
	if summary:
		model.summary()
	return model

def predict_from_ckp(model, checkpoint, normed_test_data, test_labels, *args):
	print ("load checkpoint from {0}".format(checkpoint))
	#load latest checkpoint weights
	model.load_weights(checkpoint)
	#evaluate
	loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=0)
	#predict
	predictions = predict(model, normed_test_data)
	#plot
	plot_data(test_labels, predictions)

def plot_data(test_labels, test_predictions, *args):
	plt.scatter(test_labels, test_predictions)
	plt.xlabel('True Values [seconds]')
	plt.ylabel('Predictions [seconds]')
	plt.axis('equal')
	plt.axis('square')
	plt.show()

def plot_history(history):
	hist = pd.DataFrame(history.history)
	hist['epoch'] = history.epoch
	plt.figure()
	plt.xlabel('Epoch')
	plt.ylabel('Mean Abs Error [render_seconds]')
	plt.plot(hist['epoch'], hist['mean_absolute_error'],
					 label='Train Error')
	plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
					 label = 'Val Error')
	plt.legend()
	#plt.ylim([0,5])

	plt.figure()
	plt.xlabel('Epoch')
	plt.ylabel('Mean Square Error [$render_seconds^2$]')
	plt.plot(hist['epoch'], hist['mean_squared_error'],
					 label='Train Error')
	plt.plot(hist['epoch'], hist['val_mean_squared_error'],
					 label = 'Val Error')
	plt.legend()
	#plt.ylim([0,20])
	plt.show()


def latest_checkpoint(checkpoint_dir):
	return tf.train.latest_checkpoint(checkpoint_dir)

def train(model, ckp_path, normed_train_data, train_labels, save_model = ""):
	print ("training {0}".format(ckp_path))
	early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=20)
	checkpoint_path = ckp_path + "/cp-{epoch:04d}.ckpt"
	checkpoint_dir = os.path.dirname(checkpoint_path)

	cp_callback = keras.callbacks.ModelCheckpoint(checkpoint_path, 
													 save_weights_only=True,
													 verbose=1,
													 period=20)
	history = model.fit(
		normed_train_data, train_labels,
		epochs=EPOCHS, validation_split = 0.2, verbose=0,
		callbacks=[early_stop, cp_callback])

	if save_model:
		save_model = model.save('{0}model.h5'.format(save_model))

	return history

def load_saved_model(model_path, summary=False):
	print ("loading Model from {0}".format(model_path))
	model = keras.models.load_model('{0}model.h5'.format(model_path))
	if summary:
		model.summary()
	return model

def predict(model, data, plot=False):
	predictions = model.predict(data).flatten()
	return predictions

def main(is_train=False, load_model=True):
	#checkpoint save path 
	ckp_path = "training/"
	#model save path
	model_path = "models/"
	#load data
	dataset = load_data()
	#load train set
	train_dataset, train_stats, train_labels, normed_train_data, test_dataset_index = load_train_data(dataset)
	#load test set		
	normed_test_data, test_labels = load_test_data(dataset, test_dataset_index, train_stats)

	#####LOAD SAVE MODEL
	if load_model:
		if not glob.glob(os.path.join(model_path,"*.h5")):
			print ("no existing model found in {0} !!!, creating model".format(model_path))
			#create model
			model = create_model(train_dataset)
		else:
			#load model from path
			model = load_saved_model(model_path)

	#####TRAIN
	if is_train:
		if latest_checkpoint(ckp_path):
			print ("existing ckeckpoints: {0}, set is_train flag to False to use them".format(ckp_path))
		#train
		history = train(model, ckp_path,normed_train_data, train_labels, model_path)
		plot_history(history)
		return

	#####PREDICT FROM CKP
	#load train checkpoints and predict
	if not latest_checkpoint(ckp_path):
		raise Exception("no existing ckeckpoint found in {0} !!!, set is_train flag to True to create and save them".format(ckp_path))

	predict_from_ckp(model, latest_checkpoint(ckp_path), normed_test_data, test_labels)
	return

main()