#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains the classes needed to create a Qt5 based scatter chart
using matplotlib to create the chart itself. This chart gives support for
selecting data points both individually and in convex regions of the plane.
"""

from copy import deepcopy
import numpy as np
from matplotlib import cm
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.path import Path
from matplotlib.patches import Polygon
from PyQt5.QtCore import QPoint, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QPalette
from PyQt5.QtWidgets import QSizePolicy, QToolTip

from brushableplot import BrushableCanvas


class PolygonSelection(object):
    """
    This class contains data about a group selection in the ScatterChart. All
    artists created by matplotlib (points and lines), as well as the points
    that compose the selection hull and the data points inside the hull are
    stored here."
    """

    def __init__(self, axes, data=None):
        self._axes = axes
        self._data = data
        self._hull_coords = []
        self._hull_points_art = []
        self._hull_lines_art = []
        self._polygon = None
        self._point_plot_params = {'marker': '+', 'c': 'gray'}
        self._line_plot_params = {
            'linestyle': 'dashed', 'linewidth': 3.0, 'c': 'gray'}

    def __del__(self):
        self._data = None
        self._hull_coords = None
        self._point_plot_params = None
        self._line_plot_params = None
        for art in self._hull_points_art:
            self.axes.collections.remove(art)
        for art in self._hull_lines_art:
            self.axes.lines.remove(art)
        self._hull_points_art = None
        self._hull_lines_art = None

    @property
    def axes(self):
        return self._axes

    @property
    def hull_coords(self):
        return self._hull_coords

    @property
    def polygon(self):
        return self._polygon

    def set_data(self, data):
        self._data = data

    def add_hull_point(self, coords):
        """
        Adds a new point to the hull. This new point is appended to a list of
        hull points.

        Parameters
        ----------
        coords : list
            A list with the X and Y data coordinates of the new point.
        """
        self._hull_coords.append(coords)
        art_p = self.axes.scatter(
            coords[0], coords[1], **self._point_plot_params)
        self._hull_points_art.append(art_p)

        if len(self.hull_coords) > 1:
            xcoord = [self.hull_coords[-2][0], self.hull_coords[-1][0]]
            ycoord = [self.hull_coords[-2][1], self.hull_coords[-1][1]]
            art_l = self.axes.plot(xcoord, ycoord, **self._line_plot_params)
            self._hull_lines_art.extend(art_l)

    def move_hull_point(self, pidx, new_coords):
        """
        Moves a hull point to new coordinates. Raises ValueError exception if
        the index is out of range.

        Parameters
        ----------
        pidx: int
            The index of the point to be removed.
        """
        if pidx < 0 or pidx > len(self.hull_coords):
            raise ValueError(
                'Index out of range (0, {})'.format(len(self.hull_coords)))

    def del_hull_point(self, pidx):
        """
        Removes a point from the hull. Raises ValueError exception if the
        index is out of range.

        Parameters
        ----------
        pidx: int
            The index of the point to be removed.
        """
        if pidx < 0 or pidx > len(self.hull_coords):
            raise ValueError(
                'Index out of range (0, {})'.format(len(self.hull_coords)))

    def finish_hull(self):
        """
        Method to close the hull and calculate the set of data points inside
        it. Returns a list of indices of points inside the hull.
        """
        # First, we close the hull.
        xcoord = [self.hull_coords[-1][0], self.hull_coords[0][0]]
        ycoord = [self.hull_coords[-1][1], self.hull_coords[0][1]]
        art_l = self.axes.plot(xcoord, ycoord, **self._line_plot_params)
        self._hull_lines_art.extend(art_l)
        self.axes.figure.canvas.draw()

        # Now we build a matplotlib.patches.Polygon and test the data points.
        self._polygon = Polygon(np.array(self.hull_coords))

        inside = []
        for i in range(self._data.shape[0]):
            if self.polygon.contains_point(self._data[i, :]):
                inside.append(i)

        return inside


class ScatterChart(FigureCanvas, BrushableCanvas):
    """
    This class builds a scatter chart of the given data points. It also handles
    data selection (brushing and linking) and tooltips.
    """

    MOUSE_BUTTONS = {'LEFT': 1, 'MID': 2, 'RIGHT': 3}

    def __init__(self, canvas_name, parent, width=5, height=5, dpi=100,
                 **kwargs):
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
        self._tooltip_enabled = True
        self._region_selection_enabled = False
        self._cmap_name = 'rainbow'
        self._plot_title = self.base_plot_name()
        self._xaxis_label = 'Axis 1'
        self._yaxis_label = 'Axis 2'
        self._point_names = None
        self._point_artists = None
        self._points_colors = {}
        self._selection_finished = False

        # Point plot parameters. Adding missing parameters if needed.
        self._plot_params = kwargs
        if 'picker' not in self._plot_params:
            self._plot_params['picker'] = 3.0
        if 's' not in self._plot_params:
            self._plot_params['s'] = 40

        # Convex hull attributes.
        self._chull = []  # Convex hull in data coordinates
        # Convex hull artists
        self._chull_points_art = []
        self._chull_lines_art = []
        self._chulls = []

        # Callback IDs
        self._cb_mouse_move_id = None
        self._cb_mouse_press_id = None
        self._cb_pick_id = None
        self._cb_scrollwheel_id = None
        self._cb_axes_leave_id = None
        self._cb_fig_leave_id = None

        self._connect_cb()

    # -------------------------------------------------------------------------
    # Signals
    # -------------------------------------------------------------------------
    tooltip_drawn = pyqtSignal(str, int)

    # -------------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------------
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
        """
        Returns the X axis label for this plot.
        """
        return self._xaxis_label

    @property
    def yaxis_label(self):
        """
        Returns the Y axis label for this plot.
        """
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

    @property
    def region_selection_enabled(self):
        """
        Returns wheter the region selection option is activated.
        """
        return self._region_selection_enabled

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
            raise ValueError(
                'Data is not bidimensional, this is a 2D plot only.')

        self._data = data

        # Reseting the highlighted data
        self.highlight_data(self._highlighted_data,
                            erase=True, update_chart=False)

        if update_chart:
            self.update_chart(data_changed=True)

    def set_point_names(self, point_names):
        """
        Sets the names of the points to shown when the tooltip is rendered. If
        set to None, then the tooltip will be disabled, however, tooltip
        related events will still be emitted. No checking is done to see if the
        amount of names is the same as the number of points. It is the user's
        duty to check this.

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

    def set_tooltip_state(self, enable):
        """
        Sets wheter the tooltip will be shown when the mouse hovers a data
        point.

        Parameters
        ----------
        enable: boolean
            True to enable, False to disable.
        """
        self._tooltip_enabled = enable

    def set_region_selection_state(self, state):
        """
        Sets wheter the region selection option is activated (True) or not
        (False). Region selection is done by drawing a polygon around the
        points of interest, all points within that polygon are considered
        selected once the selection is confirmed by the user.
        """
        self._region_selection_enabled = state
        fig = self.figure
        if state:
            if self._cb_pick_id:
                fig.canvas.mpl_disconnect(self._cb_pick_id)
                self._cb_pick_id = None

            self._cb_mouse_press_id = fig.canvas.mpl_connect(
                'button_press_event', self.cb_mouse_press_event)
        else:
            if self._cb_mouse_press_id:
                fig.canvas.mpl_disconnect(self._cb_mouse_press_id)
                self._cb_mouse_press_id = None

            self._cb_pick_id = fig.canvas.mpl_connect(
                'pick_event', self.cb_pick_event)

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
        if ('selection_changed' in kwargs and
                kwargs['selection_changed'] is True):
            # First, if there is selected data, we make the background points
            # more transparent. If there is not, we restore their full
            # opacity.
            bg_alpha = 0.15
            if not self.highlighted_data:
                bg_alpha = 1.0
            for col in self._point_artists:
                col.set_alpha(bg_alpha)

            # Then, we highlight the selected data with a higher opacity.
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

            plot_params = deepcopy(self._plot_params)
            for i, p in enumerate(self.data):
                plot_params['c'] = self._points_colors[i]
                self._point_artists[i] = self.axes.scatter(
                    x=p[0], y=p[1], **plot_params)
            plot_params = None

            self.update_chart(selection_changed=True)

        self.draw()

    def cb_mouse_motion_event(self, event):
        """
        Callback to process a mouse movement event.

        This method checks if the mouse cursor is over a data point and, if
        True, then it plots a tooltip (if enabled) and emits a tooltip_drawn
        signal.

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
                pos = self.mapToGlobal(
                    QPoint(event.x, self.height() - event.y))
                QToolTip.showText(pos, '{}'.format(
                    self.point_names[hover_idx]))
                self.tooltip_drawn.emit(self.name, hover_idx)
            else:
                QToolTip.hideText()

        self.draw()

    def cb_mouse_press_event(self, event):
        if event.button == ScatterChart.MOUSE_BUTTONS['LEFT']:
            if not self._chulls:
                self._chulls = [PolygonSelection(self.axes, self.data)]
            poly = self._chulls[-1]
            poly.add_hull_point([event.xdata, event.ydata])

        elif event.button == ScatterChart.MOUSE_BUTTONS['MID']:
            idx = None
            for i, hull in enumerate(self._chulls):
                if not hull.hull_coords:
                    continue
                contains = hull.polygon.contains_point(
                    [event.xdata, event.ydata])
                if contains:
                    idx = i
                    break
            if idx is not None:
                del self._chulls[idx]

        elif event.button == ScatterChart.MOUSE_BUTTONS['RIGHT']:
            to_highlight = self._chulls[-1].finish_hull()
            self._chulls.append(PolygonSelection(self.axes, self.data))
            self.highlight_data(to_highlight, erase=False, update_chart=True)

        self.draw()

    def cb_pick_event(self, event):
        """
        This method processes a picking event. The highlighted point is marked
        and a notification is sent to the parent widget.
        """
        if event.mouseevent.button == ScatterChart.MOUSE_BUTTONS['LEFT']:
            to_erase = []
            to_highlight = []
            for i, art in enumerate(self._point_artists):
                contains, _ = art.contains(event.mouseevent)
                if contains:
                    if i in self.highlighted_data:
                        to_erase.append(i)
                    else:
                        to_highlight.append(i)
            self.highlight_data(to_erase, erase=True, update_chart=False)
            self.highlight_data(to_highlight, erase=False, update_chart=True)
            self.notify_parent()
            self.draw()

    def cb_mouse_scroll_event(self, event):
        """
        This method processes scroll wheel events. (zoom)
        """
        pass

    # ------------------------------------------------------------------------
    # Private methods
    # ------------------------------------------------------------------------
    def _connect_cb(self):
        """
        Connects the callbacks to the matplotlib canvas.
        """
        fig = self.figure
        if self.region_selection_enabled:
            self._cb_pick_id = fig.canvas.mpl_connect(
                'pick_event', self.cb_pick_event)
        else:
            self._cb_mouse_press_id = fig.canvas.mpl_connect(
                'button_press_event', self.cb_mouse_press_event)

        self._cb_mouse_move_id = fig.canvas.mpl_connect(
            'motion_notify_event', self.cb_mouse_motion_event)
        self._cb_scrollwheel_id = fig.canvas.mpl_connect(
            'scroll_event', self.cb_mouse_scroll_event)
        # self._cb_axes_leave_id = fig.canvas.mpl_connect(
        #    'axes_leave_event', self.cb_axes_leave)
        # self._cb_fig_leave_id = fig.canvas.mpl_connect(
        #    'figure_leave_event', self.cb_axes_leave)

    def _disconnect_cb(self):
        """
        Detaches the callbacks from the matplotlib canvas.
        """
        fig = self.figure
        if self._cb_mouse_move_id:
            fig.canvas.mpl_disconnect(self._cb_mouse_move_id)
            self._cb_mouse_move_id = None
        if self._cb_mouse_press_id:
            fig.canvas.mpl_disconnect(self._cb_mouse_press_id)
            self._cb_mouse_press_id = None
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
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QComboBox,
                                 QLineEdit, QPushButton, QVBoxLayout,
                                 QHBoxLayout, QFormLayout, QCheckBox, QLabel,
                                 QStyleFactory)
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
            'Terrain': 'terrain',
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
            state = (enable == Qt.Checked)
            self.chart.set_tooltip_state(state)

        def set_region_selection_state(self, enable):
            state = (enable == Qt.Checked)
            self.chart.set_region_selection_state(state)

        def cb_tooltip(self, name, idx):
            print("Plot {} hovered the mouse over point {}".format(name, idx))

        def set_brushed_data(self, child_name, obj_ids):
            print('widget {} brushed some objects.'.format(child_name))
            print('Objects:\n\t', obj_ids)

        def update_data(self):
            self.points = np.random.normal(size=(self.num_points, 2))
            point_names = ['Points-' + str(i + 1)
                           for i in range(self.points.shape[0])]
            self.chart.set_data(self.points)
            self.chart.set_point_names(point_names)

        def buildUI(self):
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)

            self.chart = ScatterChart(parent=self,
                                      canvas_name='scatter1',
                                      s=40)

            self.chart.tooltip_drawn.connect(self.cb_tooltip)

            rand_data = QPushButton('Generate new data', self)
            rand_data.clicked.connect(self.update_data)
            enable_tooltip = QCheckBox('Tooltip enabled', self)
            enable_tooltip.setChecked(self.chart.tooltip_enabled)
            enable_tooltip.stateChanged.connect(self.set_tooltip_enabled)
            enable_region_sel = QCheckBox('Region selection', self)
            enable_region_sel.setChecked(self.chart.region_selection_enabled)
            enable_region_sel.stateChanged.connect(
                self.set_region_selection_state)
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
            form_layout.addRow(
                QLabel('Plot title', self.main_widget), plot_title)
            form_layout.addRow(
                QLabel('X axis label', self.main_widget), xaxis_label)
            form_layout.addRow(
                QLabel('Y axis label', self.main_widget), yaxis_label)

            panel_layout = QVBoxLayout(self.main_widget)
            panel_layout.addLayout(form_layout)
            panel_layout.addWidget(enable_tooltip)
            panel_layout.addWidget(enable_region_sel)
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
