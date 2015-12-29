# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\shihui\ericproject\imagequliting\desktop.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.pic1 = QtGui.QGraphicsView(self.centralWidget)
        self.pic1.setGeometry(QtCore.QRect(20, 120, 221, 191))
        self.pic1.setObjectName(_fromUtf8("pic1"))
        self.pic2 = QtGui.QGraphicsView(self.centralWidget)
        self.pic2.setGeometry(QtCore.QRect(330, 110, 441, 431))
        self.pic2.setObjectName(_fromUtf8("pic2"))
        self.label = QtGui.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(340, 30, 54, 12))
        self.label.setObjectName(_fromUtf8("label"))
        self.fileopen = QtGui.QPushButton(self.centralWidget)
        self.fileopen.setGeometry(QtCore.QRect(30, 500, 75, 23))
        self.fileopen.setObjectName(_fromUtf8("fileopen"))
        self.dealwith = QtGui.QPushButton(self.centralWidget)
        self.dealwith.setGeometry(QtCore.QRect(170, 500, 75, 23))
        self.dealwith.setObjectName(_fromUtf8("dealwith"))
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "图像拼接", None))
        self.fileopen.setText(_translate("MainWindow", "打开", None))
        self.dealwith.setText(_translate("MainWindow", "处理", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

