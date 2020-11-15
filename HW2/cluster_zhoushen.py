#!/usr/bin/env python
# longitude and latitude: cluster closeness
# price: cluster expensiveness

import numpy as np
import pandas as pd

import kmeans_zhou as kmeans

import folium
import matplotlib.pyplot as plt
from folium.plugins import HeatMap
from sklearn.mixture import GaussianMixture
from sklearn.cluster import AgglomerativeClustering
from mpl_toolkits.mplot3d import Axes3D
from scipy.cluster.hierarchy import dendrogram, linkage

import cv2

# read file
def read_file():
	name = ['latitude', 'longitude', 'price']
	csvfile = 'listings.csv'
	df = pd.read_csv(csvfile, sep=',', usecols=name)
	return df


# data pre-process
def data_process():
	df = read_file()
	# transform it into float type
	df = pd.DataFrame(df, dtype=np.float)
	# normalize
	df = df.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x))) 
	return df


# k means method
def k_means_pp():
	res = data_process()
	# drop all rows which has nan
	res = res.dropna()
	res = res.values.tolist()
	clustering, assignments = kmeans.k_means_pp(res, 5)
	#print(clustering)

	# 2D position plot
	fig = plt.figure()
	color = ['orange', 'y', 'g', 'r', 'violet']

	for i in range(len(clustering)):
		cluster = np.array(clustering[i])
		plt.scatter(cluster[:, 0], cluster[:, 1], cmap='rainbow')

	plt.xlabel("latitude")
	plt.ylabel("longitude")
	plt.show()

	return clustering, assignments


# hierarchical 
def Hierarchical():
	res = data_process()
	# drop all rows which has nan
	res = res.dropna()
	df = res
	res = res.values.tolist()
	res = np.array(res)

	row_rand_array = np.arange(res.shape[0])
	res = res[row_rand_array[0:3000]] #30000

	agg = AgglomerativeClustering(n_clusters = 5, linkage = 'ward')
	Hier_label = agg.fit(res).labels_

	# 2D position plot
	fig = plt.figure()
	ax = fig.add_subplot(111)
	scatter = ax.scatter(df['latitude'][row_rand_array[0:3000]], df['longitude'][row_rand_array[0:3000]], c=res, s=50)
	ax.set_xlabel('latitude')
	ax.set_ylabel('longitude')
	plt.colorbar(scatter)

	return res, Hier_label


# GMM
def GMM():
    res = data_process()
    # drop all rows which has nan
    res = res.dropna()
    data = res.values

    res = res.values.tolist()
    gmm = GaussianMixture(n_components = 5, max_iter = 100000, covariance_type = 'spherical').fit(res)
    assignment = gmm.predict(res)

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(data[:, 0], data[:,1], data[:,2], c = gmm.predict(data), cmap = 'rainbow')
    plt.show()

    return gmm, assignment




### Problem 3
# generate the heatmap
def generate_base_map(default_location=[40.693943, -73.985880]):
    base_map = folium.Map(location=default_location)
    return base_map

def draw_heatmap(data, filename):
    base_map = generateBaseMap()

    mean = data.groupby(['latitude','longitude']).mean()
    HeatMap(mean.reset_index().values.tolist(), radius = 8, max_zoom = 13).add_to(base_map)
    base_map.save(filename)

# calculate average price of each cluster
def cal_avg_price(clusterings, assignments):
    '''
        :param: clusterings: return value of run_kmeans method
        :param: assignments: assignments of points
    '''
    cluster_map = read_file().copy()
    # drop all rows which has nan
    cluster_map = cluster_map.dropna()
    cluster_map.loc[:, 'cluster_index'] = assignments

    price_mean = []

    for i in range(7):
    	prices = cluster_map[cluster_map['cluster_index'] == i]
    	price_mean.append(np.array(prices['price']).mean())

    print(price_mean)
    return cluster_map, price_mean




#### problem 4 Image Manipulation
def read_img():
	# read image
	img = cv2.imread("boston-1993606_1280.jpg")

	# reduce the matrix to 2D and change to list
	img = np.reshape(img, (-1, 3))
	img = img.tolist()

	# compute clusters' centers
	cluster, assignment = kmeans.k_means(img, 10)
	center0 = kmeans.point_avg(cluster[0])
	center1 = kmeans.point_avg(cluster[1])
	center2 = kmeans.point_avg(cluster[2])
	center3 = kmeans.point_avg(cluster[3])
	center4 = kmeans.point_avg(cluster[4])
	center5 = kmeans.point_avg(cluster[5])
	center6 = kmeans.point_avg(cluster[6])
	center7 = kmeans.point_avg(cluster[7])
	center8 = kmeans.point_avg(cluster[8])
	center9 = kmeans.point_avg(cluster[9])

	# iterate for all pixels
	for i in range(len(assignment)):
		if assignment[i] == 0:
			img[i] = center0
		if assignment[i] == 1:
			img[i] = center1
		if assignment[i] == 2:
			img[i] = center2
		if assignment[i] == 3:
			img[i] = center3
		if assignment[i] == 4:
			img[i] = center4
		if assignment[i] == 5:
			img[i] = center5
		if assignment[i] == 6:
			img[i] = center6
		if assignment[i] == 7:
			img[i] = center7
		if assignment[i] == 8:
			img[i] = center8
		if assignment[i] == 9:
			img[i] = center9

	# reshape the array to actual 3D
	img = np.array(img)
	img = np.reshape(img, (850, 1280, 3))
	img = img.astype(int)

	plt.imshow(img)
	plt.show()




# main function
def main():
	# read file
	read_file()
	
	# data pre-process
	#data_process()

	# k means ++
	#clusterings, assignments = k_means_pp()
	
	# hierarchical
	#clusterings, assignments = Hierarchical()

	# GMM
	#clusterings, assignments = GMM()

	# calculate averge price
	#cal_avg_price(clusterings, assignments)

	# read image and process
	read_img()


if __name__ == '__main__':
    main()