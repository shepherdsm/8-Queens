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
        self.square_color1 = (0, 255, 0)
        self.square_color2 = (0, 0, 255)
        self.queen_color = (0, 0, 0)
        self.offset = 40 # Offsets where the board is drawn and how big the spacer is
        # List of all the solutions
        self.solutions = queens.get_solutions(queens.init_board(size),
                                            queens.possible_moves(size), 0, [])
        self.position = 0 # Position in the solutions

        self.init_UI()

    def init_UI(self):
        self.solution_label = self.init_sol_label()
        self.set_solution_label(0)
        self.spacer = QSpacerItem(*self._get_size())

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.solution_label, alignment=Qt.AlignCenter | Qt.AlignTop)

        # A spacer item is needed to draw on, otherwise the rest of the program
        # Eats up the available space.
        self.layout.addSpacerItem(self.spacer)

        self.setLayout(self.layout)

    def _get_size(self):
        return [self.board_size * self.square_sides + self.offset] * 2

    def init_sol_label(self):
        label = QLabel("Solution 1")
        label.setFont(QFont("Helvetica", 25, QFont.Bold))
        return label

    def set_square_color1(color1):
        self.square_color1 = color1

    def set_square_color2(color2):
        self.square_color2 = color2

    def set_solution_label(self, num):
        self.solution_label.setText("Solution %s" % num)

    def update_size(self, num):
        self.board_size = num
        self.spacer.changeSize(*self._get_size())
        self.solutions = queens.get_solutions(queens.init_board(num),
                                            queens.possible_moves(num), 0, [])
        print(self.solutions)
        self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def draw_squares(self, qp, first_square, color):
        """
        Draws the squares onto the widget. The variable first_square doesn't
        particularly matter as long as it's an int and it's a different parity
        from the previous/future call of it.
        """
        offset_h = self.offset

        qp.setPen(QColor(*color))
        qp.setBrush(QColor(*color))

        for i in range(first_square, self.board_size + first_square):
            offset_w = self.square_sides * (i % 2) + self.offset // 2
            for j in range(i % 2, self.board_size, 2):
                qp.drawRect(offset_w, offset_h, self.square_sides, self.square_sides)
                offset_w += self.square_sides * 2
            offset_h += self.square_sides

    def drawWidget(self, qp):
        # Draw first set of squares
        self.draw_squares(qp, 0, self.square_color1)
        # Draw second set of squares
        self.draw_squares(qp, 1, self.square_color2)
        # Draw the queens
        self.draw_queens(qp)

    def draw_queens(self, qp):
        """
        Draws the queens onto the board. self.solutions has all the solutions, and
        self.position is where we are in the list of solutions. Updated by other functions.
        draw_queens doesn't care one iota about it. It just wants to draw some queens.
        
        The scary looking stuff in Ellipse is just to position the queens right. We center them
        into the middle of the proper square, then draw their radius 5 smaller on a side to not
        take up the entire square. Looks nicer that way I think.
        """
        tmp = self.solutions[self.position]
        qp.setPen(QColor(*self.queen_color))
        qp.setBrush(QColor(*self.queen_color))
        for row in range(len(tmp)):
            col = queens.get_column(tmp[row], self.board_size)
            qp.drawEllipse(QPointF(self.square_sides * row + (self.offset + self.square_sides) // 2,
                                  self.square_sides * col + self.offset + self.square_sides // 2),
                            self.square_sides // 2 - 5, self.square_sides // 2 - 5)

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
        size_edit.setFixedWidth(50)
        size_edit.textChanged[str].connect(self.change_size)

        color1_label = QLabel("Square1 Color Picker")
        color1_combo = QComboBox()

        color2_label = QLabel("Square2 Color Picker")
        color2_combo = QComboBox()

        queen_label = QLabel("Queen Color Picker")
        queen_combo = QComboBox()

        grid = QGridLayout()
        grid.addWidget(size_label, 0, 0, 1, 2, Qt.AlignCenter)
        grid.addWidget(size_edit, 1, 0, alignment=Qt.AlignCenter)
        grid.addWidget(color1_label, 2, 0, 1, 2, Qt.AlignCenter)
        grid.addWidget(color1_combo, 3, 0, 1, 2)
        grid.addWidget(color2_label, 4, 0, 1, 2, Qt.AlignCenter)
        grid.addWidget(color2_combo, 5, 0, 1, 2)
        grid.addWidget(queen_label, 6, 0, 1, 2, Qt.AlignCenter)
        grid.addWidget(queen_combo, 7, 0, 1, 2)

        return grid

    def change_size(self, num):
        self.board.update_size(int(num))

def main():
    app = QApplication(sys.argv)
    display = QueenDisplay()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
