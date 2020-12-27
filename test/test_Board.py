#!/usr/bin/env python3

"""
Tests for simple Connect Four game.
Author: Chris Lyon
Contact: chris@cplyon.ca
Date: 2015-09-19
"""

import logging
import sys
import unittest
from c4.c4 import Board
from c4.c4 import Colour


class BoardTest(unittest.TestCase):

    ROWS = 6
    COLUMNS = 7
    GOAL = 4

    def test_is_full_negative(self):
        board = Board(self.ROWS, self.COLUMNS, self.GOAL)
        self.assertFalse(board.is_full())

    def test_is_full_positive(self):
        board = Board(self.ROWS, self.COLUMNS, self.GOAL)
        for c in range(board.columns):
            for r in range(board.rows):
                board.drop_piece(Colour.PLAYER_1, c)
        self.assertEqual(board.filled_cells, board.rows * board.columns)
        self.assertTrue(board.is_full())

    def test_is_column_full_negative(self):
        board = Board(self.ROWS, self.COLUMNS, self.GOAL)
        self.assertFalse(board.is_column_full(0))

    def test_is_column_full_positive(self):
        board = Board(self.ROWS, self.COLUMNS, self.GOAL)
        for r in range(board.rows):
            board.drop_piece(Colour.PLAYER_1, 0)
        self.assertTrue(board.is_column_full(0))

    def test_drop_piece_empty_column(self):
        board = Board(self.ROWS, self.COLUMNS, self.GOAL)
        self.assertEqual(board.drop_piece(Colour.PLAYER_1, 0), board.rows - 1)
        self.assertEqual(board[board.rows - 1][0], Colour.PLAYER_1)

    def test_drop_piece_full_column(self):
        board = Board(self.ROWS, self.COLUMNS, self.GOAL)
        for r in range(board.rows):
            self.assertIsNotNone(board.drop_piece(Colour.PLAYER_1, 0))
        self.assertIsNone(board.drop_piece(Colour.PLAYER_1, 0))

    def test_check_top_left_to_bottom_right_positive(self):
        board = Board(self.ROWS, self.COLUMNS, self.GOAL)
        for r in range(board.rows):
            for c in range(board.columns):
                board._board[r][c] = Colour.PLAYER_1
        for r in range(board.rows):
            for c in range(board.columns):
                if (r, c) not in [
                        (0, 4), (0, 5), (0, 6), (1, 5), (1, 6), (2, 6),
                        (3, 0), (4, 0), (4, 1), (5, 0), (5, 1), (5, 2)
                        ]:
                    self.assertTrue(board.check_top_left_to_bottom_right(
                        Colour.PLAYER_1, r, c))

    def test_check_top_left_to_bottom_right_negative(self):
        board = Board(self.ROWS, self.COLUMNS, self.GOAL)
        for r in range(board.rows):
            for c in range(board.columns):
                board._board[r][c] = Colour.PLAYER_1
        for r in range(board.rows):
            for c in range(board.columns):
                if (r, c) in [
                        (0, 4), (0, 5), (0, 6), (1, 5), (1, 6), (2, 6),
                        (3, 0), (4, 0), (4, 1), (5, 0), (5, 1), (5, 2)
                        ]:
                    self.assertFalse(board.check_top_left_to_bottom_right(
                        Colour.PLAYER_1, r, c))
                    self.assertFalse(board.check_top_left_to_bottom_right(
                        Colour.PLAYER_2, r, c))

    def test_check_top_right_to_bottom_left_positive(self):
        board = Board(self.ROWS, self.COLUMNS, self.GOAL)
        for r in range(board.rows):
            for c in range(board.columns):
                board._board[r][c] = Colour.PLAYER_1
        for r in range(board.rows):
            for c in range(board.columns):
                if (r, c) not in [
                        (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0),
                        (3, 6), (4, 6), (4, 5), (5, 6), (5, 5), (5, 4)
                        ]:
                    self.assertTrue(board.check_top_right_to_bottom_left(
                        Colour.PLAYER_1, r, c))

    def test_check_top_right_to_bottom_left_negative(self):
        board = Board(self.ROWS, self.COLUMNS, self.GOAL)
        for r in range(board.rows):
            for c in range(board.columns):
                board._board[r][c] = Colour.PLAYER_1
        for r in range(board.rows):
            for c in range(board.columns):
                if (r, c) in [
                        (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0),
                        (3, 6), (4, 6), (4, 5), (5, 6), (5, 5), (5, 4)
                        ]:
                    self.assertFalse(board.check_top_right_to_bottom_left(
                        Colour.PLAYER_1, r, c))
                    self.assertFalse(board.check_top_right_to_bottom_left(
                        Colour.PLAYER_2, r, c))

    def test_check_horizontal_positive(self):
        board = Board(self.ROWS, self.COLUMNS, self.GOAL)
        for r in range(board.rows):
            for c in range(board.columns):
                board._board[r][c] = Colour.PLAYER_1
        for r in range(board.rows):
            self.assertTrue(board.check_horizontal(Colour.PLAYER_1, r))

    def test_check_horizontal_negative(self):
        board = Board(self.ROWS, self.COLUMNS, self.GOAL)
        for r in range(board.rows):
            self.assertFalse(board.check_horizontal(Colour.PLAYER_1, r))

    def test_check_vertical_positive(self):
        board = Board(self.ROWS, self.COLUMNS, self.GOAL)
        for r in range(board.rows):
            for c in range(board.columns):
                board._board[r][c] = Colour.PLAYER_1
        for r in range(board.rows - 4):
            for c in range(board.columns):
                self.assertTrue(board.check_vertical(Colour.PLAYER_1, r, c))

    def test_check_vertical_negative(self):
        board = Board(self.ROWS, self.COLUMNS, self.GOAL)
        for r in range(board.rows):
            for c in range(board.columns):
                self.assertFalse(board.check_vertical(
                    Colour.PLAYER_1, r, c))


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
