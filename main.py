import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QMenu, QAction, QFileDialog, QHBoxLayout, \
    QLabel, QListWidget, QListWidgetItem, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize


class ImageListWidgetItem(QListWidgetItem):
    """ ImageListWidgetItem(pathToImage = str) """
    def __init__(self, *args):
        super(ImageListWidgetItem, self).__init__(*args)
        self.pathToImage = None

    def setImagePath(self, path):
        self.imagePath_ = path

    def getImagePath(self):
        return self.imagePath_


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # This variable will be used to remember last directory
        self.openDir = ''
        self.setGeometry(200, 200, 500, 300)
        self.setWindowTitle("Experimental Image Processing Tool")

        self.initUI()
        self._createActions()
        self._createMenuBar()
        self._connectActions()


    def initUI(self):

        self.imageListWidget = QListWidget()
        self.imageListWidget.setViewMode(QListWidget.IconMode)
        self.imageListWidget.setIconSize(QSize(128, 128))
        self.imageListWidget.setResizeMode(QListWidget.Adjust)
        self.imageListWidget.setFixedWidth(156)
        self.centralLabel = QLabel()

        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.addWidget(self.imageListWidget, 0)
        self.hBoxLayout.addWidget(self.centralLabel, 1)

        mainWidget = QWidget()
        mainWidget.setLayout(self.hBoxLayout)
        self.setCentralWidget(mainWidget)

        self.imageListWidget.itemSelectionChanged.connect(self.changeLabelImage)

    def _createActions(self):
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

    def changeLabelImage(self):
        print("change image of label")
        print(self.imageListWidget.currentItem().getImagePath())
        pixmap = QPixmap(self.imageListWidget.currentItem().getImagePath())
        print("change image of label")
        if (self.centralLabel.size().width() < pixmap.width()) or (self.centralLabel.size().height() < pixmap.height()):
            self.centralLabel.setPixmap(pixmap.scaled(self.centralLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.centralLabel.setPixmap(pixmap)



    def openFile(self):
        # set default directory path
        if self.openDir == '':
            self.openDir = 'c:\\'
        # Logic for opening an existing file goes here...
        filename = QFileDialog.getOpenFileName(self, self.tr('Open file'), self.openDir, "Image files (*.jpg *.jpeg *.gif *.png)")
        print(filename)
        p = Path(filename[0])
        self.openDir = str(p.parent)
        imagePath = filename[0]
        self.centralLabel.setAlignment(Qt.AlignCenter)
        print(filename)
        item = ImageListWidgetItem(QIcon(imagePath), p.name)
        item.setImagePath(filename[0])
        print(filename)
        self.imageListWidget.addItem(item)
        self.imageListWidget.setCurrentItem(item)

        print(filename)

    def saveFile(self):
        # Logic for saving a file goes here...
        self.centralWidget.setText("<b>File > Save</b> clicked")

    def copyContent(self):
        # Logic for copying content goes here...
        self.centralWidget.setText("<b>Edit > Copy</b> clicked")

    def pasteContent(self):
        # Logic for pasting content goes here...
        self.centralWidget.setText("<b>Edit > Paste</b> clicked")

    def cutContent(self):
        # Logic for cutting content goes here...
        self.centralWidget.setText("<b>Edit > Cut</b> clicked")

    def helpContent(self):
        # Logic for launching help goes here...
        self.centralWidget.setText("<b>Help > Help Content...</b> clicked")

    def about(self):
        # Logic for showing an about dialog content goes here...
        self.centralWidget.setText("<b>Help > About...</b> clicked")

    def _connectActions(self):
        # Connect File actions
        self.openAction.triggered.connect(self.openFile)
        self.saveAction.triggered.connect(self.saveFile)
        self.exitAction.triggered.connect(self.close)
        # Connect Edit actions
        self.copyAction.triggered.connect(self.copyContent)
        self.pasteAction.triggered.connect(self.pasteContent)
        self.cutAction.triggered.connect(self.cutContent)
        # Connect Help actions
        self.helpContentAction.triggered.connect(self.helpContent)
        self.aboutAction.triggered.connect(self.about)

def window():
    # Setup application for operating system
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()

    sys.exit(app.exec_())


window()
