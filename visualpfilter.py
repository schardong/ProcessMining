import sys
import window

from PyQt5 import QtWidgets

class VisualProcessFilter(object):
    def __init__(self, s_argv):
        self.app = QtWidgets.QApplication(sys.argv)
        self.mainwindow = window.MainWindow(self)
        self.mainwindow.setupUi()
        
    def Init(self):
        weights = [1.0,50,0.0,0.5,1.0,0.0]
        weights_name = ["Credit Score","Request Amount","Number Of Offers", "Loan Goal", "Edit Distance", "Jaccard"]
        size = 2000
        activities = ["Accepted", "Cancelled", "Denied"]
        
        # Add sliders
        # TODO: Custom Name
        assert(len(weights) == len(weights_name))
        for i in range(len(weights)):
            self.mainwindow.AddFeatureSlider(weights_name[i], weights_name[i], weights[i])
            
        for i in range(len(activities)):
            self.mainwindow.AddActivityCheckBox(activities[i], activities[i])
        self.mainwindow.retranslateUi()
    
        #data = dataprovider.DataProvider(size, weights)
        #endsit = data.GetEndSituation()
        #dots = data.Calculate()
    
    def SetActivityVisibility(self, obj_name, state):
        print(obj_name, state)
        
    def SetFeatureWeightValue(self, obj_name, value):
        print(obj_name, value)
    
    
    def Start(self):
        self.mainwindow.Show()
        sys.exit(self.app.exec_())
    
if __name__ == "__main__":
    vpf = VisualProcessFilter(sys.argv)
    vpf.Init()
    vpf.Start()

