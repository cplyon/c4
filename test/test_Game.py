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

from c4.c4 import Game
from c4.c4 import Colour
from c4.c4 import Player


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
        game.board.is_full = lambda: True
        self.assertEqual(game.determine_winner(Colour.PLAYER_1, 0, 0),
                         Game.TIE)

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


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
