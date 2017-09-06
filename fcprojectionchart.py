import sys
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as mpatches

from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy

class ProjectionChart(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__ (self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.colors = [(0,0,1,1),(1,0,0,1),(0.48,0.98,0,1)]
        
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        # Click to focus 
        # Must be called to call key press and release events
        # or we can use "self.setFocus()" on some mouse callbacks
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        
        self.pos = None
        
        #self.save = data.SaveExportedData
        self.clicked = False
        self.selected = []
        
        ### Set Callbacks
        self.mpl_connect('button_press_event',self.buttonPressEvent)
        self.mpl_connect('button_release_event', self.buttonReleaseEvent)
        # draw_event
        self.mpl_connect('key_press_event', self.keyPressEvent)
        self.mpl_connect('key_release_event', self.keyReleaseEvent)
        self.mpl_connect('motion_notify_event', self.motionNotifyEvent)
        self.mpl_connect('pick_event', self.pickEvent)
        # resize_event
        # scroll_event
        # figure_enter_event
        # figure_leave_event
        # axes_enter_event
        # axes_leave_event
        # close_event        
                    
    def buttonPressEvent (self,event):
        #print("buttonPressEvent", event.button)
        if event.button == 3:
            for i in self.selected:
                self.coll._facecolors[i, :] = self.colors[int(self.endsit[i])]
            self.selected = []
            self.clicked = False
            self.draw()
        if event.button == 1:
            self.clicked = True

    def buttonReleaseEvent (self, event):
        #print("buttonRelease")
        if event.button == 1:
            self.clicked = False
            
    def keyPressEvent (self, event):
        #print("keyPressEvent")
        
        sys.stdout.flush()
        
        #if event.key == 's':
        #    self.save("Exported Files", self.selected)
    
    def keyReleaseEvent (self, event):
        #print("keyReleaseEvent")
        sys.stdout.flush()
    
    def motionNotifyEvent (self, event):
        #print("motion", event.xdata, event.ydata, self.clicked)
        
        if self.clicked == True:
            d = self.calcClosestDatapoint(event)
            self.selected.extend(d)
            self.selected = list(set(self.selected))
            for i in range(self.selected.__len__()):
                self.coll._facecolors[self.selected[i], :] = (1, 0.54, 0, 1)
            self.draw()

    def pickEvent (self, event):
        #print("pickEvent")
        self.coll._facecolors[event.ind, :] = (1, 0.54, 0, 1)
        self.draw()
        self.clicked = True
            
    def distance (self, point, event):
        assert point.shape == (2,), "distance: point.shape is wrong: %s, must be (3,)" % point.shape
        # Convert 2d data space to 2d screen space
        x3, y3 = self.axes.transData.transform((point[0], point[1]))
        return np.sqrt((x3 - event.x) ** 2 + (y3 - event.y) ** 2)

    def calcClosestDatapoint (self, event):
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

    def getSelectedDataPointsIndexes (self):
        assert(self.selected is not None)
        return self.selected
        
    def updateDataPoints (self, pos, endsit):
        self.pos = pos
        self.endsit = endsit
        
        # Remove selection
        for i in self.selected:
            self.coll._facecolors[i, :] = self.colors[int(self.endsit[i])]
        self.selected = []
                
        if self.pos is not None:
            self.axes.clear()
            self.coll = self.axes.scatter(self.pos[:, 0], self.pos[:, 1], c=self.endsit, cmap='brg', picker=5, alpha=0.7, edgecolors='none')
            
            green_patch = mpatches.Patch(color='blue', label='Aproved')
            red_patch = mpatches.Patch(color='red', label='Denied')
            blue_patch = mpatches.Patch(color='lawngreen', label='Canceled')
            self.axes.legend(handles=[green_patch, red_patch, blue_patch])
            
            self.draw()
        