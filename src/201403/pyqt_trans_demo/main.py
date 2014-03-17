#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
module: main
#说明:这是从机械君那里粘来的代码
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def tr(msg):
    return QCoreApplication.translate("@default", msg)

def main():
    app = QApplication([])

    trans = QTranslator();
    trans.load('plabel_zh_CN')
    app.installTranslator(trans)

    hello = QPushButton(tr("hello world!"))
    hello.show()

    app.exec_()
    
if __name__=="__main__":
    main()