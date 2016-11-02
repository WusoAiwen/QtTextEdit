#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import Mixin
import ImageQrc
rsrcPath = ":/images/"


class TextEdit(QtGui.QMainWindow, Mixin.setupFileActionsMixin, Mixin.setupEditActionsMixin,
               Mixin.setupTextActionsMixin):
    """程式主要介面
    method :
        public  : show, initialShow, closeEvent, load, maybeSave, fileNew, fileOpen, setCurrentFileName, fileSaveAs,
                  filePrint, filePrintPreview, filePrintPdf, textBold, textUnderline, textItalic, textFamily,
                  textSize, textAlign, textColor, currentCharFormatChanged, cursorPositionChanged, clipboardDataChanged
                  about, mergeFormatOnWordOrSelection, fontChanged, colorChanged, alignmentChanged
        private : __setupUi, __setupAllAction, __addAboutItem,
    """
    def __init__(self):
        super().__init__()
        # QAction
        for key in ('actionSave', 'actionTextBold', 'actionTextUnderline', 'actionTextItalic', 'actionTextColor',
                    'actionAlignLeft', 'actionAlignCenter', 'actionAlignRight', 'actionAlignJustify', 'actionUndo',
                    'actionRedo', 'actionCut', 'actionCopy', 'actionPaste'):
            setattr(self, key, None)

        self.comboFont = None  # QFontComboBox
        self.comboSize = None  # QComboBox

        self.tb = None  # QToolBar
        self.fileName = ''  # string
        self.textEdit = None  # QTextEdit

        self.__setupUi()
        self.initialShow()
        return

    def show(self):
        """顯示時，將視窗置於螢幕中央"""
        self.resize(640, 480)
        desk = QtGui.QDesktopWidget()
        x = (desk.screenGeometry().width() - self.frameSize().width()) / 2
        y = (desk.screenGeometry().height() - self.frameSize().height()) / 2
        self.move(x, y)
        super().show()
        return

    def initialShow(self, file=''):
        """預設開啟時顯示的內容資訊"""
        if not self.load(file):
            self.fileNew()
        return

    def __setupUi(self):
        """設定介面"""
        self.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.setupFileActions()
        self.setupEditActions()
        self.setupTextActions()
        self.__addAboutItem()

        self.textEdit = QtGui.QTextEdit(self)
        self.setCentralWidget(self.textEdit)
        self.textEdit.setFocus()

        self.setCurrentFileName('')
        self.actionCut.setEnabled(False)
        self.actionCopy.setEnabled(False)

        self.__setupAllAction()
        return

    def __setupAllAction(self):
        """定義所有widget的觸發事件"""
        self.textEdit.currentCharFormatChanged.connect(self.currentCharFormatChanged)
        self.textEdit.cursorPositionChanged.connect(self.cursorPositionChanged)

        self.fontChanged(self.textEdit.font())
        self.colorChanged(self.textEdit.textColor())
        self.alignmentChanged(self.textEdit.alignment())

        self.textEdit.document().modificationChanged.connect(self.actionSave.setEnabled)
        self.textEdit.document().modificationChanged.connect(self.setWindowModified)
        self.textEdit.document().undoAvailable.connect(self.actionUndo.setEnabled)
        self.textEdit.document().redoAvailable.connect(self.actionRedo.setEnabled)

        self.setWindowModified(self.textEdit.document().isModified())
        self.actionSave.setEnabled(self.textEdit.document().isModified())
        self.actionUndo.setEnabled(self.textEdit.document().isUndoAvailable())
        self.actionRedo.setEnabled(self.textEdit.document().isRedoAvailable())

        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)

        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste.triggered.connect(self.textEdit.paste)

        self.textEdit.copyAvailable.connect(self.actionCut.setEnabled)
        self.textEdit.copyAvailable.connect(self.actionCopy.setEnabled)

        QtGui.QApplication.clipboard().dataChanged.connect(self.clipboardDataChanged)
        return

    def __addAboutItem(self):
        """其它說明事項"""
        self.helpMenu = QtGui.QMenu("說明", self)
        self.menuBar().addMenu(self.helpMenu)
        self.helpMenu.addAction("關於PyQt4文字編輯器", self.about)
        return

    def closeEvent(self, e):
        """關閉視窗前，檢查檔案是否有變更，顯示需不需要存檔"""
        if self.maybeSave():
            e.accept()
        else:
            e.ignore()
        return

    def load(self, text):
        """讀取檔案資料"""
        if not QtCore.QFile.exists(text):
            return False

        file = QtCore.QFile(text)
        if not file.open(QtCore.QFile.ReadOnly):
            return False

        data = file.readAll()
        codec = QtCore.QTextCodec.codecForHtml(data)

        value = codec.toUnicode(data)
        if QtCore.Qt.mightBeRichText(value):
            self.textEdit.setHtml(value)
        else:
            self.textEdit.setPlainText(value)

        self.setCurrentFileName(text)
        return True

    def maybeSave(self):
        """檢查檔案是否有被變更，若有則顯示提示存檔訊息"""
        if not self.textEdit.document().isModified():
            return True

        ret = QtGui.QMessageBox.warning(self, "檔案變更提示訊息", "這個檔案內容已被變更，是否儲存？",
                                        QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
        if ret == QtGui.QMessageBox.Save:
            return self.fileSave()
        elif ret == QtGui.QMessageBox.Cancel:
            return False
        return True

    def fileNew(self):
        """開啟新檔"""
        if self.maybeSave():
            self.textEdit.clear()
            self.setCurrentFileName('')
        return

    def fileOpen(self):
        """開啟舊檔"""
        fn = QtGui.QFileDialog.getOpenFileName(self, "開啟檔案...", '',
                                               "Qt文字編輯器格式檔(*.qxt);;網頁檔(*.htm *.html);;一般文字檔 (*.txt)")
        if fn:
            self.load(fn)
        return

    def setCurrentFileName(self, fileName):
        """設定幕目前作用中的檔案"""
        self.fileName = fileName
        self.textEdit.document().setModified(False)

        if not self.fileName:
            shownName = "untitled.qxt"
        else:
            shownName = QtCore.QFileInfo(fileName).fileName()

        self.setWindowTitle("{}[*] - PyQt4 文字編輯器 v1.0".format(shownName))
        self.setWindowModified(False)
        return

    def fileSaveAs(self):
        """另存新檔"""
        fn = QtGui.QFileDialog.getSaveFileName(self, "儲存檔案",
                                               '', "Qt文字編輯器格式檔(*.qxt);;網頁檔(*.htm *.html);;一般文字檔 (*.txt)")
        if not fn:
            return False

        self.setCurrentFileName(fn)
        return self.fileSave()

    def fileSave(self):
        """儲存檔案"""
        if not self.fileName:
            return self.fileSaveAs()

        end_str = self.fileName.endswith(('.qxt', '.htm', '.html', '.txt'))
        success = False
        if end_str:
            writer = QtGui.QTextDocumentWriter(self.fileName)
            if end_str == '.qxt':
                writer.setFormat('html')
            success = writer.write(self.textEdit.document())
            if success:
                self.textEdit.document().setModified(False)
        else:
            for _ in ('.qxt', '.html', '.txt'):
                writer = QtGui.QTextDocumentWriter(self.fileName + _)
                if _ == '.qxt':
                    writer.setFormat('html')

                success = writer.write(self.textEdit.document())
                if success:
                    self.textEdit.document().setModified(False)
                    break

        return success

    def filePrint(self):
        """列印檔案"""
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        dlg = QtGui.QPrintDialog(printer, self)

        if self.textEdit.textCursor().hasSelection():
            dlg.addEnabledOption(QtGui.QAbstractPrintDialog.PrintSelection)

        dlg.setWindowTitle("列印檔案")
        if dlg.exec() == QtGui.QDialog.Accepted:
            self.textEdit.print(printer)

        del dlg
        return

    def filePrintPreview(self):
        """檔案預覽列印"""
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        preview = QtGui.QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self.textEdit.print)
        preview.exec()
        return

    def filePrintPdf(self):
        """輸出檔案為PDF"""
        fileName = QtGui.QFileDialog.getSaveFileName(self, "輸出PDF", '', "*.pdf")
        if not fileName:
            return

        if not fileName.endswith('.pdf'):
            fileName += '.pdf'

        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName(fileName)
        self.textEdit.document().print(printer)
        return

    def textBold(self):
        """文字改粗體"""
        fmt = QtGui.QTextCharFormat()
        fmt.setFontWeight(QtGui.QFont.Bold if self.actionTextBold.isChecked() else QtGui.QFont.Normal)
        self.mergeFormatOnWordOrSelection(fmt)
        return

    def textUnderline(self):
        """文字加底線"""
        fmt = QtGui.QTextCharFormat()
        fmt.setFontUnderline(self.actionTextUnderline.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)
        return

    def textItalic(self):
        """文字改斜體"""
        fmt = QtGui.QTextCharFormat()
        fmt.setFontItalic(self.actionTextItalic.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)
        return

    def textFamily(self, text):
        """更改字型"""
        fmt = QtGui.QTextCharFormat()
        fmt.setFontFamily(text)
        self.mergeFormatOnWordOrSelection(fmt)
        return

    def textSize(self, text):
        """調整文字尺寸"""
        if float(text) > 0:
            fmt = QtGui.QTextCharFormat()
            fmt.setFontPointSize(float(text))
            self.mergeFormatOnWordOrSelection(fmt)
        return

    def textAlign(self, action):
        """調整文字位置"""
        if action == self.actionAlignLeft:
            self.textEdit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignAbsolute)
        elif action == self.actionAlignCenter:
            self.textEdit.setAlignment(QtCore.Qt.AlignHCenter)
        elif action == self.actionAlignRight:
            self.textEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignAbsolute)
        elif action == self.actionAlignJustify:
            self.textEdit.setAlignment(QtCore.Qt.AlignJustify)
        return

    def textColor(self):
        """調整文字顏色"""
        col = QtGui.QColorDialog.getColor(self.textEdit.textColor(), self)
        if not col.isValid():
            return

        fmt = QtGui.QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatOnWordOrSelection(fmt)
        self.colorChanged(col)
        return

    def currentCharFormatChanged(self, obj):
        """調整文字字型、顏色"""
        self.fontChanged(obj.font())
        self.colorChanged(obj.foreground().color())
        return

    def cursorPositionChanged(self):
        """調整文字位置"""
        self.alignmentChanged(self.textEdit.alignment())
        return

    def clipboardDataChanged(self):
        """檢查剪貼簿資料是否有文字"""
        clipboard = QtGui.QApplication.clipboard()
        md = clipboard.mimeData()
        if md:
            self.actionPaste.setEnabled(md.hasText())
        return

    def about(self):
        """顯示其它訊息"""
        QtGui.QMessageBox.about(self, "關於PyQt4文字編輯器", "這是一個GNU開放授權的免費編輯器，原始版本為Qt4.8.7 example，"
                                "被Wuso Aiwen移植為PyQt4版本。")
        return

    def mergeFormatOnWordOrSelection(self, f):
        cursor = self.textEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QtGui.QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(f)
        self.textEdit.mergeCurrentCharFormat(f)
        return

    def fontChanged(self, f):
        self.comboFont.setCurrentIndex(self.comboFont.findText(QtGui.QFontInfo(f).family()))
        self.comboSize.setCurrentIndex(self.comboSize.findText(str(f.pointSize())))
        self.actionTextBold.setChecked(f.bold())
        self.actionTextItalic.setChecked(f.italic())
        self.actionTextUnderline.setChecked(f.underline())
        return

    def colorChanged(self, c):
        pix = QtGui.QPixmap(16, 16)
        pix.fill(c)
        self.actionTextColor.setIcon(QtGui.QIcon(pix))
        return

    def alignmentChanged(self, obj):
        if int(obj) == QtCore.Qt.AlignLeft:
            self.actionAlignLeft.setChecked(True)
        elif int(obj) == QtCore.Qt.AlignHCenter:
            self.actionAlignCenter.setChecked(True)
        elif int(obj) == QtCore.Qt.AlignRight:
            self.actionAlignRight.setChecked(True)
        elif int(obj) == QtCore.Qt.AlignJustify:
            self.actionAlignJustify.setChecked(True)
        return

