# MDS function and distance dissimilarity



from sklearn import manifold
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import numpy as np


class mdsclass(object):
    def __init__(self):
        self.clicked = False
        self.pos = []

    def mdsGen(self, data, weights):
        print("initializing MDS")
        mds = manifold.MDS(n_components=3, metric=True, n_init=4, max_iter=100, n_jobs=8, dissimilarity="precomputed")
        self.pos = mds.fit(data).embedding_
        print("stress")
        #sum = (self.pos**2).sum
        #print(np.sqrt(mds.stress_() / sum))
        print("creating plot")

        #cl = np.zeros((pos.shape[0], 1))
        #for i in range(100):
        #    cl[i] = weights[i]
        #print(pos.shape, cl.shape)
        #pos = np.hstack((pos, cl))
        print(self.pos.shape)
        return self.pos


    def onHover(self,event):
        if self.clicked == True:
            print('x=%d, y=%d ' %
                 (event.x, event.y))

    def onclick(self,event):

        if event.button == 2:
            self.clicked = True



    def drawPlot(self, size,pos,endsit):
        red = 0
        green = 0
        blue = 0

        for i in range(size):
            if (endsit[i] == 0):
                green = green + 1
            elif (endsit[i] == 1):
                red = red + 1
            else:
                blue = blue + 1

        aproved = np.zeros((green, 3))
        denied = np.zeros((red, 3))
        canceled = np.zeros((blue, 3))

        k1 = 0
        k2 = 0
        k3 = 0
        for i in range(size):
            if (endsit[i] == 0):
                aproved[k1, :] = pos[i, :]
                k1 = k1 + 1
            elif (endsit[i] == 1):
                denied[k2, :] = pos[i, :]
                k2 = k2 + 1
            else:
                canceled[k3, :] = pos[i, :]
                k3 = k3 + 1

        fig, ax = plt.subplots()
        color = ['green', 'red', 'blue']
        labels = ['Aproved', 'Denied', 'Canceled']
        ax = Axes3D(fig)
        ax.scatter(aproved[:, 0], aproved[:, 1], aproved[:, 2], c='green',
                   alpha=0.7, edgecolors='none')
        ax.scatter(denied[:, 0], denied[:, 1], denied[:, 2], c='red',
                   alpha=0.7, edgecolors='none')
        ax.scatter(canceled[:, 0], canceled[:, 1], canceled[:, 2], c='blue',
                   alpha=0.7, edgecolors='none')

        green_patch = mpatches.Patch(color='green', label='Aproved')
        red_patch = mpatches.Patch(color='red', label='Denied')
        blue_patch = mpatches.Patch(color='blue', label='Canceled')
        ax.legend(handles=[green_patch, red_patch, blue_patch])

        fig.canvas.mpl_connect('button_press_event', self.onclick)
        fig.canvas.mpl_connect('motion_notify_event', self.onHover)
        plt.show()