# MDS function and distance dissimilarity
from sklearn import manifold
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib import pyplot as plt
import copy
from scipy.spatial import ConvexHull
import numpy as np
from matplotlib.path import Path
import sys


class mdsClass(object):
    def __init__(self):
        self.pos = []

    def mdsGen(self, data):
        print("initializing MDS")
        mds = manifold.MDS(n_components=2, metric=True, n_init=4, max_iter=100, n_jobs=8, dissimilarity="precomputed")
        self.pos = mds.fit(data).embedding_
        return self.pos

    def mdsStress(self):
        return 0


class tsneClass(object):
    def __init__(self):
        self.pos = []

    def tsneGen(self, data):
        print("initializing tsne")
        tsneAlg = manifold.TSNE(n_components=2, metric='precomputed')
        self.pos = tsneAlg.fit(data).embedding_
        return self.pos


class spectralEmbeddingClass(object):
    def __init__(self):
        self.pos = []

    def genSPE(self, data):
        print("initializing Spectral Embedding")
        spe = manifold.SpectralEmbedding(n_components=2, affinity='precomputed')
        self.pos = spe.fit(data).embedding_
        return self.pos


class chart(object):
    def __init__(self, title):
        self.clicked = False
        self.pos = []
        self.selected = []
        self.selpoints = []
        self.selline = []
        self.chull = []
        self.title = title
        self.colors = [(0, 0, 1, 1), (1, 0, 0, 1), (0.48, 0.98, 0, 1)]

    def distance(self, point, event):
        assert point.shape == (2,), "distance: point.shape is wrong: %s, must be (3,)" % point.shape
        # Convert 2d data space to 2d screen space
        x3, y3 = self.ax.transData.transform((point[0], point[1]))
        return np.sqrt((x3 - event.x) ** 2 + (y3 - event.y) ** 2)

    def calcClosestDatapoint(self, event):
        """"Calculate which data point is closest to the mouse position.
        Args:
            X (np.array) - array of points, of shape (numPoints, 3)
            event (MouseEvent) - mouse event (containing mouse position)
        Returns:
            smallestIndex (int) - the index (into the array of points X) of the element closest to the mouse position
        """
        distances = np.array([self.distance(self.pos[i, 0:2], event) for i in range(self.pos.shape[0])])
        brushlist = np.where(np.logical_and(distances >= 0, distances <= 10))
        return brushlist[0]

    def saveCallback(self, function):
        self.save = function

    def keyPressed(self, event):
        sys.stdout.flush()
        if event.key == 's':
            print("saving")
            self.save(self.title, self.selected)
        if event.key == 'z':
            self.selected = []
            self.chull = []
            for i in range(self.pos.shape[0]):
                self.coll._facecolors[i, :] = self.colors[int(self.endsit[i])]
            for p in self.selpoints:
                p.remove()
            for line in self.selline:
                line.remove()
            self.selpoints = []
            self.selline = []
            self.fig.canvas.draw()


    def buttonClick(self, event):

        if event.button == 1:
            print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  (event.button, event.x, event.y, event.xdata, event.ydata))

            self.chull.append([event.xdata, event.ydata])
            p = np.array(self.chull)
            point, = plt.plot(event.xdata, event.ydata, 'o', picker=5, markersize=4, c="orange")
            line,  = plt.plot(p[:,0], p[:,1], 'r--', c="orange", lw=2)
            self.selpoints.append(point)
            self.selline.append(line)

        elif event.button == 3:
            hull = ConvexHull(np.array(self.chull))
            inds = hull.vertices
            p = np.array(self.chull)
            hull_path = Path(p[hull.vertices])
            for k in range(self.pos.shape[0]):
                if hull_path.contains_point(self.pos[k]):
                    self.selected.append(k)
                else:
                    self.coll._facecolors[k, :] = (1, 0.54, 0, 0.2)
            self.chull = []
        self.fig.canvas.draw()


    def drawPlot(self, size, pos, endsit):
        self.pos = np.array(pos)
        self.fig, self.ax = plt.subplots()
        self.endsit = endsit
        labels = ['Aproved', 'Denied', 'Canceled']
        self.coll = self.ax.scatter(pos[:, 0], pos[:, 1], c=endsit, cmap='brg', picker=5, alpha=0.7,
                                    edgecolors='none')
        plt.axis([-1, 1, -1, 1])
        green_patch = mpatches.Patch(color='blue', label='Aproved')
        red_patch = mpatches.Patch(color='red', label='Denied')
        blue_patch = mpatches.Patch(color='lawngreen', label='Canceled')
        self.ax.legend(handles=[green_patch, red_patch, blue_patch])
        self.fig.canvas.mpl_connect('button_press_event', self.buttonClick)
        self.fig.canvas.mpl_connect('key_press_event', self.keyPressed)
        plt.title(self.title)
        # plt.show()
