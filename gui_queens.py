#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
My GUI for displaying the chess board solutions of the 8-queens problem.
This is my first time using Qt for drawing a GUI, and I must say it's quite
fun. Last time I needed a GUI in Python was with Tkinter, and it can't compare
at all so far. Definitely a nice improvement.

Author: Scott Shepherd
Version: 1.0
"""

import sys
from PySide.QtCore import *
from PySide.QtGui import *

import queens
import search_queens 

class ChessBoardWidget(QWidget):
    """
    Creates a chessboard widget that gets drawn onto the screen and updated
    when certain controls are changed.

    TODO: Function that draws queens.
    """
    def __init__(self, size=8, sides=30):
        super(ChessBoardWidget, self).__init__()

        self.board_size = size
        self.square_sides = sides

        box = QHBoxLayout()
        # A spacer item is needed to draw on, otherwise the rest of the program
        # Eats up the available space.
        box.addSpacerItem(QSpacerItem(size * sides, size * sides))
        self.setLayout(box)

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
        """
        Draws the squares onto the widget. The variable first_square doesn't
        particularly matter as long as it's an int and they're a different parity.
        """
        offset_w = offset_h = 0 

        qp.setPen(QColor(*color))
        qp.setBrush(QColor(*color))

        for i in range(first_square, self.board_size + first_square):
            offset_w = self.square_sides * (i % 2)
            for j in range(i % 2, self.board_size, 2):
                qp.drawRect(offset_w, offset_h, self.square_sides, self.square_sides)
                offset_w += self.square_sides * 2
            offset_h += self.square_sides

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

        self.init_UI()


    def init_UI(self):
        self.setCentralWidget(self.main_widget())
        
        self.move(300, 300)
        self.setWindowTitle("8 Queens Problem")
        self.show()

    def main_widget(self):
        """
        Since Windows can't have a display layout really, creating
        a main widget to act as the central widget for the program.
        The main widget contains the layout for everything in the program.
        """
        main_widget = QWidget(self)

        main_layout = QHBoxLayout()

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.board)

        main_layout.addLayout(self.control_grid())
        main_layout.addLayout(right_layout)
        main_widget.setLayout(main_layout)

        return main_widget

    def control_grid(self):
        """
        A widget to define the control structure used to control the display
        of the chess board widget.
        """
        size_label = QLabel("Size")
        size_edit = QLineEdit()

        color1_label = QLabel("Square1 Color Picker")
        color1_combo = QComboBox()

        color2_label = QLabel("Square2 Color Picker")
        color2_combo = QComboBox()

        queen_label = QLabel("Queen Color Picker")
        queen_combo = QComboBox()

        grid = QVBoxLayout()
        grid.addWidget(size_label)
        grid.addWidget(size_edit)
        grid.addWidget(color1_label)
        grid.addWidget(color1_combo)
        grid.addWidget(color2_label)
        grid.addWidget(color2_combo)
        grid.addWidget(queen_label)
        grid.addWidget(queen_combo)

        return grid 
        
def main():
    app = QApplication(sys.argv)
    display = QueenDisplay()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
