#! /usr/bin/env python3
from __future__ import print_function
from itertools import groupby, chain
import sys

NONE = '.'
RED = 'X'
YELLOW = 'O'

def diagonalsPos (matrix, cols, rows):
    """Get positive diagonals, going from bottom-left to top-right."""
    for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows -1)):
        yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

def diagonalsNeg (matrix, cols, rows):
    """Get negative diagonals, going from top-left to bottom-right."""
    for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

class Game:
    def __init__ (self, cols = 7, rows = 6, requiredToWin = 4):
        """Create a new game."""
        self.cols = cols
        self.rows = rows
        self.win = requiredToWin
        self.board = [[NONE] * rows for _ in range(cols)]

    def insert (self, column, color):
        """Insert the color in the given column."""
        c = self.board[column]
        if c[0] != NONE:
            raise RuntimeError('Sorry, the column is full!')

        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = color

        self.checkForWin()

    def checkForWin (self):
        """Check the current board for a winner."""
        w = self.getWinner()
        if w:
            self.printBoard()
            print(w + ' won!')
            sys.exit()

    def getWinner (self):
        """Get the winner on the current board."""
        lines = (
            self.board, # columns
            zip(*self.board), # rows
            diagonalsPos(self.board, self.cols, self.rows), # positive diagonals
            diagonalsNeg(self.board, self.cols, self.rows) # negative diagonals
        )

        for line in chain(*lines):
            for color, group in groupby(line):
                if color != NONE and len(list(group)) >= self.win:
                    return color

    def printBoard (self):
        """Print the board."""
        print('  '.join(map(str, range(1, self.cols + 1))))
        for y in range(self.rows):
            print('  '.join(str(self.board[x][y]) for x in range(self.cols)))
        print()


if __name__ == '__main__':
    g = Game()
    turn = RED
    while True:
        g.printBoard()
        try:
            row = int(input('{}\'s turn: '.format(RED if turn == RED else YELLOW))) - 1
            g.insert(int(row), turn)
            turn = YELLOW if turn == RED else RED
        except ValueError:
            print("Sorry, you need a number from 1 to 7.\n")
        except IndexError:
            print("Sorry, you can't put a marker there.\n")
        except RuntimeError as e:
            print(e)
