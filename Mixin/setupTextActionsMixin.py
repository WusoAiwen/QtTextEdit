#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from qtpy import QtWidgets, QtCore, QtGui
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
        tb = QtWidgets.QToolBar(self)
        tb.setWindowTitle("Format Actions")
        self.addToolBar(tb)

        menu = QtWidgets.QMenu("文字格式(&T)", self)
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
        tb = QtWidgets.QToolBar(self)
        tb.setAllowedAreas(QtCore.Qt.TopToolBarArea | QtCore.Qt.BottomToolBarArea)
        tb.setWindowTitle("Format Actions")
        self.addToolBarBreak(QtCore.Qt.TopToolBarArea)
        self.addToolBar(tb)

        # 更改字型
        self.comboFont = QtWidgets.QFontComboBox(tb)
        tb.addWidget(self.comboFont)
        self.comboFont.activated.connect(self.textFamily)

        # 更改文字顏色功能
        self.__textColorAction(tb, menu)

        # 更改文字大小
        self.comboSize = QtWidgets.QComboBox(tb)
        self.comboSize.setObjectName("comboSize")
        tb.addWidget(self.comboSize)
        self.comboSize.setEditable(True)

        db = QtGui.QFontDatabase()
        for size in db.standardSizes():
            self.comboSize.addItem(str(size))

        self.comboSize.activated.connect(lambda i : self.textSize(self.comboSize.itemText(i)))
        self.comboSize.setCurrentIndex(self.comboSize.findText(str(QtWidgets.QApplication.font().pointSize())))
        return

    def __textBoldAction(self, tb, menu):
        """text change to bold action"""
        self.actionTextBold = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("format-text-bold", QtGui.QIcon(rsrcPath + "/textbold.png")), "粗體(&B)", self
        )
        self.actionTextBold.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_B)
        self.actionTextBold.setPriority(QtWidgets.QAction.LowPriority)
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
        self.actionTextItalic = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("format-text-italic", QtGui.QIcon(rsrcPath + "/textitalic.png")), "斜體(&I)", self
        )
        self.actionTextItalic.setPriority(QtWidgets.QAction.LowPriority)
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
        self.actionTextUnderline = QtWidgets.QAction(QtGui.QIcon.fromTheme("format-text-underline",
                                                 QtGui.QIcon(rsrcPath + "/textunder.png")), "底斜線(&U)", self)
        self.actionTextUnderline.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_U)
        self.actionTextUnderline.setPriority(QtWidgets.QAction.LowPriority)
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
        grp = QtWidgets.QActionGroup(self)
        grp.triggered.connect(self.textAlign)

        # Make sure the alignLeft is always left of the alignRight
        if QtWidgets.QApplication.isLeftToRight():
            self.actionAlignLeft = QtWidgets.QAction(
                QtGui.QIcon.fromTheme("format-justify-left", QtGui.QIcon(rsrcPath + "/textleft.png")), "靠左(&L)", grp
            )
            self.actionAlignCenter = QtWidgets.QAction(
                QtGui.QIcon.fromTheme("format-justify-center", QtGui.QIcon(rsrcPath + "/textcenter.png")),
                "置中(&C)", grp
            )
            self.actionAlignRight = QtWidgets.QAction(
                QtGui.QIcon.fromTheme("format-justify-right", QtGui.QIcon(rsrcPath + "/textright.png")), "靠右(&R)", grp
            )
        else:
            self.actionAlignRight = QtWidgets.QAction(
                QtGui.QIcon.fromTheme("format-justify-right", QtGui.QIcon(rsrcPath + "/textright.png")), "靠右(&R)", grp
            )
            self.actionAlignCenter = QtWidgets.QAction(
                QtGui.QIcon.fromTheme("format-justify-center", QtGui.QIcon(rsrcPath + "/textcenter.png")),
                "置中(&C)", grp
            )
            self.actionAlignLeft = QtWidgets.QAction(
                QtGui.QIcon.fromTheme("format-justify-left", QtGui.QIcon(rsrcPath + "/textleft.png")),
                "靠左(&L)", grp
            )

        self.actionAlignJustify = QtWidgets.QAction(
            QtGui.QIcon.fromTheme("format-justify-fill", QtGui.QIcon(rsrcPath + "/textjustify.png")), "左右對齊(&J)", grp
        )

        self.actionAlignLeft.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_L)
        self.actionAlignLeft.setCheckable(True)
        self.actionAlignLeft.setPriority(QtWidgets.QAction.LowPriority)
        self.actionAlignCenter.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.actionAlignCenter.setCheckable(True)
        self.actionAlignCenter.setPriority(QtWidgets.QAction.LowPriority)
        self.actionAlignRight.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_R)
        self.actionAlignRight.setCheckable(True)
        self.actionAlignRight.setPriority(QtWidgets.QAction.LowPriority)
        self.actionAlignJustify.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_J)
        self.actionAlignJustify.setCheckable(True)
        self.actionAlignJustify.setPriority(QtWidgets.QAction.LowPriority)

        tb.addActions(grp.actions())
        menu.addActions(grp.actions())
        return

    def __textColorAction(self, tb, menu):
        """更改文字顏色功能"""
        pix = QtGui.QPixmap(16, 16)
        pix.fill(QtCore.Qt.black)
        self.actionTextColor = QtWidgets.QAction(QtGui.QIcon(pix), "字體顏色...", self)
        self.actionTextColor.triggered.connect(self.textColor)
        tb.addAction(self.actionTextColor)
        menu.addAction(self.actionTextColor)
        return

