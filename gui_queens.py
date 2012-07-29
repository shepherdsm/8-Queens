#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PySide.QtCore import *
from PySide.QtGui import *

import queens
import search_queens 

class ChessBoardWidget(QWidget):
    def __init__(self, size=8):
        super(ChessBoardWidget, self).__init__()

        self.board_size = size

        self.square_color1 = (0, 255, 0)
        self.square_color2 = (0, 0, 0)

        self.init_UI()

    def init_UI(self):
        pass

    def set_square_color1(color1):
        self.square_color1 = color1

    def set_square_color2(color2):
        self.square_color2 = color2

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def draw_squares(self, qp, first_square, color):
        sides = 20

        offset_w = offset_h = 0        

        qp.setPen(QColor(*color))
        qp.setBrush(QColor(*color))

        for i in range(first_square, self.board_size + first_square):
            offset_w = sides * (i % 2)
            for j in range(i % 2, self.board_size, 2):
                qp.drawRect(offset_w, offset_h, sides, sides)
                offset_w += sides * 2
            offset_h += sides

    def drawWidget(self, qp):
        # Draw first set of squares
        self.draw_squares(qp, 0, self.square_color1)
        # Draw second set of squares
        self.draw_squares(qp, 1, self.square_color2)

class QueenDisplay(QMainWindow):
    """
    Main form for displaying the 8 queens chess board along with various
    ways to interact with the chessboard and change its appearance and such.
    """

    def __init__(self, parent=None):
        super(QueenDisplay, self).__init__()

        self.board = ChessBoardWidget()
        #self.board.update()

        self.init_UI()


    def init_UI(self):
        self.setCentralWidget(self.main_widget())
        
        self.setGeometry(300, 800, 250, 180)
        self.setWindowTitle("8 Queens Problem")
        self.show()

    def main_widget(self):
        main_widget = QWidget(self)

        main_box = QHBoxLayout()
        main_box.addWidget(self.board)
        main_widget.setLayout(main_box)

        return main_widget
        
def main():
    app = QApplication(sys.argv)
    display = QueenDisplay()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
