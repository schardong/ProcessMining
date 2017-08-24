# MDS function and distance dissimilarity

import numpy as np

from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from sklearn.decomposition import PCA
from sklearn import manifold
from sklearn.metrics import euclidean_distances


def mdsGen(data, weights):
    print("initializing MDS")
    mds = manifold.MDS(n_components=2, metric=True, n_init=4, max_iter=300, n_jobs=8, dissimilarity="precomputed")
    pos = mds.fit(data).embedding_
    print("creating plot")

    #cl = np.zeros((pos.shape[0], 1))
    #for i in range(100):
    #    cl[i] = weights[i]
    #print(pos.shape, cl.shape)
    #pos = np.hstack((pos, cl))
    print(pos.shape)
    return pos
