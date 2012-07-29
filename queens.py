#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
My implementation for solving the Queen's problem. Uses the most naive brute-force
approach. I'm attempting to be clever by treating everything as bits to save on space,
and hopefully save on computation time. We'll see how it goes, eh?

Author: Scott Shepherd
Ver: 1.0
"""

import math

ALL_SOLS = []

def init_board(size):
    """
    Takes in a size for a side of the board, and makes a list of 0s of length size.

    Returns a list of 0s len size.
    """
    if size < 4:
        raise ValueError("The board size must be 4 or more.")

    return [0] * size

def is_valid_move(move, board, row):
    """
    Checks a given queen move on the board to see if it's valid.

    Returns True for valid moves, False otherwise.
    """

    # See if the current move choice can even go on the board
    if move & board[row] != 0:
        return False
    else:
        board_size = len(board)
        mvs = invalid_spots(move, row, board_size)
        for i in range(board_size):
            if mvs[i] & board[i] != 0:
                return False
        return True

def print_board(board):
    """
    Prints the board so it's not so damn hard to read what's going on. :|
    """

    text = "{:0>%d}" % len(board)
    for move in board:
        print(text.format(bin(move)[2:].replace('1', 'Q')))

def make_move(move, board, row):
    """
    Makes a move onto the board for a given row.
    Updates the board inplace and returns the move made.

    Returns the move if valid.
    """
    board[row] ^= move
    return move
    

def remove_move(move, row, board):
    """
    Removes the given move from the board.
    """
    
    board[row] ^= move

def invalid_spots(move, move_row, size):
    """
    Takes in a move, then makes a list containing all of the spots
    that are invalidated by that move.
    
    Returns the list of invalidated locations.
    """

    moves = []
    col = size - int(math.log(move, 2)) - 1 # Get the column the move falls into
    for cur_row in range(size):
        diff = abs(cur_row - move_row)
        if diff != 0:
            left = right = 0
            if col - diff >= 0:
                left = 2 ** (size - 1) >> (col - diff)
            if col + diff < size:
                right = 1 << (size - (col + diff) - 1)
            moves.append(left ^ right ^ move)
        else:
            moves.append(move)

    return moves

def possible_moves(size):
    """
    Given the size of the board, it makes a list containing the possible moves.

    Returns a list of the possible moves.
    """

    return [2 ** (n - 1) for n in range(size, 0, -1)]

def find_solutions_naive(board, move_list, cur_row, cur_moves):
    """
    Most naive implementation of finding the solution to the 8 queens.
    Doesn't rule anything out and bruteforces every possible attempt.
    Runs moderately fast enough up to about 11 queens.
    """
    if cur_row != len(board):
        for move in move_list:
            if is_valid_move(move, board, cur_row):
                cur_moves.append(make_move(move, board, cur_row))
                find_solutions(board, move_list, cur_row + 1, cur_moves)
        try:
            remove_move(cur_moves.pop(), cur_row - 1, board)
        except IndexError:
            pass
    else:
        global ALL_SOLS
        ALL_SOLS.append(cur_moves)
        try:
            remove_move(cur_moves.pop(), cur_row - 1, board)
        except IndexError:
            pass

def get_solutions():
    """
    Abstracts away the fact a global is used to collect the solutions as I might want to
    change that later to not quite be so spaghetti like.

    Returns a list of all the solutions found.
    """

    global ALL_SOLS
    return ALL_SOLS

if __name__ == "__main__":
    for size in range(4, 7):
        board = init_board(size)
        find_solutions_naive(board, possible_moves(size), 0, [])
        print ("Found {} solutions for size {}".format(len(get_solutions()), size))
