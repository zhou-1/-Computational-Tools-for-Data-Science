#!/usr/bin/env python
__author__ = 'Zhou Shen'

import os

file_path = 'arrhythmia.data'
X = []
Y = []
# a list to record index for NaN
NaN_place = []
# a list for each NaN value of NaN_place
median_list = []

# import data from file, add first 279 data of each line to temp array first then add in X
# take care of 0-279 values of each line, change '?' to 'NaN'
# add eachLine[279], last element to Y 
def import_data(filePath):
	f = open(filePath, "r")
	lines = f.readlines()
	for line in lines:
		eachLine = line.split(",")

		temp = []
		for i in range(279):
			eachVal = eachLine[i]
			if(eachVal == '?'):
				eachVal = 'NaN'
				if i not in NaN_place:
					NaN_place.append(i)
			temp.append(eachVal)
		X.append(temp)
		Y.append(eachLine[279])

	#print(X)
	#print(Y)
	#print(NaN_place)
	#cal_median(NaN_place) #if plan to use median for missing value
	#discard_missing(X, Y)  #if plan to discard the missing value

	return X, Y


# a function to compute median of all NaN column
# connect to impute_missing function
def cal_median(NaN_place):
	# iterate all NaN from NaN_place
	for i in NaN_place:
		#print(type(i))
		temp_list = []
		for ele in X[i]:
			if(ele != 'NaN'):
				temp_list.append(ele)
		sorted_list = sorted(temp_list)
		#print(sorted_list)
		listLen = len(sorted_list)
		index = (listLen-1)//2
		
		if(listLen%2 == 0):
			median_list.append(sorted_list[index])
		else:
			median_list.append((sorted_list[index]+sorted_list[index+1])/2.0)
	
	#print(median_list)
	impute_missing(X)


# impute these missing entries with median of column in X
# connect to cal_median function
def impute_missing(X):
	for i in range(len(X)):
		for j in range(len(X[i])):
			if(X[i][j] == 'NaN'):
				indexx = NaN_place.index(j)
				val = median_list[indexx]
				X[i][j] = val

	#print(X)
	return X


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


if __name__ == "__main__":
    import_data(file_path)