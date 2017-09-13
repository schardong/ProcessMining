#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import cm
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QSizePolicy, QToolTip
from PyQt5.QtGui import QFont, QPalette, QColor

from brushableplot import BrushableCanvas

class ScatterChart(FigureCanvas, BrushableCanvas):
    """
    This class builds a scatter chart of the given data points. It also handles
    data selection (brushing and linking) and tooltips.
    """

    def __init__(self, canvas_name, parent, width=5, height=5, dpi=100, **kwargs):
        """
        Default constructor.

        Parameters
        ----------
        canvas_name: str
            The canvas name. Used when notifying other objects of changes.
        parent: Qt5.QWidget
            The parent widget. The parent widget must implement the
            'set_brush_data' method, which receives the canvas name and a list
            of highlighted objects as parameters.
        width: int
            The canvas width. Default value is 5 inches
        height: int
            The canvas height. Default value is 5 inches
        dpi: int
            The canvas' resolution. Default value is 100
        kwargs:
            Other keyword arguments
        """
        fig = Figure(figsize=(width, height), dpi=dpi)
        self._axes = fig.add_subplot(1, 1, 1)
        FigureCanvas.__init__(self, fig)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.setParent(parent)
        BrushableCanvas.__init__(self, canvas_name, parent)

        # Data and plot style setup
        self._data = None
        self._pointnames = None
        self._tooltip_enabled = True
        self._cmap_name = 'rainbow'
        self._plot_title = self.base_plot_name()
        self._xaxis_label = 'Axis 1'
        self._yaxis_label = 'Axis 2'
        self._point_names = None
        self._point_artists = None
        self._points_colors = {}
        self._plot_params = kwargs
        if 'picker' not in self._plot_params:
            self._plot_params['picker'] = 3
        if 's' not in self._plot_params:
            self._plot_params['s'] = 40

        # Callback IDs
        self._cb_mouse_move_id = None
        self._cb_mouse_button_id = None
        self._cb_scrollwheel_id = None
        self._cb_axes_leave_id = None
        self._cb_fig_leave_id = None

        self._connect_cb()

    @classmethod
    def base_plot_name(self):
        """
        Static method that returns the base name of this plot.
        """
        return 'Scatter Chart'

    @property
    def axes(self):
        """
        Returns the axes associated to this object.

        Returns
        -------
        out: matplotlib.Axes
            The associated axes.
        """
        return self._axes

    @property
    def data(self):
        """
        Returns the points given to this instance.
        
        Returns
        -------
        out: numpy.array
            The NxD point matrix. N is the number of points and D is the
            number of dimensions (2 or 3).
        """
        return self._data

    @property
    def point_names(self):
        """
        Returns the names of the data-points given by the user.
        """
        return self._point_names

    @property
    def plot_title(self):
        """
        Returns the title of this plot.
        """
        return self._plot_title

    @property
    def xaxis_label(self):
        return self._xaxis_label

    @property
    def yaxis_label(self):
        return self._yaxis_label

    @property
    def colormap_name(self):
        """
        Returns the name of the colormap being used by this chart.

        Returns
        -------
        out: str
            The colormap's name.
        """
        return self._cmap_name

    @property
    def tooltip_enabled(self):
        """
        Returns wheter the tooltip is enabled or not.
        """
        return self._tooltip_enabled

    def set_data(self, data, update_chart=True):
        """
        Defines the points to be plotted.

        Parameters
        ----------
        data: numpy.array
            The Nx2 matrix of points to be plotted. N is the number of points.
        update_chart: boolean
             Switch that indicates if the update_chart method should be called
             at the end of this function. Default value is True, meaning that
             the update wll be called.
        """
        if not len(data):
            raise AttributeError('Invalid data provided (Empty or None).')
        if data.shape[1] != 2:
            raise ValueError('Data is not bidimensional, this is a 2D plot only.')

        self._data = data

        #Reseting the highlighted data
        self.highlight_data(self._highlighted_data, erase=True, update_chart=False)

        if update_chart:
            self.update_chart(data_changed=True)

    def set_point_names(self, point_names):
        """
        Sets the names of the points to shown when the tooltip is rendered. If
        set to None, then the tooltip will be disabled, however, tooltip related
        events will still be emitted. No checking is done to see if the amount
        of names is the same as the number of points. It is the user's duty to
        check this.

        Parameters
        ----------
        point_names: list of strings
            A list of names for the given data points. Used to render the
            tooltip.
        """
        self._point_names = point_names

    def set_plot_title(self, title, update_chart=True):
        """
        Sets the title of this plot.

        Parameters
        ----------
        title: str
            This plot's title.
        update_chart: boolean
            Switch to indicate if the chart should be updated at the end of
            the method.
        """
        self._plot_title = title
        if update_chart:
            self.update_chart(data_changed=True)

    def set_xaxis_label(self, lbl, update_chart=True):
        """
        Sets the label for the X axis of this plot.

        Parameters
        ----------
        lbl: str
            This plot's X axis label.
        update_chart: boolean
            Switch to indicate if the chart should be updated at the end of
            the method.
        """
        self._xaxis_label = lbl
        if update_chart:
            self.update_chart(data_changed=True)

    def set_yaxis_label(self, lbl, update_chart=True):
        """
        Sets the label for the Y axis of this plot.

        Parameters
        ----------
        lbl: str
            This plot's Y axis label.
        update_chart: boolean
            Switch to indicate if the chart should be updated at the end of
            the method.
        """
        self._yaxis_label = lbl
        if update_chart:
            self.update_chart(data_changed=True)

    def set_colormap(self, cmap_name, update_chart=True):
        """
        Sets the colormap function to use when plotting.

        Parameters
        ----------
        cmap_name: str
        update_chart: boolean
            Switch to indicate if the plot should be updated. Default value
            is True.
        """
        self._cmap_name = cmap_name
        if update_chart:
            self.update_chart(data_changed=True)

    def set_tooltip_enabled(self, enable):
        """
        Sets wheter the tooltip will be shown when the mouse hovers a data point.
        enable: boolean
            True to enable, False to disable.
        """
        self._tooltip_enabled = enable

    def update_chart(self, **kwargs):
        """
        Selectively updates the plot based on the keywords arguments provided.

        Parameters
        ----------
        kwargs: Other keyword arguments
            data_changed: boolean - Indicates if the data was changes since the
                                    last update.
            selection_changed: boolean - Indicates if new data were selected.
        """
        if 'selection_changed' in kwargs and kwargs['selection_changed'] is True:
            bg_alpha = 0.3
            if not self.highlighted_data:
                bg_alpha = 1.0
            for col in self.axes.collections:
                col.set_alpha(bg_alpha)
            for i in self.highlighted_data:
                self.axes.collections[i].set_alpha(1.0)

        if 'data_changed' in kwargs and kwargs['data_changed'] is True:
            self.axes.cla()
            self.axes.set_title(self.plot_title)
            self.axes.set_xlabel(self.xaxis_label)
            self.axes.set_ylabel(self.yaxis_label)

            self._point_artists = [None] * self.data.shape[0]
            colormap = cm.get_cmap(name=self.colormap_name,
                                   lut=len(self.data))
            self._points_colors = dict((i, colormap(i))
                                       for i in range(len(self.data)))

            plot_params = self._plot_params
            for i, p in enumerate(self.data):
                plot_params['c'] = self._points_colors[i]
                self._point_artists[i] = self.axes.scatter(x=p[0], y=p[1], **plot_params)

            self.update_chart(selection_changed=True)

        self.draw()

    def cb_mouse_motion(self, event):
        """
        Callback to process a mouse movement event.

        If the group selection option is enabled, then any points with
        Y-coordinate less than the cursor's Y-coordinate will be marked in a
        different opacity level, but not highlighted. If the user clicks with
        the mouse, then the points will be highlighted, but this event is
        processed in another method.

        This method also processes tooltip-related events when the group
        selection is disabled. If the user hovers the mouse cursor over a data
        point, then the name associated to that point will be shown in a
        tooltip.

        Parameters
        ----------
        event: matplotlib.backend_bases.MouseEvent
            Data about the event.
        """
        # Restoring the points' original size.
        if self._point_artists:
            for art in self._point_artists:
                if art is None:
                    continue
                art.set_sizes([self._plot_params['s']])

        if event.xdata is None or event.ydata is None:
            return False

        # Testing if the cursor is over a point. If it is, we plot the
        # tooltip and notify this event by calling the registered
        # callback, if any.
        if not self.point_names:
            return False
        else:
            hover_idx = None
            for i, art in enumerate(self._point_artists):
                if not art:
                    continue
                contains, _ = art.contains(event)
                if contains:
                    art.set_sizes([self._plot_params['s'] * 3])
                    if i > len(self.point_names):
                        return False
                    hover_idx = i
                    break

            if hover_idx is not None and self.tooltip_enabled:
                palette = QPalette()
                palette.setColor(QPalette.ToolTipBase, QColor(252, 243, 207))
                palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
                QToolTip.setPalette(palette)
                QToolTip.setFont(QFont('Arial', 14, QFont.Bold))
                pos = self.mapToGlobal(QPoint(event.x, self.height() - event.y))
                QToolTip.showText(pos, '{}'.format(self.point_names[hover_idx]))
            else:
                QToolTip.hideText()

            #if self._cb_notify_tooltip:
            #    self._cb_notify_tooltip(self.name, hover_idx)

    def cb_mouse_button(self, event):
        pass

    def cb_mouse_scroll(self, event):
        pass

    #--------------------------------------------------------------------------
    # Private methods
    #--------------------------------------------------------------------------
    def _connect_cb(self):
        """
        Connects the callbacks to the matplotlib canvas.
        """
        fig = self.figure
        self._cb_mouse_move_id = fig.canvas.mpl_connect(
            'motion_notify_event', self.cb_mouse_motion)
        self._cb_mouse_button_id = fig.canvas.mpl_connect(
            'button_press_event', self.cb_mouse_button)
        self._cb_scrollwheel_id = fig.canvas.mpl_connect(
            'scroll_event', self.cb_mouse_scroll)
        #self._cb_axes_leave_id = fig.canvas.mpl_connect(
        #    'axes_leave_event', self.cb_axes_leave)
        #self._cb_fig_leave_id = fig.canvas.mpl_connect(
        #    'figure_leave_event', self.cb_axes_leave)

    def _disconnect_cb(self):
        """
        Detaches the callbacks from the matplotlib canvas.
        """
        fig = self.figure
        if self._cb_mouse_move_id:
            fig.canvas.mpl_disconnect(self._cb_mouse_move_id)
            self._cb_mouse_move_id = None
        if self._cb_mouse_button_id:
            fig.canvas.mpl_disconnect(self._cb_mouse_button_id)
            self._cb_mouse_button_id = None
        if self._cb_scrollwheel_id:
            fig.canvas.mpl_disconnect(self._cb_scrollwheel_id)
            self._cb_scrollwheel_id = None
        if self._cb_axes_leave_id:
            fig.canvas.mpl_disconnect(self._cb_axes_leave_id)
            self._cb_axes_leave_id = None
        if self._cb_fig_leave_id:
            fig.canvas.mpl_disconnect(self._cb_fig_leave_id)
            self._cb_fig_leave_id = None

def main():
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QComboBox, QLineEdit,
                                 QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QSlider,
                                 QMessageBox, QCheckBox, QLabel, QStyleFactory)
    from PyQt5 import QtCore
    from PyQt5.QtCore import Qt
    import sys

    """
    Simple test function for the ScatterChart class.
    """
    class TestWidget(QMainWindow):
        """
        Qt derived class to embed our chart.
        """

        COLORMAPS = {
            'Rainbow': 'rainbow',
            'Winter': 'winter',
            'Summer': 'summer',
            'Topological': 'gist_earth',
            'Ocean': 'ocean',
            'Gist Stern': 'gist_stern',
            'Terrain':'terrain',
            'Blue to Magenta': 'cool',
        }

        COLORMAPS_ORDER = [
            'Rainbow',
            'Topological',
            'Ocean',
            'Terrain',
            'Blue to Magenta',
            'Gist Stern',
            'Winter',
            'Summer',
        ]
        
        def __init__(self):
            super().__init__()
            self.left = 0
            self.top = 0
            self.title = 'ScatterChart test'
            self.width = 600
            self.height = 400
            self.chart = None
            self.points = None
            self.main_widget = None
            self.num_points = 30

            self.setFocusPolicy(QtCore.Qt.WheelFocus)
            self.buildUI()
            self.update_data()

        def set_num_points(self, num_points):
            self.num_points = num_points
            self.update_data()

        def set_plot_title(self, title):
            self.chart.set_plot_title(title)

        def set_xaxis_label(self, lbl):
            self.chart.set_xaxis_label(lbl)

        def set_yaxis_label(self, lbl):
            self.chart.set_yaxis_label(lbl)

        def set_colormap(self, cm_name):
            self.chart.set_colormap(self.COLORMAPS[cm_name])

        def set_tooltip_enabled(self, enable):
            state = False
            if enable == Qt.Checked:
                state = True
            self.chart.set_tooltip_enabled(state)
            
        def update_data(self):
            self.points = np.random.normal(size=(self.num_points, 2))
            point_names = ['Points-' + str(i+1) for i in range(self.points.shape[0])]
            self.chart.set_data(self.points)
            self.chart.set_point_names(point_names)

        def buildUI(self):
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)

            self.chart = ScatterChart(parent=self,
                                      canvas_name='scatter1',
                                      s=40)

            rand_data = QPushButton('Generate new data', self)
            rand_data.clicked.connect(self.update_data)
            enable_tooltip = QCheckBox('Tooltip enabled', self)
            enable_tooltip.setChecked(self.chart.tooltip_enabled)
            enable_tooltip.stateChanged.connect(self.set_tooltip_enabled)
            colormap = QComboBox(self)
            for k in self.COLORMAPS_ORDER:
                colormap.addItem(k)
            colormap.currentTextChanged.connect(self.set_colormap)
            plot_title = QLineEdit(self.chart.plot_title, self)
            plot_title.textChanged.connect(self.set_plot_title)
            xaxis_label = QLineEdit(self.chart.xaxis_label, self)
            xaxis_label.textChanged.connect(self.set_xaxis_label)
            yaxis_label = QLineEdit(self.chart.yaxis_label, self)
            yaxis_label.textChanged.connect(self.set_yaxis_label)
            

            self.main_widget = QWidget(self)
            l = QHBoxLayout(self.main_widget)

            form_layout = QFormLayout(self.main_widget)
            form_layout.addRow(QLabel('Colormap', self.main_widget), colormap)
            form_layout.addRow(QLabel('Plot title', self.main_widget), plot_title)
            form_layout.addRow(QLabel('X axis label', self.main_widget), xaxis_label)
            form_layout.addRow(QLabel('Y axis label', self.main_widget), yaxis_label)
            
            panel_layout = QVBoxLayout(self.main_widget)
            panel_layout.addLayout(form_layout)
            panel_layout.addWidget(enable_tooltip)
            panel_layout.addWidget(rand_data)
            
            l.addWidget(self.chart)
            l.addLayout(panel_layout)

            self.setFocus()
            self.setCentralWidget(self.main_widget)

    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    app = QApplication(sys.argv)
    ex = TestWidget()
    ex.show()
    sys.exit(app.exec_())
            
if __name__ == '__main__':
    main()
