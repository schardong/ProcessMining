# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designerwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

import sys
import random
import matplotlib
matplotlib.use("Qt5Agg")

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import dataprovider
import mds

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
		
    def compute_initial_figure(self):
        pass

class ActivityCheckBox():
    def __init__(self, ckb_name, wgt_parent, report_cb):
        self.obj_name = ckb_name
        self.report_cb = report_cb
        self.parent = wgt_parent
        self.checkBox = QtWidgets.QCheckBox(self.parent)
        self.checkBox.setObjectName(ckb_name)
        self.checkBox.stateChanged.connect(self.StateChanged)       
        
    def AddWidget(self, layout_reference):
        self.refence = layout_reference
        self.refence.addWidget(self.checkBox)
        
    def RemoveWidget(self):
        self.refence.removeWidget(self.checkBox)
        self.checkBox.deleteLater()
        self.checkBox = None
        
    def SetText(self, text):
        self.text = text
        
    def UpdateLabel(self, translate):
        self.checkBox.setText(translate("MainWindow", self.text))
        
    def SetCheckState(self, state):
        assert(state == QtCore.Qt.Checked or state == QtCore.Qt.Unchecked)
        self.state = state
        self.checkBox.setCheckState(state)
        
    ''' stateChanged Qt Signal connected from QCheckBox
        CheckState:
            Qt.Unchecked        0
            Qt.PartiallyChecked	1
            Qt.Checked          2
    '''
    def StateChanged(self, state):
        assert(state == QtCore.Qt.Checked or state == QtCore.Qt.Unchecked)
        self.state = state
        self.report_cb(self.obj_name, self.state)
        
class SliderFeatureController():
    def __init__(self, obj_name, wgt_parent, lyt_parent, report_cb):
        self.obj_name = obj_name
        self.parent = wgt_parent
        self.parent_layout = lyt_parent
        self.report_cb = report_cb
        
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.setObjectName("vertical_layout_" + obj_name)
        
        self.ftr_label = QtWidgets.QLabel(self.parent)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ftr_label.sizePolicy().hasHeightForWidth())
        
        self.ftr_label.setSizePolicy(sizePolicy)
        self.ftr_label.setObjectName("ftr_label_" + obj_name)
        
        # add label into vertical layout
        self.vertical_layout.addWidget(self.ftr_label)
        
        self.slr_h_feature = QtWidgets.QSlider(self.parent)
        self.slr_h_feature.setOrientation(QtCore.Qt.Horizontal)
        self.slr_h_feature.setObjectName(obj_name)
        self.slr_h_feature.valueChanged.connect(self.ValueChanged)
        
        self.vertical_layout.addWidget(self.slr_h_feature)
        self.parent_layout.addLayout(self.vertical_layout)
    
    def SetValue(self, curr_value):
        self.value = curr_value
        self.slr_h_feature.setValue(curr_value)
    
    def SetText(self, text):
        self.text = text
        
    def UpdateLabel(self, translate):
        self.ftr_label.setText(translate("MainWindow", self.text))
        
    ''' valueChanged Qt Signal connected from QSlider '''
    def ValueChanged(self, value):
        self.value = value
        self.report_cb(self.obj_name, self.value)
        
class Ui_MainWindow(object):
    def __init__(self, MainWindow, vpf_controller):
        super(Ui_MainWindow, self).__init__()
        self.main_window = MainWindow
        self.controller = vpf_controller
                
    def setupUi(self):
        assert(self.main_window is not None)
        self.main_widget = QtWidgets.QWidget(self.main_window)
        
        self.main_window.setObjectName("MainWindow")
        self.main_window.resize(978, 667)
        
        # Global Horizontal Layout (All window)
        self.CentralHLayout = QtWidgets.QWidget(self.main_window)
        self.CentralHLayout.setObjectName("CentralHLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.CentralHLayout)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        # Left Vertical Layout (CheckBoxes, Plot and progressBar)
        self.LeftVLayout = QtWidgets.QVBoxLayout()
        self.LeftVLayout.setObjectName("LeftVLayout")
        
        # Right Horizontal Layout (FeatureHSliders, VSliders)
        self.RightHLayout = QtWidgets.QHBoxLayout()
        self.RightHLayout.setObjectName("RightHLayout")
        
        # scrollable area for checkboxes
        self.checkbox_scrollarea = QtWidgets.QScrollArea(self.CentralHLayout)
        self.checkbox_scrollarea.setMaximumSize(QtCore.QSize(16777215, 54))
        self.checkbox_scrollarea.setWidgetResizable(True)
        self.checkbox_scrollarea.setObjectName("checkbox_scrollarea")
        # horizontal layout for checkbox (widget + checkbox)
        self.widget_cbx_hor_layout = QtWidgets.QWidget()
        self.widget_cbx_hor_layout.setGeometry(QtCore.QRect(0, 0, 473, 52))
        self.widget_cbx_hor_layout.setObjectName("widget_cbx_hor_layout")
        self.layout_hor_cbx = QtWidgets.QHBoxLayout(self.widget_cbx_hor_layout)
        self.layout_hor_cbx.setContentsMargins(0, 0, 0, 0)
        self.layout_hor_cbx.setObjectName("layout_hor_cbx")
        self.checkbox_scrollarea.setWidget(self.widget_cbx_hor_layout)
        
        #########################
        # Check Box Activity List
        self.lst_aCheckBox = list()
        #self.AddActivityCheckBox("checkbox0")
        #self.AddActivityCheckBox("checkbox1")
        #self.AddActivityCheckBox("checkbox2")
        #self.AddActivityCheckBox("checkbox3")
        #self.AddActivityCheckBox("checkbox4")
        #self.AddActivityCheckBox("checkbox5")

        # Add Checkbox ScrollArea into the LeftVLayout
        self.LeftVLayout.addWidget(self.checkbox_scrollarea, 0, QtCore.Qt.AlignTop)
        
        #########################
        # MatPlot Creation
        self.graphicsView = MyMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        self.graphicsView.setObjectName("graphicsView")
        
        # Add MatPlot into the LeftVLayout
        self.LeftVLayout.addWidget(self.graphicsView)
        
        #########################
        # Progress bar
        self.progressBar = QtWidgets.QProgressBar(self.CentralHLayout)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        
        # Add ProgressBar into the LeftVLayout
        self.LeftVLayout.addWidget(self.progressBar)
        
        # Scrollable Area for Sliders
        self.scl_are_features = QtWidgets.QScrollArea(self.CentralHLayout)
        self.scl_are_features.setMaximumSize(QtCore.QSize(300, 16777215))
        self.scl_are_features.setWidgetResizable(True)
        self.scl_are_features.setObjectName("scl_are_features")
        
        # Create the widget for vertical layout
        self.lay_ver_features = QtWidgets.QWidget()
        self.lay_ver_features.setGeometry(QtCore.QRect(0, 0, 298, 604))
        self.lay_ver_features.setObjectName("lay_ver_features")
        # Create the VBoxLayout
        self.verticalLayout = QtWidgets.QVBoxLayout(self.lay_ver_features)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        #########################
        # Create Feature Sliders
        self.lst_fSlider = list()
        #self.AddFeatureSlider("slider0")
        #self.AddFeatureSlider("slider1")
        #self.AddFeatureSlider("slider2")
        #self.AddFeatureSlider("slider3")
        #self.AddFeatureSlider("slider4")
        #self.AddFeatureSlider("slider5")             
        #self.AddFeatureSlider("slider6")
        #self.AddFeatureSlider("slider7")
        #self.AddFeatureSlider("slider8")        
        
        # Add the vertical widget layout for sliders
        self.scl_are_features.setWidget(self.lay_ver_features)
        
        # Add Scrollable Area into the right horizontal Layout
        self.RightHLayout.addWidget(self.scl_are_features)
        
        # Create the Vertical Slider to control the number of cases
        self.verticalSlider = QtWidgets.QSlider(self.CentralHLayout)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        
        # Add Vertical Slider into the right horizontal Layout
        self.RightHLayout.addWidget(self.verticalSlider)
        
        
        # Add LeftVLayout to the Global Horizontal Layout
        self.horizontalLayout.addLayout(self.LeftVLayout)
        # Add RightVLayout to the Global Horizontal Layout
        self.horizontalLayout.addLayout(self.RightHLayout)
        
        # Add Central Horizontal Layout into the MainWindow
        self.main_window.setCentralWidget(self.CentralHLayout)
        
        # Menu Bar Creation
        self.menubar = QtWidgets.QMenuBar(self.main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 978, 21))
        self.menubar.setObjectName("menubar")
        
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        
        self.main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.main_window)
        self.statusbar.setObjectName("statusbar")
        self.main_window.setStatusBar(self.statusbar)
        
        # Action attached to "Quit" menu item
        self.actionQuit = QtWidgets.QAction(self.main_window)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.triggered.connect(self.QuitApplication)
        
        self.actionRemove_Checkbox = QtWidgets.QAction(self.main_window)
        self.actionRemove_Checkbox.setObjectName("actionRemove_Checkbox")
        self.actionRemove_Checkbox.triggered.connect(self.removeCheckboxFromMain)


        self.menuFile.addAction(self.actionRemove_Checkbox)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        
        self.main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        # Update Check Box Activity Names
        for i in range(len(self.lst_aCheckBox)):
            self.lst_aCheckBox[i].UpdateLabel(_translate)
        
        # Update Slider Feature Names        
        for i in range(len(self.lst_fSlider)):
            self.lst_fSlider[i].UpdateLabel(_translate)
        
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionRemove_Checkbox.setText(_translate("MainWindow", "Remove Checkbox"))

    """ Remove CheckBox From MainWindow """
    def removeCheckboxFromMain(self):
        if len(self.lst_aCheckBox) > 0:
            self.lst_aCheckBox[0].RemoveWidget()
            self.lst_aCheckBox[0] = None
            self.lst_aCheckBox.remove(self.lst_aCheckBox[0])
        
    """ Quit Application """
    def QuitApplication(self):
        ret_mbox = QtWidgets.QMessageBox.question(self.main_window, "Quit","Are you sure?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) 
        if ret_mbox == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass
            
    """ Add a new Activity CheckBox """        
    def AddActivityCheckBox(self, obj_name, text_label):
        assert(self.widget_cbx_hor_layout is not None and self.layout_hor_cbx is not None and self.lst_aCheckBox is not None)
        
        index_cbox = len(self.lst_aCheckBox)
        
        self.lst_aCheckBox.append(ActivityCheckBox(obj_name, self.widget_cbx_hor_layout, self.SetCheckBoxState))
        self.lst_aCheckBox[index_cbox].AddWidget(self.layout_hor_cbx)
        self.lst_aCheckBox[index_cbox].SetText(text_label)
        self.lst_aCheckBox[index_cbox].SetCheckState(QtCore.Qt.Checked)
        
    def AddFeatureSlider(self, obj_name, text_label, initial_value):
        assert(self.lay_ver_features is not None and self.verticalLayout is not None and self.lst_fSlider is not None)
                
        index_cbox = len(self.lst_fSlider)
        
        self.lst_fSlider.append(SliderFeatureController(obj_name, self.lay_ver_features, self.verticalLayout, self.SetSliderValue))
        #self.lst_fSlider[index_cbox].AddWidget(self.layout_hor_cbx)
        self.lst_fSlider[index_cbox].SetText(text_label)
        self.lst_fSlider[index_cbox].SetValue(initial_value)
        
    def SetCheckBoxState(self, obj_name, state):
        if state == QtCore.Qt.Checked:
            self.controller.SetActivityVisibility(obj_name, True)
        else:
            self.controller.SetActivityVisibility(obj_name, False)
    
    def SetSliderValue(self, obj_name, value):
        self.controller.SetFeatureWeightValue(obj_name, value * 0.01)
    
    def Show(self):
        assert(self.main_window is not None)
        self.main_window.show()