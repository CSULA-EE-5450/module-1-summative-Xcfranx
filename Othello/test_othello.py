from unittest import TestCase, mock


class Testothello(TestCase):
    def board_d(board):
        board.assertEqual(len(board.othello._board_d(1)), 52)
