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

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets \
    import (QPushButton, QWidget, QLabel, QApplication, QVBoxLayout)

import sys
import urllib.request
import table_validator.api

#
# this is a Qt app that is a drop target
# and validates the file dropped
#
class ValidationDropTarget(QWidget):


    def __init__(self):
        #self.labelUrl = 0;
        super().__init__()


        self.setAcceptDrops(True)
        self.initUI()

        # taken from
        # https://www.iana.org/assignments/media-types/media-types.txt
        self.accepted_formats = ['text/uri-list']

    # overloading the drop event
    def dropEvent(self, e):
        print("Dropped!")
        urls = e.mimeData().urls()
        response = urllib.request.urlopen(urls[0].toString())
        data = response.read()      # a `bytes` object

        candidate = [
            list(line.strip().split('\t'))
            for line in data.decode("UTF-8").split("\n")
        ]

        print("Candidate %s" % candidate)

        # FIXME: example is hardcoded
        template_file = open('../../tests/simple_candidate.tsv');

        template = table_validator.api.parse_tsv(template_file)

        self.labelUrl.setText(urls[0].toString())

        if table_validator.api.validate(template, candidate):
            self.labelSuccess.setText('<span style=" font-size:18pt; font-weight:600; color:#00aa00;">Validation succeeded!</span>')
        else:
            self.labelSuccess.setText('<span style=" font-size:18pt; font-weight:600; color:#00aa00;">Validation failed!</span>')

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

        accept = self.isAccepted(e)
        if(accept):
            print("Accepted")
        else:
            print("failed %s" % e.mimeData().formats())

    # initUI
    def initUI(self):

        self.labelUrl = QLabel()
        self.labelUrl.setAlignment(Qt.AlignLeft)
        self.labelUrl.setText("Drop your files here:")

        self.labelSuccess = QLabel()
        self.labelSuccess.setAlignment(Qt.AlignLeft)
        self.labelSuccess.setText("Not analyzed, yet!")

        self.labelInstructions = QLabel()
        self.labelInstructions.setAlignment(Qt.AlignLeft)
        self.labelInstructions.setText("""
        <p>
        Are you asking yourself if your tabular data file is really matching
        the template you agreed on with your collaboration partners?
        <p>
        Then this tool is the solution for you. Just take this file in your
        file manager (finder, windows explorer, nautilus...) and then
        <b> drop it</b> onto this window.
        <p>
        We will check the format compliance of your file and immediately
        give
        <ul>
        <li> information if it is correct with respect to the template
        <li> give information on where it is incorrect
        </ul>

        <p>
        <b>Note:</b> Currently we process only <b>tab delimited</b> files.
        </p>

        """)

        vbox = QVBoxLayout()
        vbox.addWidget(self.labelUrl)
        vbox.addWidget(self.labelSuccess)
        vbox.addWidget(self.labelInstructions)
        vbox.addStretch()

        self.setLayout(vbox);


        self.setWindowTitle('INCOME table Validation Drop Target')
        self.setGeometry(800, 500, 300, 400)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    drop_target = ValidationDropTarget()
    drop_target.show()

    app.exec_()
