import unittest

from src.game_functions import Game


class CastlingTest(unittest.TestCase):
    def test_white_castles_kingside(self):
        game = Game("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")

        self.assertTrue(game.validate_move("e1", "g1"))
        game.play("e1", "g1")

        self.assertEqual(game.board[7][6], "K")
        self.assertEqual(game.board[7][5], "R")
        self.assertEqual(game.board[7][7], ".")
        self.assertEqual(game.board[7][4], ".")
        self.assertNotIn("K", game.castling)

    def test_white_castles_queenside(self):
        game = Game("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")

        self.assertTrue(game.validate_move("e1", "c1"))
        game.play("e1", "c1")

        self.assertEqual(game.board[7][2], "K")
        self.assertEqual(game.board[7][3], "R")
        self.assertEqual(game.board[7][0], ".")
        self.assertEqual(game.board[7][4], ".")

    def test_black_castles_kingside(self):
        game = Game("r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1")

        self.assertTrue(game.validate_move("e8", "g8"))
        game.play("e8", "g8")

        self.assertEqual(game.board[0][6], "k")
        self.assertEqual(game.board[0][5], "r")

    def test_castling_blocked_by_piece(self):
        # White queen on d1 blocks queenside castling.
        game = Game("r3k2r/8/8/8/8/8/8/R2QK2R w KQkq - 0 1")

        self.assertFalse(game.validate_move("e1", "c1"))
        self.assertTrue(game.validate_move("e1", "g1"))

    def test_castling_through_check_is_illegal(self):
        # Black rook on f2 attacks f1, which the king crosses.
        game = Game("4k3/8/8/8/8/8/5r2/R3K2R w KQ - 0 1")

        self.assertFalse(game.validate_move("e1", "g1"))

    def test_castling_out_of_check_is_illegal(self):
        # Black rook on e2 gives check on the e-file.
        game = Game("4k3/8/8/8/8/8/4r3/R3K2R w KQ - 0 1")

        self.assertFalse(game.validate_move("e1", "g1"))
        self.assertFalse(game.validate_move("e1", "c1"))

    def test_castling_right_lost_after_king_moves(self):
        game = Game("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")

        game.play("e1", "e2")

        self.assertEqual(game.castling, "kq")

    def test_castling_right_lost_after_rook_moves(self):
        game = Game("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")

        game.play("h1", "h2")
        self.assertEqual(game.castling, "Qkq")

        game.play("a8", "a7")
        self.assertEqual(game.castling, "Qk")

    def test_castling_right_lost_after_rook_is_captured(self):
        # Black queen on g2 can capture the white rook on h1.
        game = Game("r3k2r/8/8/8/8/8/6q1/R3K2R b KQkq - 0 1")

        game.play("g2", "h1")

        self.assertNotIn("K", game.castling)