#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import ImageQrc
rsrcPath = ":/images/"


class setupEditActionsMixin:
    """這是一個Mixin class，定義檔案編輯項目功能
    method:
        public : setupEditActions
        private: __undoAction, __redoAction, __cutAction, __copyAction, __pasteAction
    """

    def setupEditActions(self):
        """設定編輯項目功能"""
        tb = QtGui.QToolBar(self)
        tb.setWindowTitle("Edit Actions")
        self.addToolBar(tb)
        menu = QtGui.QMenu("編輯(&E)", self)
        self.menuBar().addMenu(menu)

        # 定義各子項目功能
        for _ in ((self.__undoAction, True), (self.__redoAction, True), (menu.addSeparator, False),
                  (self.__cutAction, True), (self.__copyAction, True), (self.__pasteAction, True)):
            if _[1]:
                _[0](tb, menu)
            else:
                _[0]()
        return

    def __undoAction(self, tb, menu):
        """undo功能"""
        self.actionUndo = QtGui.QAction(QtGui.QIcon.fromTheme("edit-undo", QtGui.QIcon(rsrcPath + "/editundo.png")),
                                        "復原(&U)", self)
        self.actionUndo.setShortcut(QtGui.QKeySequence.Undo)
        tb.addAction(self.actionUndo)
        menu.addAction(self.actionUndo)
        return

    def __redoAction(self, tb, menu):
        """redo功能"""
        self.actionRedo = QtGui.QAction(QtGui.QIcon.fromTheme("edit-redo", QtGui.QIcon(rsrcPath + "/editredo.png")),
                                        "重做(&D)", self)
        self.actionRedo.setPriority(QtGui.QAction.LowPriority)
        self.actionRedo.setShortcut(QtGui.QKeySequence.Redo)
        tb.addAction(self.actionRedo)
        menu.addAction(self.actionRedo)
        return

    def __cutAction(self, tb, menu):
        """cut功能"""
        self.actionCut = QtGui.QAction(QtGui.QIcon.fromTheme("edit-cut", QtGui.QIcon(rsrcPath + "/editcut.png")),
                                       "剪下(&T)", self)
        self.actionCut.setPriority(QtGui.QAction.LowPriority)
        self.actionCut.setShortcut(QtGui.QKeySequence.Cut)
        tb.addAction(self.actionCut)
        menu.addAction(self.actionCut)
        return

    def __copyAction(self, tb, menu):
        """copy功能"""
        self.actionCopy = QtGui.QAction(QtGui.QIcon.fromTheme("edit-copy", QtGui.QIcon(rsrcPath + "/editcopy.png")),
                                        "複製(&C)", self)
        self.actionCopy.setPriority(QtGui.QAction.LowPriority)
        self.actionCopy.setShortcut(QtGui.QKeySequence.Copy)
        tb.addAction(self.actionCopy)
        menu.addAction(self.actionCopy)
        return

    def __pasteAction(self, tb, menu):
        """paste功能"""
        self.actionPaste = QtGui.QAction(QtGui.QIcon.fromTheme("edit-paste", QtGui.QIcon(rsrcPath + "/editpaste.png")),
                                         "貼上(&P)", self)
        self.actionPaste.setPriority(QtGui.QAction.LowPriority)
        self.actionPaste.setShortcut(QtGui.QKeySequence.Paste)
        tb.addAction(self.actionPaste)
        menu.addAction(self.actionPaste)
        return
