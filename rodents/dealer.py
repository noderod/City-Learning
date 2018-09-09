"""
BASICS

Uses keras neural network to compute the price of a car
Stores the model
"""


from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense, Dropout
import math
import numpy as np
import random
from scipy.stats import norm
import sys
import time



# fix random seed for reproducibility
seed = 7
np.random.seed(seed)



# Entire data
dataset = np.loadtxt("car_prices_numeric.csv", delimiter=",")
car_max_price = 21 # -1)*1000 $
D1 = []
for row in dataset:
	# 45 variables, where only one is true
	carval = int(row[3])
	bell_curve  = norm(carval, 0.125*carval)


	YVAL = car_max_price*[0]
	# Each value is the cdf of the bell curve 
	YVAL[carval] = 1

	D1.append([row[0], row[1], row[2], YVAL])


# 85% will be dedicated to testing and the 15% left, to verify the result
testdata = []
verifydata = []

for aset in D1:

	if random.random() < 0.85:
		testdata.append(aset)
		continue
	verifydata.append(aset)

# Splits testing into input (X) and output (Y) variables
X, Y = [], []
for row in testdata:
	X.append(row[:3])
	Y.append(row[3])


def relu_advanced(x):
    return K.relu(x, max_value=1)


# create model
model = Sequential()
model.add(Dense(6, input_dim=3, kernel_initializer ='uniform', activation='sigmoid'))
model.add(Dropout(0.5))
model.add(Dense(8, kernel_initializer ='uniform', activation='softmax'))
model.add(Dense(units=car_max_price, kernel_initializer ='uniform', activation='softmax'))

# Compile model
model.compile(loss='logcosh', optimizer='adagrad', metrics=['accuracy'])
# Fit the model
model.fit(np.array(X), np.array(Y), epochs=80, batch_size=20,  verbose=0)


VX, VY = [], []
for row in verifydata:
	VX.append(row[:3])
	VY.append(row[3])

scores = model.evaluate(np.array(VX), np.array(VY))
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# Computes the average difference
predictions = model.predict(np.array(VX))

print(list(set([int(list(d).index(max(d))) for d in predictions])))
time.sleep(5)
#sys.exit()


# Checks against car value
diff = []
orig = []
for hh in range(0, len(VY)):
	res = list(VY[hh]).index(max(VY[hh]))
	maxpred = list(predictions[hh]).index(max(predictions[hh]))

	orig.append(res)
	diff.append(abs(maxpred - res))

	#print("Original: %d, Predicted: %d" % (res, maxpred))


print("\nmean difference = $%f, σ = $%f\n" % (np.mean(diff), np.std(diff)))
