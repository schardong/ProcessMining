# MDS function and distance dissimilarity
from sklearn import manifold
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib import pyplot as plt
import copy
import numpy as np


class mdsclass(object):
    def __init__(self):
        self.clicked = False
        self.pos = []
        self.selected = []

    def mdsGen(self, data, weights):
        print("initializing MDS")
        mds = manifold.MDS(n_components=2, metric=True, n_init=4, max_iter=100, n_jobs=8, dissimilarity="precomputed")
        self.pos = mds.fit(data).embedding_
        return self.pos

    def mdsStress(self):
        return 0

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

    def onHover(self, event):
        if self.clicked == True:
            d = self.calcClosestDatapoint(event)
            self.selected.extend(d)
            self.selected = list(set(self.selected))
            for i in range(self.selected.__len__()):
                self.coll._facecolors[self.selected[i], :] = (1, 0.54, 0, 1)
            self.fig.canvas.draw()

    def buttonClick(self, event):
        self.coll._facecolors[event.ind, :] = (1, 0.54, 0, 1)
        self.fig.canvas.draw()
        self.clicked = True


    def buttonRelease(self, event):
        if event.button == 1:
            self.clicked = False

    def drawPlot(self, size, pos, endsit):
        self.fig, self.ax = plt.subplots()
        labels = ['Aproved', 'Denied', 'Canceled']
        self.coll = self.ax.scatter(pos[:, 0], pos[:, 1], c=endsit, cmap='brg', picker=5, alpha=0.7,
                                      edgecolors='none')
        plt.axis([-1, 1, -1, 1])
        green_patch = mpatches.Patch(color='blue', label='Aproved')
        red_patch = mpatches.Patch(color='red', label='Denied')
        blue_patch = mpatches.Patch(color='lawngreen', label='Canceled')
        self.ax.legend(handles=[green_patch, red_patch, blue_patch])
        self.fig.canvas.mpl_connect('pick_event', self.buttonClick)
        self.fig.canvas.mpl_connect('motion_notify_event', self.onHover)
        self.fig.canvas.mpl_connect('button_release_event', self.buttonRelease)
        plt.show()
