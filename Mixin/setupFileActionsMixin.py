#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import ImageQrc
rsrcPath = ":/images/"


class setupFileActionsMixin:
    """這是一個Mixin class，定義檔案項目功能
    method:
        public : setupFileActions
        private: __openFile, __openOldFile, __saveFile, __saveFileAs, __printFile, __exportPDF, __exit
    """

    def setupFileActions(self):
        """設定檔案項目的事件"""
        tb = QtGui.QToolBar(self)
        tb.setWindowTitle("File Actions")
        self.addToolBar(tb)

        menu = QtGui.QMenu("檔案(&F)", self)
        self.menuBar().addMenu(menu)

        for _ in ((self.__openFile, True), (self.__openOldFile, True), (menu.addSeparator, False),
                  (self.__saveFile, True), (self.__saveFileAs, True), (menu.addSeparator, False),
                  (self.__printFile, True), (self.__printFilePreview, True),
                  (self.__exportPDF, True), (menu.addSeparator, False), (self.__exit, True)):
            if _[1]:
                _[0](tb, menu)
            else:
                _[0]()
        return

    def __openFile(self, tb, menu):
        """開啟新檔"""
        newIcon = QtGui.QIcon.fromTheme("document-new", QtGui.QIcon(rsrcPath + "/filenew.png"))
        a = QtGui.QAction(newIcon, "開啟新檔(&N)", self)
        a.setPriority(QtGui.QAction.LowPriority)
        a.setShortcut(QtGui.QKeySequence.New)
        a.triggered.connect(self.fileNew)
        tb.addAction(a)
        menu.addAction(a)
        return

    def __openOldFile(self, tb, menu):
        """開啟舊檔"""
        a = QtGui.QAction(QtGui.QIcon.fromTheme("document-open", QtGui.QIcon(rsrcPath + "/fileopen.png")),
                          "開啟(&O)...", self)
        a.setShortcut(QtGui.QKeySequence.Open)
        a.triggered.connect(self.fileOpen)
        tb.addAction(a)
        menu.addAction(a)
        return

    def __saveFile(self, tb, menu):
        """儲存檔案"""
        self.actionSave = QtGui.QAction(QtGui.QIcon.fromTheme("document-save",
                                        QtGui.QIcon(rsrcPath + "/filesave.png")), "儲存(&S)", self)

        self.actionSave.setShortcut(QtGui.QKeySequence.Save)
        self.actionSave.triggered.connect(self.fileSave)
        self.actionSave.setEnabled(False)
        tb.addAction(self.actionSave)
        menu.addAction(self.actionSave)
        return

    def __saveFileAs(self, tb, menu):
        """另存新檔"""
        a = QtGui.QAction("另存為(&A)...", self)
        a.setPriority(QtGui.QAction.LowPriority)
        a.triggered.connect(self.fileSaveAs)
        menu.addAction(a)
        return

    def __printFile(self, tb, menu):
        """列印檔案"""
        a = QtGui.QAction(QtGui.QIcon.fromTheme("document-print", QtGui.QIcon(rsrcPath + "/fileprint.png")),
                          "列印(&P)...", self)
        a.setPriority(QtGui.QAction.LowPriority)
        a.setShortcut(QtGui.QKeySequence.Print)
        a.triggered.connect(self.filePrint)
        tb.addAction(a)
        menu.addAction(a)
        return

    def __printFilePreview(self, tb, menu):
        """預覽列印"""
        a = QtGui.QAction(QtGui.QIcon.fromTheme("fileprint",
                          QtGui.QIcon(rsrcPath + "/fileprint.png")), "預覽列印...", self)
        a.triggered.connect(self.filePrintPreview)
        menu.addAction(a)
        return

    def __exportPDF(self, tb, menu):
        """輸出為PDF檔"""
        a = QtGui.QAction(QtGui.QIcon.fromTheme("exportpdf", QtGui.QIcon(rsrcPath + "/exportpdf.png")),
                          "輸出為PDF(&E)...", self)
        a.setPriority(QtGui.QAction.LowPriority)
        a.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_D)
        a.triggered.connect(self.filePrintPdf)
        tb.addAction(a)
        menu.addAction(a)
        return

    def __exit(self, tb, menu):
        """離開介面"""
        a = QtGui.QAction("離開(&Q)", self)
        a.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        a.triggered.connect(self.close)
        menu.addAction(a)
        return
