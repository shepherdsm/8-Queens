#!/usr/bin/python3

"""
Runs the queens implementation in a, hopefully, independant of implementation way.
I'm trying to hide everything behind function calls so the internals can be changed
without having to change the running program.

Author: Scott Shepherd
Ver: 1.0
"""

import queens
import time

solutions = 0

def find_solutions(board, move_list, cur_row, cur_moves):
    if cur_row != len(board):
        for move in move_list:
            if queens.is_valid_move(move, board, cur_row):
                cur_moves.append(queens.make_move(move, board, cur_row))
                find_solutions(board, move_list, cur_row + 1, cur_moves)
        try:
            queens.remove_move(cur_moves.pop(), cur_row - 1, board)
        except IndexError:
            pass
    else:
        global solutions
        solutions += 1
        #queens.print_board(board)
        try:
            queens.remove_move(cur_moves.pop(), cur_row - 1, board)
        except IndexError:
            pass
            

if __name__ == "__main__":
    for size in range(4, 15):
        board = queens.init_board(size)
        start = time.time()
        find_solutions(board, queens.possible_moves(size), 0, [])
        print ("It took {} seconds.".format(time.time() - start))
        print ("Found {} solutions for size {}".format(solutions, size))
        solutions = 0
