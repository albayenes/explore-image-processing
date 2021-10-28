import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QMenu, QAction, QFileDialog, QHBoxLayout, \
    QLabel, QListWidget, QListWidgetItem, QWidget, \
    QStatusBar, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QImage, QColor
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QThread, QRunnable, QObject, pyqtSlot, QThreadPool


from Modules.scikit import ColorManipulation
from skimage.io import imread
import traceback, sys


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, img):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.img = img
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(self.img)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class ImageListWidgetItem(QListWidgetItem):
    """ ImageListWidgetItem(pathToImage = str) """
    def __init__(self, *args):
        super(ImageListWidgetItem, self).__init__(*args[1:])
        self.pathToImage = args[0]
        self.imageInOriginalSize = imread(self.pathToImage)


class MainWindow(QMainWindow):
    resized = pyqtSignal()
    def __init__(self):
        super(MainWindow, self).__init__()

        # This variable will be used to remember last directory
        self.openDir = ''
        self.setGeometry(200, 200, 500, 300)
        self.setWindowTitle("Experimental Image Processing Tool")
        self.threadpool = QThreadPool()

        self.initUI()
        self._createActions()
        self._scikitActions()
        self._createMenuBar()
        self._connectActions()


    def initUI(self):

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.imageListWidget = QListWidget()
        self.imageListWidget.setViewMode(QListWidget.IconMode)
        self.imageListWidget.setIconSize(QSize(128, 128))
        self.imageListWidget.setResizeMode(QListWidget.Adjust)
        self.imageListWidget.setFixedWidth(156)
        self.centralLabel = QLabel()
        self.centralLabel.setMinimumSize(100, 100)

        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.addWidget(self.imageListWidget, 0)
        self.hBoxLayout.addWidget(self.centralLabel, 1)

        mainWidget = QWidget()
        mainWidget.setLayout(self.hBoxLayout)
        self.setCentralWidget(mainWidget)

        self.imageListWidget.itemSelectionChanged.connect(self.changeLabelImage)

        self.resized.connect(self.resizeImage)

        self.statusBar.showMessage(self.tr("No image"))

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)

    def _createActions(self):
        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("C&ut", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)

    def _scikitActions(self):
        self.rgb2greyAction = QAction("RGB-to-Gray", self)

    def _createMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = QMenu("&File", self)
        editMenu = QMenu("&Edit", self)
        scikitMenu = QMenu("&Scikit", self)
        helpMenu = QMenu("&Help", self)

        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)

        menuBar.addMenu(editMenu)
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)

        menuBar.addMenu(scikitMenu)
        scikitMenu.addAction(self.rgb2greyAction)

        menuBar.addMenu(helpMenu)
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)

    def numpy2QPixmap(self, img):
        if len(img.shape) == 3:
            height, width, channel = img.shape
            bytesPerLine = 3 * width
            qImg = QImage(img, width, height,
                          bytesPerLine, QImage.Format_RGB888)
        elif len(img.shape) == 2:
            height, width = img.shape
            bytesPerLine = width
            qImg = QImage(img, width, height, bytesPerLine, QImage.Format_Indexed8)
        else:
            raise ValueError("can only convert 2D or 3D arrays")

        pixmap = QPixmap(qImg)
        self.resizeImageAccordingToWindow(pixmap)

    def resizeImageAccordingToWindow(self, pixmap):
        if (self.centralLabel.size().width() < pixmap.width()) or (self.centralLabel.size().height() < pixmap.height()):
            self.centralLabel.setPixmap(
                pixmap.scaled(self.centralLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            heightRatio = self.centralLabel.height() / pixmap.height()
            widthRatio = self.centralLabel.width() / pixmap.width()

            if heightRatio < widthRatio:
                self.statusBar.showMessage("Zoom ratio: %{:.2f}".format(heightRatio * 100), 2000)
            else:
                self.statusBar.showMessage("Zoom ratio: %{:.2f}".format(widthRatio * 100), 2000)

        else:
            self.centralLabel.setPixmap(pixmap)
            self.statusBar.showMessage("Zoom ratio: %{:.2f}".format(100), 2000)

    def resizeImage(self):
        if self.imageListWidget.count() > 0:
            if self.imageListWidget.currentItem() is not None:
                pixmap = self.numpy2QPixmap(self.imageListWidget.currentItem().imageInOriginalSize)

    def changeLabelImage(self):
        pixmap = QPixmap(self.imageListWidget.currentItem().pathToImage)
        self.resizeImageAccordingToWindow(pixmap)

    def openFile(self):
        # set default directory path
        if self.openDir == '':
            self.openDir = 'c:\\'
        # Logic for opening an existing file goes here...
        filename = QFileDialog.getOpenFileName(self, self.tr('Open file'), self.openDir, "Image files (*.jpg *.jpeg *.gif *.png)")
        p = Path(filename[0])
        self.openDir = str(p.parent)
        imagePath = filename[0]
        self.centralLabel.setAlignment(Qt.AlignCenter)
        item = ImageListWidgetItem(imagePath, QIcon(imagePath), p.name)
        self.imageListWidget.addItem(item)
        self.imageListWidget.setCurrentItem(item)

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

        # Connect Scikit actions
        self.rgb2greyAction.triggered.connect(self.scikitRGB2Gray)

    def showFinishedMessage(self):
        self.statusBar.showMessage("Completed.", 2000)

    def scikitRGB2Gray(self):
        if self.imageListWidget.count() == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No image selected!")
            msg.setInformativeText("Please select image before applying algorithm")
            msg.setWindowTitle("No image")
            msg.setStandardButtons(QMessageBox.Ok)
            return msg.exec_()

        worker = Worker(ColorManipulation.convertRGB2Gray, self.imageListWidget.currentItem().imageInOriginalSize)
        worker.signals.result.connect(self.numpy2QPixmap)
        worker.signals.finished.connect(self.showFinishedMessage)
        self.statusBar.showMessage("Processig...")
        self.threadpool.start(worker)




def window():
    # Setup application for operating system
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()

    sys.exit(app.exec_())


window()
