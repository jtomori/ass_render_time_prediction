import matplotlib.pyplot as plt
import numpy as np
import random as pyran
import sklearn.linear_model
import sklearn.datasets
import tensorflow as tf

samples = np.arange(0.1, 500.0, 1.0)
seconds_plus_bias = samples ** 1.3 + np.random.rand(*samples.shape) * 500
test_block = np.random.randint( size=(20), low=5, high=495)
samples_test, seconds_test = [], []
seconds_train, samples_training = [], []

for n in range(500):
	if n in test_block:
		samples_test.append(samples[n])
		seconds_test.append(seconds_plus_bias[n])
	else:
		samples_training.append(samples[n])
		seconds_train.append(seconds_plus_bias[n])

X_samples = np.c_[samples_training]
y_seconds = np.c_[seconds_train]
model = sklearn.linear_model.LinearRegression()
model.fit(X_samples,y_seconds)
print (model.score(X_samples, y_seconds))

seconds_prediction = []
for t in samples_test:
	seconds_prediction.append(model.predict([[t]]))

#show train data
plt.scatter(samples_training, seconds_train, c="b")
#show test data
plt.scatter(samples_test, seconds_test, c="g")
#show prediciton data
plt.scatter(samples_test, seconds_prediction, c="r")

plt.xlabel("sam")
plt.ylabel("sec")


X = tf.constant(X_samples, dtype=tf.float32, name="X")
y = tf.constant(y_seconds, dtype=tf.float32, name="y")
XT = tf.transpose(X)
theta = tf.matmul(tf.matmul(tf.matrix_inverse(tf.matmul(XT, X)), XT), y)
with tf.Session() as sess:
	theta_value = theta.eval()
	print ("Tf theta", theta_value)
	print ("sklearn theta", model.coef_)

plt.savefig('./res.png')
plt.show()
