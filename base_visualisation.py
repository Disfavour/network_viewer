from mayavi import mlab
from PyQt5 import QtWidgets
import os
import numpy as np
from numpy import cos
from mayavi.mlab import contour3d

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pyface.qt import QtGui, QtCore
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor


class Visualization(HasTraits):
    def __init__(self, data, mode, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data[::10,::50, ::50]
        self.mode = mode
        #print(self.data)

    scene = Instance(MlabSceneModel, ())

    @on_trait_change('scene.activated')
    def update_plot(self):
        ## PLot to Show
        if self.mode == 1:
            # surface
            mlab.contour3d(self.data, colormap='gray')

            """x, y, z = np.ogrid[-3:3:60j, -3:3:60j, -3:3:60j]
            t = 0
            Pf = 0.45 + ((x * cos(t)) * (x * cos(t)) + (y * cos(t)) * (y * cos(t)) - (z * cos(t)) * (z * cos(t)))
            obj = contour3d(Pf, contours=[0], transparent=False)"""
        elif self.mode == 2:
            #plane
            mlab.volume_slice(self.data, colormap='gray')

    view = View(Item(
        'scene', editor=SceneEditor(scene_class=MayaviScene), height=250, width=300, show_label=False), resizable=True)


class MayaviQWidget(QWidget):
    def __init__(self, parent, data, mode):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.visualization = Visualization(data, mode)

        self.ui = self.visualization.edit_traits(parent=self, kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, data, mode):
        ## MAIN WINDOW
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(200, 200, 1100, 700)

        ## CENTRAL WIDGET
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        ## GRID LAYOUT
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        ## Mayavi Widget 1
        container = QWidget()
        mayavi_widget = MayaviQWidget(container, data, mode)
        self.gridLayout.addWidget(mayavi_widget)


class Vis:
    def __init__(self, arr):
        self.arr = arr

    def get_surf(self):
        """Plot iso-surfaces of volumetric data defined as a 3D array."""
        mlab.contour3d(self.arr, colormap='gray')
        mlab.show()

    def get_plane(self):
        """Plot an interactive image plane sliced through volumetric data."""
        mlab.volume_slice(self.arr, colormap='gray')
        mlab.show()


if __name__ == "__main__":
    pass
