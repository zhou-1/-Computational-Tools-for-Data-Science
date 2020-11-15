#!/usr/bin/env python
__author__ = 'Zhou Shen'

import os
import numpy as np 
import random as random

file_path = 'train.csv'
# X: passengerId, Pclass, Age, SibSp, parch, fare
# alter sex (female: 0 & male: 1) 
# embarked (C:0, Q:1, S:2)
X = []
pId = []
pCls = []
sex = []
age = []
sibSp = []
parch = []
fare = []
embarked = []
# Y for "survived" feature 
Y = []

missing_vals = []

# import data from file
# return a matrix (list of lists) in row major
def read_csv(filePath):
	f = open(filePath, "r")
	lines = f.readlines()
	index = 0
	for line in lines:
		eachLine = line.split(",")

		if (line == lines[0]):
			pId.append(eachLine[0]) #PassengerId
			pCls.append(eachLine[2]) #Pclass
			sex.append(eachLine[4]) #Sex
			age.append(eachLine[5]) #age
			sibSp.append(eachLine[6]) #SibSp
			parch.append(eachLine[7]) #Parch
			fare.append(eachLine[9]) #Fare
			embarked.append(eachLine[11]) #Embarked
			Y.append(eachLine[1]) #survived
		else:
			#name has ',' between last and first names
			pId.append(int(eachLine[0])) #PassengerId
			pCls.append(int(eachLine[2])) #Pclass
			# Need to alert: X.append(eachLine[5]) #Sex
			if(eachLine[5] == 'female'):
				sex.append(0)
			elif(eachLine[5] == 'male'):
				sex.append(1)
			else:
				sex.append(-1)
			age.append(eachLine[6]) #age
			if(eachLine[6] == ''):
				missing_vals.append(index)
			sibSp.append(int(eachLine[7])) #SibSp
			parch.append(int(eachLine[8])) #Parch
			fare.append(int(float(eachLine[10]))) #Fare
			# Need to alert: X.append(eachLine[12]) #Embarked
			#print(eachLine[12])
			if('C' in eachLine[12]):
				embarked.append(0);
			elif('Q' in eachLine[12]):
				embarked.append(1);
			elif('S' in eachLine[12]):
				embarked.append(2);
			else:	
				#if(eachLine[12] == ''):
				# in case it also missing value for age
				embarked.append(-1);
				if index not in missing_vals:
					missing_vals.append(index)
			Y.append(int(eachLine[1])) #survived

		index += 1

	X.append(pId)
	X.append(pCls)
	X.append(sex)
	X.append(age)
	X.append(sibSp)
	X.append(parch)
	X.append(fare)
	X.append(embarked)

	#print(len(missing_vals))
	#print(len(X[0]))
	for i in reversed(missing_vals):
		Y.remove(Y[i])
		for j in range(len(X)):
			#print(X[j][i])
			X[j].remove(X[j][i])		

	#print(len(X[0]))
	#print(len(Y))
	#print(X)
	#print(Y)
	return X, Y



# split into 2 sets: train and tests
# t_f should be in [0,1]
def train_test_split(X, Y, t_f):
	# Train-test split
	X_train = []
	Y_train = []
	X_test = []
	Y_test = []
	test_indexs = []
	train_indexs = []
	# test for t_f
	if(t_f < 0 or t_f >1):
		raise Exception("sorry, t_f does not meet requirements")

	# get rid of the name: 'survived'
	tempY = Y[1:len(Y)]	
	test_Len = int(len(tempY) * t_f)
	train_len = len(tempY) - test_Len
	
	# get random indexes for test
	i = 0
	while(i < test_Len):
		# get a random number
		r = random.randint(0, len(tempY)+1)
		if(r not in test_indexs):
			test_indexs.append(r)
			i += 1

	# get random indexes for train
	for j in range(len(tempY)):
		if(j not in test_indexs):
			train_indexs.append(j)

	# put each element into Y's train and test sets
	for j in range(len(tempY)):
		if(j in test_indexs):
			Y_test.append(tempY[j])
		elif(j in train_indexs):
			Y_train.append(tempY[j])

	#print(len(Y_test))
	
	# put each element into X's train and test sets
	for k in range(len(X)):
		X_curCat_test = []
		X_curCat_train = []
		# get rid of the category name
		curTempX = X[k]
		curTempX = curTempX[1:len(X[k])]
		#print(curTempX)
		for j in range(len(curTempX)):
			if(j in test_indexs):
				X_curCat_test.append(curTempX[j])
			elif(j in train_indexs):
				X_curCat_train.append(curTempX[j])
		X_test.append(X_curCat_test)
		X_train.append(X_curCat_train)

	#print(len(X_test[0]))
	#print(len(X_train[0]))
	#print(len(Y_test))
	#print(len(Y_train))
	return X_train, Y_train, X_test, Y_test
	

def train_test_CV_split(X, Y, t_f, cv_f):
	# Train-test split
	X_train = []
	Y_train = []
	X_test = []
	Y_test = []
	X_cv = []
	Y_cv = []
	test_indexs = []
	train_indexs = []
	cv_indexs = []
	# test for t_f
	if(t_f < 0 or t_f >1):
		raise Exception("sorry, t_f does not meet requirements")
	# test for cv_f
	if(cv_f < 0 or cv_f >1):
		raise Exception("sorry, cv_f does not meet requirements")

	# get rid of the name: 'survived'
	tempY = Y[1:len(Y)]	
	test_Len = int(len(tempY) * t_f)
	cv_Len = int(len(tempY) * cv_f)
	train_len = len(tempY) - test_Len - cv_Len

	# get random indexes for test
	i = 0
	while(i < test_Len):
		# get a random number
		r = random.randint(0, len(tempY)+1)
		if(r not in test_indexs):
			test_indexs.append(r)
			i += 1
	# get random indexes for cv
	i = 0
	while(i < cv_Len):
		# get a random number
		r = random.randint(0, len(tempY)+1)
		if((r not in test_indexs) and (r not in cv_indexs)):
			cv_indexs.append(r)
			i += 1
	# get random indexes for train
	for j in range(len(tempY)):
		if((j not in test_indexs) and (j not in cv_indexs)):
			train_indexs.append(j)

	# put each element into Y's train and test sets
	for j in range(len(tempY)):
		if(j in test_indexs):
			Y_test.append(tempY[j])
		elif(j in train_indexs):
			Y_train.append(tempY[j])
		elif(j in cv_indexs):
			Y_cv.append(tempY[j])

	#print(len(Y_test))
	#print(len(Y_cv))
	#print(len(Y_train))

	# put each element into X's train and test sets
	for k in range(len(X)):
		X_curCat_test = []
		X_curCat_train = []
		X_curCat_cv = []
		# get rid of the category name
		curTempX = X[k]
		curTempX = curTempX[1:len(X[k])]
		#print(curTempX)
		for j in range(len(curTempX)):
			if(j in test_indexs):
				X_curCat_test.append(curTempX[j])
			elif(j in train_indexs):
				X_curCat_train.append(curTempX[j])
			elif(j in cv_indexs):
				X_curCat_cv.append(curTempX[j])
		X_test.append(X_curCat_test)
		X_train.append(X_curCat_train)
		X_cv.append(X_curCat_cv)

	#print(len(X_test[1]))
	#print(len(X_cv[1]))
	#print(len(X_train[1]))

	return X_train, Y_train, X_test, Y_test, X_cv, Y_cv


if __name__ == "__main__":
	read_csv(file_path)
	#train_test_split(X, Y, 0.5)
	#train_test_CV_split(X, Y, 0.2, 0.3)