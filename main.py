#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""這是一個GNU開放授權的免費編輯器，原始版本為Qt4.8.7 example，被Wuso Aiwen移植為PyQt版本。
author  : Wuso Aiwen
version : 1.0 date : 2016.11.02
version : 2.0 date : 2017.04.24
  (a) 修改內容為PyQt5版本。
  (b) 修改另存新檔的bug.
"""
from qtpy import QtWidgets
import TextEdit

app = QtWidgets.QApplication([])
gui = TextEdit.TextEdit()
gui.show()
app.exec()
