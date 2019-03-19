#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

Author: Wolfgang Müller
The initial starting point was taken from zetcode
However, there are only few lines that survived changes.


-
ZetCode PyQt5 tutorial

This is a simple drag and
drop example.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017

http://zetcode.com/gui/pyqt5/dragdrop/
"""

from PyQt5.QtWidgets \
    import (QPushButton, QWidget, QLineEdit, QApplication)

import sys
import urllib.request

#
# this is a Qt app that is a drop target
# and validates the file dropped
#
class ValidationDropTarget(QWidget):

    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)
        self.initUI()

        # taken from
        # https://www.iana.org/assignments/media-types/media-types.txt
        self.accepted_formats = ['text/plain','application/vnd.ms-excel']

    # overloading the drop event
    def dropEvent(self, e):
        urls = e.mimeData().urls()
        response = urllib.request.urlopen(urls[0])
        data = response.read()      # a `bytes` object
        print("dropped" % urls)


    # a method for acceptance checks based
    # on the mime type of the thing dragged
    def isAccepted(self,e):
        accept = False;
        for i in self.accepted_formats:
            if e.mimeData().hasFormat(i):
                accept = True;
        if accept:
            e.accept()
        else:
            e.ignore()

    # when you enter a drop zone
    # then this function decides if you can drop
    # this type of file
    def dragEnterEvent(self, e):
        print("enter")
        print(e.mimeData().urls())

        return self.isAccepted(e)

    # initUI
    def initUI(self):

        self.setWindowTitle('INCOME Validation Drop Target')
        self.setGeometry(100, 100, 300, 150)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    drop_target = ValidationDropTarget()
    drop_target.show()

    app.exec_()
