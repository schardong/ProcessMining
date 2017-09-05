import sys

import window
import dataprovider
import learn

from PyQt5 import QtWidgets

class VisualProcessFilter(object):
    def __init__(self, s_argv):
        self.app = QtWidgets.QApplication(sys.argv)
        self.mainwindow = window.MainWindow(self)
        self.mainwindow.setupUi()
        
    def Init(self):
        self.weights_name = ["Credit Score",
                             "Request Amount",
                             "Number Of Offers",
                             "Loan Goal",
                             "Edit Distance",
                             "Jaccard"]
        
        self.weights = { "Credit Score" : 1.0,
                         "Request Amount" : 0.5,
                         "Number Of Offers" : 0.0,
                         "Loan Goal" : 0.5,
                         "Edit Distance" : 1.0,
                         "Jaccard" : 0.0 }
        
        activities = ["Accepted", "Cancelled", "Denied"]
        
        # Add sliders
        # TODO: Custom Name
        for i in range(len(self.weights_name)):
            self.mainwindow.AddFeatureSlider(self.weights_name[i], self.weights_name[i], self.weights[self.weights_name[i]])
            
        for i in range(len(activities)):
            self.mainwindow.AddActivityCheckBox(activities[i], activities[i])
        self.mainwindow.retranslateUi()
   
        #dots = data.Calculate()

        # Add data  
        self.mainwindow.setMaxNumberOfCases(400)
        self.mainwindow.setCurrentNumberOfCases(200)
        self.updateNumberOfCases(200)
                
    def SetActivityVisibility(self, obj_name, state):
        print(obj_name, state)
        
    def SetFeatureWeightValue(self, obj_name, value):
        self.weights[obj_name] = value
    
    def updateNumberOfCases (self, size):
        ax_weights = []
        for i in range(len(self.weights_name)):
            ax_weights.append(self.weights[self.weights_name[i]])
        
        data = dataprovider.DataProvider(size, ax_weights)
        endsit = data.GetEndSituation()
        dots = data.Calculate()
        mds = learn.mdsClass()
        pos = mds.mdsGen(dots)
         
        plot = self.mainwindow.GetProjectionChart()
        plot.updateDataPoints(pos, endsit)
    
    def Start(self):
        self.mainwindow.Show()
        sys.exit(self.app.exec_())
    
if __name__ == "__main__":
    vpf = VisualProcessFilter(sys.argv)
    vpf.Init()
    vpf.Start()

