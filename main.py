from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction
from PyQt5.QtGui import QIcon
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 500, 300)
        self.setWindowTitle("Experimental Image Processing Tool")

        self._createActions()
        self._createMenuBar()
        self.initUI()

    def initUI(self):
        pass

    def _createActions(self):
        # Creating action using the first constructor
        self.newAction = QAction(self)
        self.newAction.setText("&New")
        # Creating actions using the second constructor
        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("C&ut", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)

    def _createMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = QMenu("&File", self)
        editMenu = QMenu("&Edit", self)
        helpMenu = QMenu("&Help", self)

        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)

        menuBar.addMenu(editMenu)
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)

        menuBar.addMenu(helpMenu)
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)


def window():
    # Setup application for operating system
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()

    sys.exit(app.exec_())


window()
