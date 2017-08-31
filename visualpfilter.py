import sys
import window

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class VisualProcessFilter(object):
    def __init__(self, s_argv):
        self.app = QtWidgets.QApplication(sys.argv)
        self.ui = window.Ui_MainWindow(QtWidgets.QMainWindow(), self)
        self.ui.setupUi()
    
    def Init(self):
        weights = [1.0,50,0.0,0.5,1.0,0.0]
        weights_name = ["Credit Score","Request Amount","Number Of Offers", "Loan Goal", "Edit Distance", "Jaccard"]
        size = 2000
        activities = ["Accepted", "Cancelled", "Denied"]
        
        # Add sliders
        # TODO: Custom Name
        assert(len(weights) == len(weights_name))
        for i in range(len(weights)):
            self.ui.AddFeatureSlider(weights_name[i], weights_name[i], weights[i])
            
        for i in range(len(activities)):
            self.ui.AddActivityCheckBox(activities[i], activities[i])
        self.ui.retranslateUi()
    
        #data = dataprovider.DataProvider(size, weights)
        #endsit = data.GetEndSituation()
        #dots = data.Calculate()
    
    def SetActivityVisibility(self, obj_name, state):
        print(obj_name, state)
        
    def SetFeatureWeightValue(self, obj_name, value):
        print(obj_name, value)
    
    
    def Start(self):
        self.ui.Show()
        sys.exit(self.app.exec_())
    
if __name__ == "__main__":
    vpf = VisualProcessFilter(sys.argv)
    vpf.Init()
    vpf.Start()

