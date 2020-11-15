from collections import defaultdict
from math import inf
import random
import csv


def point_avg(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    (points can have more dimensions than 2)
    
    Returns a new point which is the center of all the points.
    """
    n = len(points)
    x = sum([p[0] for p in points]) / n
    y = sum([p[1] for p in points]) / n
    z = sum([p[2] for p in points]) / n
    return [x, y, z]


def update_centers(dataset, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.
    Compute the center for each of the assigned groups.
    Return `k` centers in a list
    """
    k = max(assignments) + 1
    clusters = [[] for i in range(k)]
    for pointIndex, pointAssignment in enumerate(assignments):
        clusters[pointAssignment].append(dataset[pointIndex])

    new_centers = []
    for cluster in clusters:
        new_centers.append(point_avg(cluster))

    return new_centers

def assign_points(data_points, centers):
    """
    """
    assignments = []
    for point in data_points:
        shortest = inf  # positive infinity
        shortest_index = 0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments


def distance(a, b):
    """
    Returns the Euclidean distance between a and b
    """
    return sum([(a - b) ** 2 for a, b in zip(a, b)]) ** 0.5

def distance_squared(a, b):
    return distance(a, b) ** 2


def generate_k(dataset, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    """
    return random.sample(dataset, k)


def cost_function(clustering):
    cost = 0
    for idx in clustering:
        center = point_avg(clustering[idx])
        cost += sum([distance_squared(center, p) for p in clustering[idx]])

    return cost


def generate_k_pp(dataset, k):
    center = random.choice(dataset)
    k_points = [center]

    while len(k_points) < k:
        prob = []
        for point in dataset:
            prob.append(distance_squared(center, point))
        
        prob = [p/sum(prob) for p in prob]
        center = random.choices(dataset, prob)[0]

        k_points.append(center)

    return k_points


def _do_lloyds_algo(dataset, k_points):
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = update_centers(dataset, assignments)
        old_assignments = assignments
        assignments = assign_points(dataset, new_centers)
    clustering = defaultdict(list)
    for assignment, point in zip(assignments, dataset):
        clustering[assignment].append(point)

    return clustering, assignments


def k_means(dataset, k):
    if k not in range(1, len(dataset)+1):
        raise ValueError("lengths must be in [1, len(dataset)]")
    
    k_points = generate_k(dataset, k)
    return _do_lloyds_algo(dataset, k_points)


def k_means_pp(dataset, k):
    if k not in range(1, len(dataset)+1):
        raise ValueError("lengths must be in [1, len(dataset)]")

    k_points = generate_k_pp(dataset, k)
    return _do_lloyds_algo(dataset, k_points)
