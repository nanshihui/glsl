# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import sys
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QMainWindow
from PyQt4 import QtGui, QtCore
from Ui_desktop import Ui_MainWindow
import imagequlit
reload(sys)
sys.setdefaultencoding('utf-8')

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.filepath=None
    def chooseFile(self):
        dialog = QtGui.QFileDialog()
        
        imageFile = dialog.getOpenFileName()
  
        if imageFile != '':
            self.openImageFile(imageFile,self.pic1)
            self.path = imageFile    
            print self.path
    
    def openImageFile(self, imageFile, component):
        """ Load the image from the file given, and create four pixmaps based
            on the original image.
            The window caption is set, and the Brightness menu enabled if the image file
            can be loaded.
        """
        pixmap=QtGui.QPixmap()
        self.filepath=imageFile
        if pixmap.load(imageFile):

            self.scene=QtGui.QGraphicsScene(self)
            item=QtGui.QGraphicsPixmapItem(pixmap)
            self.scene.addItem(item)
            component.setScene(self.scene)


        else:
            QtGui.QMessageBox.warning(self, "Cannot open file",
                    "文件无法打开",
                    QtGui.QMessageBox.Cancel, QtGui.QMessageBox.NoButton,
                    QtGui.QMessageBox.NoButton)
    @pyqtSignature("")
    def on_fileopen_clicked(self):

        self.chooseFile()

    
    @pyqtSignature("")
    def on_dealwith_clicked(self):
        result,path=imagequlit.doqilt(self.filepath)
        if result:
            self.openImageFile(path,self.pic2)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()

    sys.exit(app.exec_())
