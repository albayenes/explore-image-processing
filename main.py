from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 500, 300)
        self.setWindowTitle("Experimental Image Processing Tool")

        self._createMenuBar()
        self.initUI()

    def initUI(self):
        pass

    def _createMenuBar(self):
        menu_bar = self.menuBar()

        file_menu = QMenu("&File", self)
        edit_menu = QMenu("&Edit", self)
        help_menu = QMenu("&Help", self)

        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(edit_menu)
        menu_bar.addMenu(help_menu)


def window():
    # Setup application for operating system
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()

    sys.exit(app.exec_())


window()
