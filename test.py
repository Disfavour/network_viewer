import data
import sklearn.cluster
#import cuml.cluster
#import scikit-cuda
#import pycuda
import time

import matplotlib.pyplot
import matplotlib.pyplot as plt


path = "/home/disfavour/projects/network_viewer/datasets/20111209 Lomonosov-1/network_average.nc"
data_obj = data.Data(path)
arr = data_obj.get_3d_array()
cur_data = arr[0]
#print(arr)

#db = sklearn.cluster.DBSCAN(eps=0.0001)
#hz = db.fit(cur_data)
#lables = hz.labels_
#print(lables)
seconds = time.time()
print(seconds)
clustering = sklearn.cluster.AgglomerativeClustering(n_clusters=5)
for i in range(100):
    cur_data = arr[i]
    hz = clustering.fit(cur_data)
    lables = hz.labels_
seconds = time.time() - seconds
print(seconds)
"""
clustering = sklearn.cluster.AgglomerativeClustering(n_clusters=5).fit(cur_data)
print(clustering.labels_)
plt.scatter(cur_data[:,0], cur_data[:,1], c=clustering.labels_, cmap='Paired')
plt.title("K-means")
plt.show()
"""
