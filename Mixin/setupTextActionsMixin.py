#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import ImageQrc
rsrcPath = ":/images/"


class setupTextActionsMixin:
    """這是一個Mixin class，定義文字格式項目功能
    method:
        public : setupTextActions
        private: __textFormatAction, __textBoldAction, __textItalicAction, __textUnderlineAction, __textAlignAction
                 __textColorAction
    """

    def setupTextActions(self):
        """定義文字格式功能"""
        tb = QtGui.QToolBar(self)
        tb.setWindowTitle("Format Actions")
        self.addToolBar(tb)

        menu = QtGui.QMenu("文字格式(&T)", self)
        self.menuBar().addMenu(menu)

        # text change to bold action
        self.__textBoldAction(tb, menu)

        # text change to italic action
        self.__textItalicAction(tb, menu)

        # text change to have under line
        self.__textUnderlineAction(tb, menu)
        menu.addSeparator()

        # 文字位置調整功能
        self.__textAlignAction(tb, menu)
        menu.addSeparator()

        # 調整字型及大小
        self.__textFormatAction(menu)
        return

    def __textFormatAction(self, menu):
        """調整字型及大小"""
        tb = QtGui.QToolBar(self)
        tb.setAllowedAreas(QtCore.Qt.TopToolBarArea | QtCore.Qt.BottomToolBarArea)
        tb.setWindowTitle("Format Actions")
        self.addToolBarBreak(QtCore.Qt.TopToolBarArea)
        self.addToolBar(tb)

        # 更改字型
        self.comboFont = QtGui.QFontComboBox(tb)
        tb.addWidget(self.comboFont)
        self.connect(self.comboFont, QtCore.SIGNAL('activated(QString)'), self.textFamily)

        # 更改文字顏色功能
        self.__textColorAction(tb, menu)

        # 更改文字大小
        self.comboSize = QtGui.QComboBox(tb)
        self.comboSize.setObjectName("comboSize")
        tb.addWidget(self.comboSize)
        self.comboSize.setEditable(True)

        db = QtGui.QFontDatabase()
        for size in db.standardSizes():
            self.comboSize.addItem(str(size))

        self.connect(self.comboSize, QtCore.SIGNAL('activated(QString)'), self.textSize)
        self.comboSize.setCurrentIndex(self.comboSize.findText(str(QtGui.QApplication.font().pointSize())))
        return

    def __textBoldAction(self, tb, menu):
        """text change to bold action"""
        self.actionTextBold = QtGui.QAction(QtGui.QIcon.fromTheme("format-text-bold",
                                            QtGui.QIcon(rsrcPath + "/textbold.png")), "粗體(&B)", self)
        self.actionTextBold.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_B)
        self.actionTextBold.setPriority(QtGui.QAction.LowPriority)
        bold = QtGui.QFont()
        bold.setBold(True)
        self.actionTextBold.setFont(bold)
        self.actionTextBold.triggered.connect(self.textBold)
        tb.addAction(self.actionTextBold)
        menu.addAction(self.actionTextBold)
        self.actionTextBold.setCheckable(True)
        return

    def __textItalicAction(self, tb, menu):
        """text change to italic action"""
        self.actionTextItalic = QtGui.QAction(QtGui.QIcon.fromTheme("format-text-italic",
                                              QtGui.QIcon(rsrcPath + "/textitalic.png")), "斜體(&I)", self)
        self.actionTextItalic.setPriority(QtGui.QAction.LowPriority)
        self.actionTextItalic.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_I)
        italic = QtGui.QFont()
        italic.setItalic(True)
        self.actionTextItalic.setFont(italic)
        self.actionTextItalic.triggered.connect(self.textItalic)
        tb.addAction(self.actionTextItalic)
        menu.addAction(self.actionTextItalic)
        self.actionTextItalic.setCheckable(True)
        return

    def __textUnderlineAction(self, tb, menu):
        """text change to have under line"""
        self.actionTextUnderline = QtGui.QAction(QtGui.QIcon.fromTheme("format-text-underline",
                                                 QtGui.QIcon(rsrcPath + "/textunder.png")), "底斜線(&U)", self)
        self.actionTextUnderline.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_U)
        self.actionTextUnderline.setPriority(QtGui.QAction.LowPriority)
        underline = QtGui.QFont()
        underline.setUnderline(True)
        self.actionTextUnderline.setFont(underline)
        self.actionTextUnderline.triggered.connect(self.textUnderline)
        tb.addAction(self.actionTextUnderline)
        menu.addAction(self.actionTextUnderline)
        self.actionTextUnderline.setCheckable(True)
        return

    def __textAlignAction(self, tb, menu):
        """文字位置調整功能"""
        grp = QtGui.QActionGroup(self)
        grp.triggered.connect(self.textAlign)

        # Make sure the alignLeft is always left of the alignRight
        if QtGui.QApplication.isLeftToRight():
            self.actionAlignLeft = QtGui.QAction(
                QtGui.QIcon.fromTheme("format-justify-left", QtGui.QIcon(rsrcPath + "/textleft.png")), "靠左(&L)", grp
            )
            self.actionAlignCenter = QtGui.QAction(
                QtGui.QIcon.fromTheme("format-justify-center", QtGui.QIcon(rsrcPath + "/textcenter.png")),
                "置中(&C)", grp
            )
            self.actionAlignRight = QtGui.QAction(
                QtGui.QIcon.fromTheme("format-justify-right", QtGui.QIcon(rsrcPath + "/textright.png")), "靠右(&R)", grp
            )
        else:
            self.actionAlignRight = QtGui.QAction(
                QtGui.QIcon.fromTheme("format-justify-right", QtGui.QIcon(rsrcPath + "/textright.png")), "靠右(&R)", grp
            )
            self.actionAlignCenter = QtGui.QAction(
                QtGui.QIcon.fromTheme("format-justify-center", QtGui.QIcon(rsrcPath + "/textcenter.png")),
                "置中(&C)", grp
            )
            self.actionAlignLeft = QtGui.QAction(
                QtGui.QIcon.fromTheme("format-justify-left", QtGui.QIcon(rsrcPath + "/textleft.png")),
                "靠左(&L)", grp
            )

        self.actionAlignJustify = QtGui.QAction(
            QtGui.QIcon.fromTheme("format-justify-fill", QtGui.QIcon(rsrcPath + "/textjustify.png")), "左右對齊(&J)", grp
        )

        self.actionAlignLeft.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_L)
        self.actionAlignLeft.setCheckable(True)
        self.actionAlignLeft.setPriority(QtGui.QAction.LowPriority)
        self.actionAlignCenter.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.actionAlignCenter.setCheckable(True)
        self.actionAlignCenter.setPriority(QtGui.QAction.LowPriority)
        self.actionAlignRight.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_R)
        self.actionAlignRight.setCheckable(True)
        self.actionAlignRight.setPriority(QtGui.QAction.LowPriority)
        self.actionAlignJustify.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_J)
        self.actionAlignJustify.setCheckable(True)
        self.actionAlignJustify.setPriority(QtGui.QAction.LowPriority)

        tb.addActions(grp.actions())
        menu.addActions(grp.actions())
        return

    def __textColorAction(self, tb, menu):
        """更改文字顏色功能"""
        pix = QtGui.QPixmap(16, 16)
        pix.fill(QtCore.Qt.black)
        self.actionTextColor = QtGui.QAction(QtGui.QIcon(pix), "字體顏色...", self)
        self.actionTextColor.triggered.connect(self.textColor)
        tb.addAction(self.actionTextColor)
        menu.addAction(self.actionTextColor)
        return

