#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PySide.QtCore import *
from PySide.QtGui import *

import queens
import search_queens 

class QueenDisplay(QMainWindow):
    """
    Main form for displaying the 8 queens chess board along with various
    ways to interact with the chessboard and change its appearance and such.
    """

    def __init__(self, parent=None):
        super(QueenDisplay, self).__init__()
        self.setWindowTitle("8 Queens Problem")

def main():
    app = QApplication(sys.argv)
    display = QueenDisplay()
    display.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
