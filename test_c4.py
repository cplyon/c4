#!/usr/bin/env python3

"""
Tests for simple Connect Four game.
Author: Chris Lyon
Contact: chris@cplyon.ca
Date: 2015-09-19
"""

import logging
import unittest
from c4 import *

class GameTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_play_invalid_columns(self):
        game = Game()
        self.assertFalse(game.play('a'))
        self.assertFalse(game.play(0))
        self.assertFalse(game.play(game.board.columns + 1))

    def test_play_full_column(self):
        game = Game()
        for r in range(game.board.rows):
            # fill up column
            game.board[r][0] = Colour.PLAYER_1
        self.assertFalse(game.play(1))

    def test_play_empty_board(self):
        game = Game()
        self.assertEqual(game.board[game.board.rows-1][0], Colour.NONE)
        self.assertTrue(game.play(1))
        self.assertEqual(game.board[game.board.rows-1][0], Colour.PLAYER_1)

    def test_play_turn_ends(self):
        game = Game()
        self.assertEqual(game.turn, game.player1)
        self.assertTrue(game.play(1))
        self.assertEqual(game.turn, game.player2)

    def test_play_fill_column(self):
        game = Game()
        for row in reversed(range(game.board.rows)):
            self.assertTrue(game.play(1))
            if row % 2 == 0:
                self.assertEqual(game.board[row][0], Colour.PLAYER_2)
            else:
                self.assertEqual(game.board[row][0], Colour.PLAYER_1)
        self.assertFalse(game.play(1))

    def test_play_empty_board_winner(self):
        game = Game()
        self.assertEqual(game.winner, None)
        self.assertTrue(game.play(1))
        self.assertEqual(game.winner, None)

    def test_play_player1_winner(self):
        game = Game()
        for r in range(4):
            game.play(1)
            game.play(2)
        self.assertEqual(game.winner, game.player1.name)

    def test_determine_winner_empty_board(self):
        game = Game()
        self.assertIsNone(game.determine_winner(Colour.PLAYER_1, 0, 0))

    def test_determine_winner_full_board(self):
        game = Game()
        game.board.is_full = lambda : True
        self.assertEqual(game.determine_winner(Colour.PLAYER_1, 0, 0), Game.TIE)

    def test_determine_winner_vertical(self):
        game = Game()
        game.board[0][game.board.columns - 1] = Colour.PLAYER_1
        self.assertIsNone(game.determine_winner(Colour.PLAYER_1, 0,
            game.board.columns - 1))
        game.board[1][game.board.columns - 1] = Colour.PLAYER_1
        self.assertIsNone(game.determine_winner(Colour.PLAYER_1, 0,
            game.board.columns - 1))
        game.board[2][game.board.columns - 1] = Colour.PLAYER_1
        self.assertIsNone(game.determine_winner(Colour.PLAYER_1, 0,
            game.board.columns - 1))
        game.board[3][game.board.columns - 1] = Colour.PLAYER_1
        self.assertEqual(game.determine_winner(Colour.PLAYER_1, 0,
            game.board.columns - 1), Player.PLAYER_1)

    def test_determine_winner_horizontal(self):
        game = Game()
        game.board[game.board.rows - 1][0] = Colour.PLAYER_1
        self.assertIsNone(game.determine_winner(Colour.PLAYER_1,
            game.board.rows - 1, 0))
        game.board[game.board.rows - 1][1] = Colour.PLAYER_1
        self.assertIsNone(game.determine_winner(Colour.PLAYER_1,
            game.board.rows - 1, 0))
        game.board[game.board.rows - 1][2] = Colour.PLAYER_1
        self.assertIsNone(game.determine_winner(Colour.PLAYER_1,
            game.board.rows - 1, 0))
        game.board[game.board.rows - 1][3] = Colour.PLAYER_1
        self.assertEqual(game.determine_winner(Colour.PLAYER_1,
            game.board.rows - 1, 0), Player.PLAYER_1)

    def test_determine_winner_diagonal_tl_br(self):
        game = Game()
        game.board[0][0] = Colour.PLAYER_1
        self.assertIsNone(game.determine_winner(Colour.PLAYER_1, 0, 0))
        game.board[1][1] = Colour.PLAYER_1
        self.assertIsNone(game.determine_winner(Colour.PLAYER_1, 0, 0))
        game.board[2][2] = Colour.PLAYER_1
        self.assertIsNone(game.determine_winner(Colour.PLAYER_1, 0, 0))
        game.board[3][3] = Colour.PLAYER_1
        self.assertEqual(game.determine_winner(Colour.PLAYER_1, 0, 0),
                Player.PLAYER_1)

    def test_determine_winner_diagonal_tr_bl(self):
        game = Game()
        game.board[0][3] = Colour.PLAYER_1
        self.assertIsNone(game.determine_winner(Colour.PLAYER_1, 0, 3))
        game.board[1][2] = Colour.PLAYER_1
        self.assertIsNone(game.determine_winner(Colour.PLAYER_1, 0, 3))
        game.board[2][1] = Colour.PLAYER_1
        self.assertIsNone(game.determine_winner(Colour.PLAYER_1, 0, 3))
        game.board[3][0] = Colour.PLAYER_1
        self.assertEqual(game.determine_winner(Colour.PLAYER_1, 0, 3),
                Player.PLAYER_1)


class BoardTest(unittest.TestCase):
    def test_is_full_negative(self):
        board = Board()
        self.assertFalse(board.is_full())

    def test_is_full_positive(self):
        board = Board()
        for c in range(board.columns):
            for r in range(board.rows):
                board.drop_piece(Colour.PLAYER_1, c)
        self.assertEqual(board.filled_cells, board.rows * board.columns)
        self.assertTrue(board.is_full())

    def test_is_column_full_negative(self):
        board = Board()
        self.assertFalse(board.is_column_full(0))

    def test_is_column_full_positive(self):
        board = Board()
        for r in range(board.rows):
            board.drop_piece(Colour.PLAYER_1, 0)
        self.assertTrue(board.is_column_full(0))

    def test_drop_piece_empty_column(self):
        board = Board()
        self.assertEqual(board.drop_piece(Colour.PLAYER_1, 0), board.rows - 1)
        self.assertEqual(board[board.rows - 1][0], Colour.PLAYER_1)

    def test_drop_piece_full_column(self):
        board = Board()
        for r in range(board.rows):
            self.assertIsNotNone(board.drop_piece(Colour.PLAYER_1, 0))
        self.assertIsNone(board.drop_piece(Colour.PLAYER_1, 0))

    def test_check_top_left_to_bottom_right_positive(self):
        board = Board()
        for r in range(board.rows):
            for c in range(board.columns):
                board._board[r][c] = Colour.PLAYER_1
        for r in range(board.rows):
            for c in range(board.columns):
                if (r, c) not in [(0,4), (0,5), (0,6), (1,5), (1,6), (2,6), (3,0), (4,0),
                        (4,1), (5,0), (5,1), (5,2)]:
                    self.assertTrue(board.check_top_left_to_bottom_right(Colour.PLAYER_1,
                        r, c, 4))

    def test_check_top_left_to_bottom_right_negative(self):
        board = Board()
        for r in range(board.rows):
            for c in range(board.columns):
                board._board[r][c] = Colour.PLAYER_1
        for r in range(board.rows):
            for c in range(board.columns):
                if (r, c) in [(0,4), (0,5), (0,6), (1,5), (1,6), (2,6), (3,0), (4,0),
                        (4,1), (5,0), (5,1), (5,2)]:
                    self.assertFalse(board.check_top_left_to_bottom_right(Colour.PLAYER_1,
                        r, c, 4))
                    self.assertFalse(board.check_top_left_to_bottom_right(Colour.PLAYER_2,
                        r, c, 4))

    def test_check_top_right_to_bottom_left_positive(self):
        board = Board()
        for r in range(board.rows):
            for c in range(board.columns):
                board._board[r][c] = Colour.PLAYER_1
        for r in range(board.rows):
            for c in range(board.columns):
                if (r, c) not in [(0,0), (0,1), (0,2), (1,0), (1,1), (2,0), (3,6), (4,6),
                        (4,5), (5,6), (5,5), (5,4)]:
                    self.assertTrue(board.check_top_right_to_bottom_left(Colour.PLAYER_1,
                        r, c, 4))

    def test_check_top_right_to_bottom_left_negative(self):
        board = Board()
        for r in range(board.rows):
            for c in range(board.columns):
                board._board[r][c] = Colour.PLAYER_1
        for r in range(board.rows):
            for c in range(board.columns):
                if (r, c) in [(0,0), (0,1), (0,2), (1,0), (1,1), (2,0), (3,6), (4,6),
                        (4,5), (5,6), (5,5), (5,4)]:
                    self.assertFalse(board.check_top_right_to_bottom_left(Colour.PLAYER_1,
                        r, c, 4))
                    self.assertFalse(board.check_top_right_to_bottom_left(Colour.PLAYER_2,
                        r, c, 4))

    def test_check_horizontal_positive(self):
        board = Board()
        for r in range(board.rows):
            for c in range(board.columns):
                board._board[r][c] = Colour.PLAYER_1
        for r in range(board.rows):
            self.assertTrue(board.check_horizontal(Colour.PLAYER_1, r, 4))

    def test_check_horizontal_negative(self):
        board = Board()
        for r in range(board.rows):
            self.assertFalse(board.check_horizontal(Colour.PLAYER_1, r, 4))

    def test_check_vertical_positive(self):
        board = Board()
        for r in range(board.rows):
            for c in range(board.columns):
                board._board[r][c] = Colour.PLAYER_1
        for r in range(board.rows - 4):
            for c in range(board.columns):
                self.assertTrue(board.check_vertical(Colour.PLAYER_1, r, c, 4))

    def test_check_vertical_negative(self):
        board = Board()
        for r in range(board.rows):
            for c in range(board.columns):
                self.assertFalse(board.check_vertical(Colour.PLAYER_1, r, c, 4))

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
