#!/usr/bin/env python3

"""
Simple Connect Four game.
Author: Chris Lyon
Contact: chris@cplyon.ca
Date: 2015-09-19
"""

import sys
from enum import IntEnum


class Colour(IntEnum):
    """
    Enum of possible cell values on the game board.
    """
    NONE = 0
    PLAYER_1 = 1
    PLAYER_2 = 2


class Player:
    """
    Encapsulates properties of a player.
    """
    PLAYER_1 = "Player 1"
    PLAYER_2 = "Player 2"

    def __init__(self, name: str, colour: Colour):
        self.name = name
        self.colour = colour


class Board:
    """
    The game board, with customizable size
    """

    def __init__(self, rows: int, columns: int, goal: int):
        self.rows = rows
        self.columns = columns
        self._board = [[Colour.NONE for x in range(self.columns)]
                       for x in range(self.rows)]
        self.filled_cells = 0
        self.goal = goal

    def __getitem__(self, key: int) -> Colour:
        """
        Allow indexing into the board, like a 2D array
        """
        return self._board[key]

    def __str__(self) -> str:
        """
        Return a string representation of the board.
        """
        printable_board = ""
        for r in range(self.rows):
            for c in range(self.columns):
                printable_board += "%d " % self._board[r][c]
            printable_board += "\n"
        return printable_board

    def is_full(self) -> bool:
        """
        Return True if all cells on board have been filled.
        Return False otherwise.
        """
        return (self.filled_cells == self.rows * self.columns)

    def is_column_full(self, column: int) -> bool:
        """
        Return True if top-most cell in column is not NONE
        Return False otherwise
        """
        return self._board[0][column] is not Colour.NONE

    def drop_piece(self, colour: Colour, column: int) -> int:
        """
        Set the lowest empty cell in column to colour.
        Return the row that was coloured.
        Return None if column is full.
        """
        for r in reversed(range(self.rows)):
            if self._board[r][column] is Colour.NONE:
                # we found the lowest empty cell
                self._board[r][column] = colour
                self.filled_cells += 1
                return r

        return None

    def check_top_left_to_bottom_right(self, colour: Colour,
                                       row: int, column: int) -> bool:
        """
        Return True if there exists a diagonal streak of length or more cells
        on the board in row.
        Return False otherwise.
        """
        # need to check entire diagonal, since a piece could have been added in
        # the middle of a streak
        streak_length = 0
        r = row - min(row, column)
        c = column - min(row, column)
        while r < self.rows and c < self.columns:
            if self._board[r][c] is colour:
                streak_length += 1
                if streak_length >= self.goal:
                    return True
            else:
                streak_length = 0
            r += 1
            c += 1
        return False

    def check_top_right_to_bottom_left(self, colour: Colour,
                                       row: int, column: int) -> bool:
        """
        Return True if there exists a diagonal streak of length or more cells
        on the board in row.
        Return False otherwise.
        """
        # need to check entire diagonal, since a piece could have been added in
        # the middle of a streak
        streak_length = 0
        r = row - min(row, self.columns - column - 1)
        c = column + min(row, self.columns - column - 1)
        while r < self.rows and c >= 0:
            if self._board[r][c] is colour:
                streak_length += 1
                if streak_length == self.goal:
                    return True
            else:
                streak_length = 0
            r += 1
            c -= 1
        return False

    def check_horizontal(self, colour: Colour, row: int) -> bool:
        """
        Return True if there exists a horizontal streak of length or more cells
        on the board in row.
        Return False otherwise.
        """
        streak_length = 0
        # need to check entire row, since a piece could have been added in the
        # middle of a streak
        for c in range(self.columns):
            if self._board[row][c] is colour:
                streak_length += 1
                if streak_length == self.goal:
                    return True
            else:
                streak_length = 0
        return False

    def check_vertical(self, colour: Colour, row: int, column: int) -> bool:
        """
        Return True if there exists a vertical streak of length or more cells
        on the board in column starting at row.
        Return False otherwise.
        """
        streak_length = 1
        # if the piece is less than goal cells away from the bottom, we know
        # there's no winner yet
        if self.rows - row < self.goal:
            return False

        # only need to check from this row down, since this piece is guaranteed
        # to be on top because of gravity
        for r in range(row + 1, self.rows):
            if self._board[r][column] is colour:
                streak_length += 1
                if streak_length == self.goal:
                    return True
            else:
                # we can bail as soon as we find a cell not the target colour
                break
        return False


class Game:
    """
    Contains turn logic and determines winner.
    """
    TIE = "TIE GAME!"
    DEFAULT_COLUMNS = 7
    DEFAULT_ROWS = 6
    GOAL = 4

    def __init__(self):
        self.player1 = Player(Player.PLAYER_1, Colour.PLAYER_1)
        self.player2 = Player(Player.PLAYER_2, Colour.PLAYER_2)
        self.board = Board(self.DEFAULT_ROWS, self.DEFAULT_COLUMNS, self.GOAL)
        self.winner = None
        self.turn = self.player1

    def play(self, column: int) -> bool:
        """
        Main game logic. Place a piece on the board, determine a winner
        and end the current player's turn.
        column is the desired index + 1 (1-based index from user input)
        Return True if piece was successfully placed into an empty cell.
        Return False if invalid or illegal column.
        """
        try:
            column = int(column) - 1
        except ValueError:
            # not a number
            return False
        if column < 0 or column >= self.board.columns:
            # out of bounds
            return False
        if self.board.is_column_full(column):
            # column is full
            return False

        # drop current player's piece into column
        row = self.board.drop_piece(self.turn.colour, column)

        # check for winner.  There can be only one!
        if not self.winner:
            self.winner = self.determine_winner(self.turn.colour, row, column)

        # end turn
        self.turn = self.player2 if self.turn is self.player1 else self.player1

        return True

    def determine_winner(self, colour: Colour, row: int,
                         column: int) -> Player:
        """
        Return the player name who has created a streak of four or more either
        horizontally, vertically or diagonally.
        Return Game.TIE if all board cells have been filled without a winner.
        Return None if game is not over.
        """

        if self.board.check_horizontal(colour, row) or \
                self.board.check_vertical(colour, row, column) or \
                self.board.check_top_left_to_bottom_right(colour, row,
                                                          column) or \
                self.board.check_top_right_to_bottom_left(colour, row, column):
            return self.turn.name

        if self.board.is_full():
            # no available spaces, and no winner found. Game over!
            return Game.TIE

        # no winner yet
        return None


def main(argv=None):
    game = Game()

    # game loop
    while True:
        print()
        print(game.board)
        print("%s choose a column:" % game.turn.name)
        user_input = sys.stdin.readline().strip()
        if str(user_input).lower() == 'q':
            sys.exit(0)
        if not game.play(user_input):
            print("Invalid column. Try again")
        if game.winner:
            break
    print()
    print(game.board)
    if game.winner == Game.TIE:
        print(Game.TIE)
    else:
        print("Winner is %s!" % game.winner)
    print()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
