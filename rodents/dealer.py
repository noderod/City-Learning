"""
BASICS

Uses keras neural network to compute if the price of a car is larger than $8,000
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
car_max_price = 1 # -1)*1000 $
D1 = []
L8 = 0
for row in dataset:
	carval = 1*(int(row[3]) > 8)
	L8 += carval

	D1.append([row[0], row[1], row[2], carval])


print("Original: %.2f%%" % (100*L8/len(D1)))


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

# 100 50 50 50 20
# create model
model = Sequential()
model.add(Dense(100, input_dim=3, kernel_initializer ='uniform', activation='relu'))
model.add(Dense(50, input_dim=3, kernel_initializer ='uniform', activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(80, input_dim=3, kernel_initializer ='uniform', activation='sigmoid'))
model.add(Dropout(0.5))
model.add(Dense(50, kernel_initializer ='uniform', activation='relu'))
model.add(Dropout(0.8))
model.add(Dense(50, kernel_initializer ='uniform', activation='sigmoid'))
model.add(Dropout(0.3))
model.add(Dense(50, kernel_initializer ='uniform', activation='sigmoid'))
model.add(Dropout(0.4))
model.add(Dense(units=car_max_price, kernel_initializer ='uniform', activation='sigmoid'))


"""
78 max % 

model = Sequential()
model.add(Dense(100, input_dim=3, kernel_initializer ='uniform', activation='relu'))
model.add(Dense(50, input_dim=3, kernel_initializer ='uniform', activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(80, input_dim=3, kernel_initializer ='uniform', activation='sigmoid'))
model.add(Dropout(0.7))
model.add(Dense(50, kernel_initializer ='uniform', activation='relu'))
model.add(Dropout(0.8))
model.add(Dense(50, kernel_initializer ='uniform', activation='sigmoid'))
model.add(Dropout(0.3))
model.add(Dense(50, kernel_initializer ='uniform', activation='sigmoid'))
model.add(Dropout(0.4))
model.add(Dense(units=car_max_price, kernel_initializer ='uniform', activation='sigmoid'))
"""

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
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

# Checks against car value
diff = []
orig = []
for hh in range(0, len(VY)):
	res = VY[hh]
	pred = int(round(predictions[hh][0]))

	orig.append(res)
	diff.append(abs(pred - res))

print("\nmean difference = %f, σ = %f\n" % (np.mean(diff), np.std(diff)))
# Saves the model for later
model.save('price_L8.h5')
