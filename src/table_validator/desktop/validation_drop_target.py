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

import logging
import sys
import urllib.request

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

import table_validator

logger = logging.getLogger(__name__)


class ValidationDropTarget(QWidget):
    """A Qt app that is a drop target and validates the file dropped."""

    def __init__(self, template_file):
        # self.labelUrl = 0;
        super().__init__()

        self.setAcceptDrops(True)
        self.initUI()

        self.template = table_validator.parse_tsv(template_file)

        # taken from
        # https://www.iana.org/assignments/media-types/media-types.txt
        self.accepted_formats = ['text/uri-list']

    def _validate_table(self, candidate) -> bool:
        return table_validator.validate(self.template, candidate)

    # overloading the drop event
    def dropEvent(self, e):
        print("Dropped!")
        urls = e.mimeData().urls()
        response = urllib.request.urlopen(urls[0].toString())
        candidate = table_validator.parse_tsv(response.read().decode("UTF-8").split("\n"))

        print("Candidate %s" % candidate)

        self.labelUrl.setText(urls[0].toString())

        if self._validate_table(candidate):
            self.labelSuccess.setText(
                '<span style=" font-size:18pt; font-weight:600; color:#00aa00;">Validation succeeded!</span>')
        else:
            self.labelSuccess.setText(
                '<span style=" font-size:18pt; font-weight:600; color:#00aa00;">Validation failed!</span>')

        print("dropped" % urls)

    # a method for acceptance checks based
    # on the mime type of the thing dragged
    def isAccepted(self, e):
        accept = any(
            e.mimeData().hasFormat(i)
            for i in self.accepted_formats
        )

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
        if accept:
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
        Just <b>drag and drop</b> your files here to check if they match the format
        as agreed with your colleague<p>

        Currently we process only <b>tab delimited</b> files.


        """)

        vbox = QVBoxLayout()
        vbox.addWidget(self.labelUrl)
        vbox.addWidget(self.labelSuccess)
        vbox.addWidget(self.labelInstructions)
        vbox.addStretch()

        self.setLayout(vbox)

        self.setWindowTitle('INCOME table Validation Drop Target')
        self.setGeometry(800, 500, 300, 400)


def main():
    app = QApplication(sys.argv)
    with open('../../../tests/simple_candidate.tsv') as file:
        drop_target = ValidationDropTarget(file)
    drop_target.show()
    app.exec_()


if __name__ == '__main__':
    main()
