import sklearn.cluster
#import cuml.cluster

#cuml.common.memory_utils.set_global_output_type(numpy)

def get_labels_dbscan(data):
    db = sklearn.cluster.DBSCAN(eps=0.0001)
    cl = db.fit(data)
    lables = cl.labels_
    return lables


def get_labels_agg(data):
    agg = sklearn.cluster.AgglomerativeClustering(n_clusters=5)
    clustering = agg.fit(data)
    labels = clustering.labels_
    return labels

"""
def get_labels_d_cuda(data):
    db = cuml.cluster.DBSCAN(eps=0.0001)
    cl = db.fit(data)
    lables = cl.labels_
    return lables


def get_labels_a_cuda(data):
    agg = cuml.cluster.AgglomerativeClustering(n_clusters=5)
    clustering = agg.fit(data)
    labels = clustering.labels_
    return labels
"""

if __name__ == "__main__":
    pass
