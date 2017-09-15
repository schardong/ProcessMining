#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that defines the multidimensional projection algorithms available.
"""

import numpy as np
from sklearn import manifold


class BaseProjection(object):
    """
    Base class for all projection algorithms. Provides a series of methods to
    call the algorithms and to evaluate the projection's fitness.
    """

    def __init__(self, name):
        """
        Default constructor for the base projection.

        Parameters
        ----------
        name: str
            The name of the projection algorithm. e.g. 'MDS', 'LAMP', 'TSNE',
            etc. To be given by the inherited class.
        """
        self._name = name
        self._proj_data = None

    @property
    def projected_data(self):
        """
        Returns the results of the projection.
        """
        return self._proj_data

    def calc_projection_fitness(self):
        """
        """
        raise NotImplementedError('Method must be implemented by a subclass.')


class MDS(BaseProjection):
    """
    This class runs the multidimensional scaling algorithm on a given
    dissimilarity matrix. It acts as a wrapper around the sklearn.manifold.MDS
    object and passes the given arguments to that object.

    References to the MDS and its workings can be found here:
    https://en.wikipedia.org/wiki/Multidimensional_scaling
    References to the sklearn MDS algorithm can be found here:
    http://scikit-learn.org/stable/modules/generated/sklearn.manifold.MDS.html
    """

    def __init__(self):
        super().__init__('MDS')

    def __call__(self, diss_data, **kwargs):
        """
        Runs the MDS algorithm on the given dissimilarity matrix.

        Parameters
        ----------
        diss_data: numpy.array
            A NxN matrix with the input dissimilarity matrix, where N is the
            number of objects.
        kwargs: Other keyword arguments
            Other arguments to pass to manifold.MDS.

        Returns
        -------
        A numpy.array with N rows and ndims columns created by the MDS.
        """
        mds = manifold.MDS(dissimilarity='precomputed', **kwargs)
        self._proj_data = mds.fit(diss_data).embedding_
        return self._proj_data


class TSNE(BaseProjection):
    """
    This class runs the t-distributed Stochastic Neighbor Embedding algorithm
    on the given dissimilarity matrix. It acts as a wrapper over the
    sklearn.manifold.TSNE object and, when called, passes any given arguments
    to it.

    References to the TSNE can be found here:
    https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding
    References to the sklearn version of the algorithm can be found here:
    http://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
    """

    def __init__(self):
        super().__init__('TSNE')

    def __call__(self, diss_data, **kwargs):
        """
        Runs the TSNE algorithm on the given dissimilarity matrix.

        Parameters
        ----------
        data: numpy.array
            A NxN matrix with the input dissimilarity matrix, where N is the
            number of objects.
        kwargs: Other keyword arguments
            Other arguments to pass to manifold.TSNE.
        """
        tsne_obj = manifold.TSNE(metric='precomputed', **kwargs)
        self._proj_data = tsne_obj.fit(diss_data).embedding_
        return self._proj_data


class SpectralEmbedding(BaseProjection):
    """
    This class runs the Spectral Embedding algorithm on the given dissimilarity
    matrix. It acts as a wrapper over the sklearn.manifold.SpectralEmbedding
    object and, when called, passes any given arguments to it.

    References to the algorithm can be found here:
    https://en.wikipedia.org/wiki/Nonlinear_dimensionality_reduction
    References to the sklearn version of the algorithm can be found here:
    http://scikit-learn.org/stable/modules/generated/sklearn.manifold.SpectralEmbedding.html
    """

    def __init__(self):
        super().__init__('SpectralEmbedding')

    def __call__(self, diss_data, **kwargs):
        """
        Runs the Spectral Embedding algorithm using the given dissimilarity
        matrix as input.

        Parameters
        ----------
        data: numpy.array
            A NxN matrix with the input dissimilarity matrix, where N is the
            number of objects.
        kwargs: Other keyword arguments
            Other arguments to pass to manifold.SpectralEmbedding.
        """
        tsne_obj = manifold.SpectralEmbedding(affinity='precomputed', **kwargs)
        self._proj_data = tsne_obj.fit(diss_data).embedding_
        return self._proj_data


def main():
    import matplotlib.pyplot as plt
    from scipy.spatial.distance import squareform, pdist

    data = np.random.exponential(scale=1, size=(50, 30))
    dist = squareform(pdist(data))

    mds = MDS()
    pts1 = mds(dist, n_components=2)
    tsne = TSNE()
    pts2 = tsne(dist, n_components=2)
    spm = SpectralEmbedding()
    pts3 = spm(dist, n_components=2)

    plt.subplot(311)
    plt.scatter(pts1[:, 0], pts1[:, 1])
    plt.subplot(312)
    plt.scatter(pts2[:, 0], pts2[:, 1])
    plt.subplot(313)
    plt.scatter(pts3[:, 0], pts3[:, 1])

    plt.show()


if __name__ == '__main__':
    main()
