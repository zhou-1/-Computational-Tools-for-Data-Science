#!/usr/bin/env python
__author__ = 'Zhou Shen'

import os
import numpy as np 
import random as random

file_path = 'question3.data'
X = []
Y = []

# import data
def import_data(filePath):
	f = open(filePath, "r")
	lines = f.readlines()
	for line in lines:
		eachLine = line.split(",")

		temp = []
		for i in range(len(eachLine)-1):
			eachVal = eachLine[i]
			if(eachVal == '?'):
				eachVal = 'NaN'
			temp.append(eachVal)
		X.append(temp)
		Y.append(eachLine[len(eachLine)-1])

	discard_missing(X, Y)
	#print(X)
	#print(Y)
	#shuffle_order(X, Y)
	#standard_deviation(X)
	#remove_entries(X, Y)
	#standardize_data(X)
	return X,Y


# a function to discard the NAN samples
def discard_missing(X, Y):
	index_place = []
	for i in range(len(X)):
		for j in range(len(X[i])):
			if(X[i][j] == 'NaN'):
				# in case in one sample, there are 2 or more NANs
				if i not in index_place:
					index_place.append(i)

	#print(len(index_place))
	for i in reversed(index_place):
		X.remove(X[i])
		Y.remove(Y[i])
	
	return X, Y



# Shuffle funtion
def shuffle_order(X, Y):
	for i in range(len(X)-1, 0, -1):
		# get a random number
		r = random.randint(0, i+1)
		# swap X[i] with the lement at random index
		X[i], X[r] = X[r], X[i]
		Y[i], Y[r] = Y[r], Y[i]

	#print(X)
	#print(Y)
	return X, Y


# standard deviation of each feature
def standard_deviation(X):
	N = len(X)
	elements_line = len(X[0]) #how many attributes for each line
	mean_list = [0]*elements_line 
	sd_list = [0]*elements_line

	for i in range(N):
		for j in range(elements_line):
			mean_list[j] += int(X[i][j])

	# get mean value
	for i in range(len(mean_list)):
		mean_list[i] = mean_list[i]//N

	# get sum of square deviation and standard deviation
	for i in range(len(mean_list)):
		ss = sum((int(X[j][i]) - mean_list[i])**2 for j in range(len(X)))
		sd = ss // (N-1)
		
		sd_list[i] = sd

	print(sd_list)
	return mean_list, sd_list


# remove entries that contain a value more than 2 sd away from the mean
def remove_entries(X, Y):
	mean_list, sd_list = standard_deviation(X)
	rm_list = []
	
	for i in range(len(mean_list)):
		mean_val = mean_list[i]
		sd_val = sd_list[i]
		for j in range(len(X)):
			if(abs(int(X[j][i]) - mean_val) > (sd_val*2)):
				if j not in rm_list:
					rm_list.append(j)

	#print(rm_list)
	for i in reversed(sorted(rm_list)):
		X.remove(X[i])
		Y.remove(Y[i])

	print(X)
	print(Y)
	return X, Y


# standardize all the data points
def standardize_data(X):
	mean_list, sd_list = standard_deviation(X)
	for i in range(len(X)):
		for j in range(len(X[i])):
			if(sd_list[j] == 0):
				X[i][j] = 0
			else:
				X[i][j] = (int(X[i][j])-mean_list[j])//sd_list[j]
			
	print(X)
	return X



if __name__ == "__main__":
	import_data(file_path)