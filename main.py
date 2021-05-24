import data
from base_visualisation import *
import clust

import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import matplotlib.pyplot as plt


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.path = None
        self.data_obj = None
        self.arr_data = None
        self.vis_obj = None
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        grid = QGridLayout()
        # grid.setSpacing(100)
        self.setLayout(grid)

        self.choose_file = QPushButton("Select file")
        self.chosen_file = QLabel("None")
        self.load = QPushButton("Load")
        self.img_label = QLabel(self)
        self.draw_surf = QPushButton("Surface")
        self.draw_plane = QPushButton("Plane")
        self.cluster = QPushButton("DBScan")
        self.cluster_aggl = QPushButton("Agglomerative")

        #self.test_btn = QPushButton("PRIKOL")

        self.choose_file.clicked.connect(self.get_chosen_file)
        self.load.clicked.connect(self.load_file)
        pixmap = QPixmap("images/logotype.png")
        self.img_label.setPixmap(pixmap)
        self.draw_surf.clicked.connect(self.get_surf)
        self.draw_plane.clicked.connect(self.get_plane)
        self.cluster.clicked.connect(self.get_dbscan)
        self.cluster_aggl.clicked.connect(self.get_agg)

        #self.test_btn.clicked.connect(self.mpl)

        grid.addWidget(self.choose_file, 0, 0)
        grid.addWidget(self.chosen_file, 1, 0, 1, 2)
        grid.addWidget(self.load, 0, 1)
        grid.addWidget(self.img_label, 0, 3, 5, 1)
        grid.addWidget(self.draw_surf, 2, 0)
        grid.addWidget(self.draw_plane, 2, 1)
        grid.addWidget(self.cluster, 3, 0)
        grid.addWidget(self.cluster_aggl, 3, 1)

        #grid.addWidget(self.test_btn, 6, 1)

        """
        btn = QPushButton('Example', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.buttonClicked)
        grid.addWidget(btn, 3, 2)
        """

        self.quit_button = QPushButton('Quit', self)
        self.quit_button.setToolTip("<b>Quit</b>")
        self.quit_button.clicked.connect(QCoreApplication.instance().quit)
        self.quit_button.resize(self.quit_button.sizeHint())
        grid.addWidget(self.quit_button, 4, 0, 1, 2)

        """
        self.tmp_label = QLabel("Lomonosov-1", self)
        combo = QComboBox(self)
        combo.addItems(["Lomonosov-1", "Lomonosov-2"])
        grid.addWidget(self.tmp_label, 1, 0)
        grid.addWidget(combo, 0, 0)
        combo.activated[str].connect(self.label_changed)
        """

        # self.setGeometry(300, 300, 300, 220)
        # self.resize(250, 150)
        self.center()
        self.setWindowTitle('network_viewer')
        self.show()

    def mpl(self):
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        #sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        sc.scatter
        self.mw = QMainWindow(self)
        self.mw.setCentralWidget(sc)
        self.mw.show()

    def get_agg(self):
        #if self.arr_data:
        cur_d = self.arr_data[0]
        labels = clust.get_labels_agg(cur_d)
        plt.scatter(cur_d[:,0], cur_d[:,1], c=labels, cmap='Paired')
        plt.show()

        """
        cur_d = self.arr_data[0]
        labels = clust.get_labels_agg(cur_d)
        plt.scatter(cur_d[:, 0], cur_d[:, 1], c=labels, cmap='Paired')
        plt.show()
        """

    def get_dbscan(self):
        #if self.arr_data:
        cur_d = self.arr_data[0]
        labels = clust.get_labels_dbscan(cur_d)
        plt.scatter(cur_d[:, 0], cur_d[:, 1], c=labels, cmap='Paired')
        plt.show()

    def get_surf(self):
        if self.vis_obj:
            MainWindow = QMainWindow(self)
            ui = Ui_MainWindow()
            ui.setupUi(MainWindow, self.arr_data, 1)
            MainWindow.show()

    def get_plane(self):
        if self.vis_obj:
            MainWindow = QMainWindow(self)
            ui = Ui_MainWindow()
            ui.setupUi(MainWindow, self.arr_data, 2)
            MainWindow.show()
    """
    @pyqtSlot()
    def get_surf(self):
        if self.vis_obj:
            self.vis_obj.get_surf()

    @pyqtSlot()
    def get_plane(self):
        if self.vis_obj:
            self.vis_obj.get_plane()
    """
    def load_file(self):
        if self.path:
            self.data_obj = data.Data(self.path)
            self.arr_data = self.data_obj.get_3d_array()
            self.vis_obj = Vis(self.arr_data)
            self.refresh_label(f"Loaded {self.path.split('/')[-1]}")

    def get_chosen_file(self):
        path = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if path:
            self.path = path
            self.refresh_label(self.path)

    def refresh_label(self, text):
        self.chosen_file.setText(text)
        self.chosen_file.adjustSize()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def buttonClicked(self):
        sender = self.sender()
        print(sender.text())
        self.statusBar().showMessage(sender.text())

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())
