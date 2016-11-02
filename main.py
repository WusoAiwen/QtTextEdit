#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""這是一個GNU開放授權的免費編輯器，原始版本為Qt4.8.7 example，被Wuso Aiwen移植為PyQt4版本。
author  : Wuso Aiwen
version : 1.0 date : 2016.11.02
"""
from PyQt4 import QtGui
import TextEdit

app = QtGui.QApplication([])
gui = TextEdit.TextEdit()
gui.show()
app.exec()
