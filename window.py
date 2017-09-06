# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designerwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

import sys
import matplotlib
matplotlib.use("Qt5Agg")

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMenu, QVBoxLayout, QMessageBox, QWidget

from uielements import ActivityCheckBox, SliderFeatureController

from fcprojectionchart import ProjectionChart

class MainWindow(QtWidgets.QMainWindow):
    def __init__ (self, vpf_controller):
        super(MainWindow, self).__init__()
        self.controller = vpf_controller
     
    def setupUi (self):
        self.main_widget = QtWidgets.QWidget(self)
        
        self.setObjectName("MainWindow")
        self.resize(978, 667)
        
        # Global Horizontal Layout (All window)
        self.CentralHLayout = QtWidgets.QWidget(self)
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
        ## MatPlot Creation
        self.chart = ProjectionChart(self.main_widget, width=5, height=4, dpi=100)
        self.chart.setObjectName("chart")
        
        # Add MatPlot into the LeftVLayout
        self.LeftVLayout.addWidget(self.chart)
        
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
        self.sld_numberofcases = QtWidgets.QSlider(self.CentralHLayout)
        self.sld_numberofcases.setOrientation(QtCore.Qt.Vertical)
        self.sld_numberofcases.setObjectName("sld_numberofcases")
        
        # valueChanged()   Emitted when the slider's value has changed. The tracking() determines whether this signal is emitted during user interaction.
        # sliderPressed() Emitted when the user starts to drag the slider.
        # sliderMoved()   Emitted when the user drags the slider.
        # Emitted when the user releases the slider.
        self.sld_numberofcases.sliderReleased.connect(self.setNumberOfCases)
        
        # Add Vertical Slider into the right horizontal Layout
        self.RightHLayout.addWidget(self.sld_numberofcases)
        
        
        # Add LeftVLayout to the Global Horizontal Layout
        self.horizontalLayout.addLayout(self.LeftVLayout)
        # Add RightVLayout to the Global Horizontal Layout
        self.horizontalLayout.addLayout(self.RightHLayout)
        
        # Add Central Horizontal Layout into the MainWindow
        self.setCentralWidget(self.CentralHLayout)
        
        # Menu Bar Creation
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 978, 21))
        self.menubar.setObjectName("menubar")
        
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        
        # Action attached to "Quit" menu item
        self.actionQuit = QtWidgets.QAction(self)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.triggered.connect(self.QuitApplication)
        
        self.actionRemove_Checkbox = QtWidgets.QAction(self)
        self.actionRemove_Checkbox.setObjectName("actionRemove_Checkbox")
        self.actionRemove_Checkbox.triggered.connect(self.removeCheckboxFromMain)


        self.menuFile.addAction(self.actionRemove_Checkbox)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
                    
    def retranslateUi (self):
        _translate = QtCore.QCoreApplication.translate
        
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        # Update Check Box Activity Names
        for i in range(len(self.lst_aCheckBox)):
            self.lst_aCheckBox[i].UpdateLabel(_translate)
        
        # Update Slider Feature Names        
        for i in range(len(self.lst_fSlider)):
            self.lst_fSlider[i].UpdateLabel(_translate)
        
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionRemove_Checkbox.setText(_translate("MainWindow", "Remove Checkbox"))

    # Remove CheckBox From MainWindow
    def removeCheckboxFromMain (self):
        if len(self.lst_aCheckBox) > 0:
            self.lst_aCheckBox[0].RemoveWidget()
            self.lst_aCheckBox[0] = None
            self.lst_aCheckBox.remove(self.lst_aCheckBox[0])
        
    # Quit Application
    def QuitApplication (self):
        ret_mbox = QtWidgets.QMessageBox.question(self, "Quit","Are you sure?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) 
        if ret_mbox == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def GetProjectionChart (self):
        assert(self.chart is not None)
        return self.chart
    
    def Show (self):
        self.show()
    
    #-----------------------------------------------
    # Activities visibility checkbox functions    
    #-----------------------------------------------
    # Add a new Activity CheckBox
    def AddActivityCheckBox (self, obj_name, text_label):
        assert(self.widget_cbx_hor_layout is not None and self.layout_hor_cbx is not None and self.lst_aCheckBox is not None)
        
        index_cbox = len(self.lst_aCheckBox)
        
        self.lst_aCheckBox.append(ActivityCheckBox(obj_name, self.widget_cbx_hor_layout, self.SetCheckBoxState))
        self.lst_aCheckBox[index_cbox].AddWidget(self.layout_hor_cbx)
        self.lst_aCheckBox[index_cbox].SetText(text_label)
        self.lst_aCheckBox[index_cbox].SetCheckState(QtCore.Qt.Checked)
    
    def SetCheckBoxState (self, obj_name, state):
        if state == QtCore.Qt.Checked:
            self.controller.SetActivityVisibility(obj_name, True)
        else:
            self.controller.SetActivityVisibility(obj_name, False)

    #-----------------------------------------------
    # Feature weight slider functions    
    #-----------------------------------------------
    def AddFeatureSlider (self, obj_name, text_label, initial_value):
        assert(self.lay_ver_features is not None and self.verticalLayout is not None and self.lst_fSlider is not None)
                
        index_cbox = len(self.lst_fSlider)
        
        self.lst_fSlider.append(SliderFeatureController(obj_name, self.lay_ver_features, self.verticalLayout, self.SetSliderValue))
        #self.lst_fSlider[index_cbox].AddWidget(self.layout_hor_cbx)
        self.lst_fSlider[index_cbox].SetText(text_label)
        self.lst_fSlider[index_cbox].SetValue(initial_value)
    
    def SetSliderValue (self, obj_name, value):
        #print("SetSliderValue", obj_name, value)
        self.controller.SetFeatureWeightValue(obj_name, value)
        
    #----------------------------------
    # number of cases slider functions    
    #----------------------------------
    # set the current range of the slider
    def setMaxNumberOfCases (self, n_max_cases):
        assert(self.sld_numberofcases is not None)
        self.sld_numberofcases.setRange(0, n_max_cases)
    
    # set the current number of cases, but did not call the update from controller
    def setCurrentNumberOfCases (self, n_cases):
        assert(self.sld_numberofcases is not None)
        self.sld_numberofcases.setValue(n_cases)
        #self.controller.updateNumberOfCases(n_cases)
        
    ## SIGNAL
    # signal received from the 'sliderReleased' callback
    def setNumberOfCases (self):
        #print("Set Number Of Cases Called!", self.sld_numberofcases.value())
        self.controller.updateNumberOfCases(self.sld_numberofcases.value())

    #---------------
    # input callbacks
    #---------------
    # Keyboard callback
    def keyPressEvent (self, ev):
        print("MainWindow key press", ev.key)