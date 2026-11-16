import unittest

from src.game_functions import SQUARES, Game, is_square_attacked, square_name

START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class BasicLegalityTest(unittest.TestCase):
    def test_pawn_moves_from_start(self):
        game = Game(START)
        self.assertTrue(game.validate_move("e2", "e3"))
        self.assertTrue(game.validate_move("e2", "e4"))
        self.assertFalse(game.validate_move("e2", "e5"))
        self.assertFalse(game.validate_move("e2", "d3"))   # nothing to capture

    def test_blocked_pawn_cannot_move_or_double_push(self):
        game = Game("4k3/8/8/8/8/4p3/4P3/4K3 w - - 0 1")
        self.assertFalse(game.validate_move("e2", "e3"))
        self.assertFalse(game.validate_move("e2", "e4"))

    def test_knight_and_bishop(self):
        game = Game(START)
        self.assertTrue(game.validate_move("g1", "f3"))
        self.assertFalse(game.validate_move("g1", "g3"))
        self.assertFalse(game.validate_move("g1", "e2"))   # own pawn
        self.assertFalse(game.validate_move("f1", "e2"))   # own pawn

    def test_cannot_move_opponents_piece(self):
        self.assertFalse(Game(START).validate_move("e7", "e5"))

    def test_cannot_capture_own_piece(self):
        self.assertFalse(Game(START).validate_move("a1", "a2"))

    def test_garbage_input_is_rejected(self):
        game = Game(START)
        self.assertFalse(game.validate_move("e4", "e5"))   # empty start square
        self.assertFalse(game.validate_move("e2", "e2"))   # same square
        self.assertFalse(game.validate_move("z9", "e4"))
        self.assertFalse(game.validate_move("e2", "z9"))

    def test_play_raises_on_illegal_move(self):
        with self.assertRaises(ValueError):
            Game(START).play("e2", "e5")


class CheckAndPinTest(unittest.TestCase):
    def test_must_respond_to_check(self):
        # Black rook on e8 checks the White king on e1.
        game = Game("4r2k/8/8/8/8/8/8/R3K3 w - - 0 1")
        self.assertFalse(game.validate_move("a1", "a2"))   # ignores the check
        self.assertFalse(game.validate_move("e1", "e2"))   # still on the e-file
        self.assertTrue(game.validate_move("e1", "d1"))
        self.assertTrue(game.validate_move("e1", "f1"))

    def test_pinned_piece_cannot_leave_the_pin_line(self):
        game = Game("4r2k/8/8/8/8/8/4R3/4K3 w - - 0 1")
        self.assertFalse(game.validate_move("e2", "a2"))
        self.assertTrue(game.validate_move("e2", "e5"))    # stays on the e-file
        self.assertTrue(game.validate_move("e2", "e8"))    # captures the pinner

    def test_king_cannot_step_into_check(self):
        game = Game("4k3/8/8/8/8/8/3r4/4K3 w - - 0 1")
        self.assertFalse(game.validate_move("e1", "e2"))
        self.assertFalse(game.validate_move("e1", "d1"))
        self.assertFalse(game.validate_move("e1", "f2"))
        self.assertTrue(game.validate_move("e1", "f1"))
        self.assertTrue(game.validate_move("e1", "d2"))    # captures the undefended rook


class EnPassantTest(unittest.TestCase):
    BLACK_EP = "rnbqkbnr/ppp1pppp/8/8/3pP3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"

    def test_black_captures_en_passant(self):
        game = Game(self.BLACK_EP)
        self.assertTrue(game.validate_move("d4", "e3"))
        game.play("d4", "e3")
        self.assertEqual(game.board[5][4], "p")    # e3
        self.assertEqual(game.board[4][4], ".")    # captured pawn on e4 is gone
        self.assertEqual(game.board[4][3], ".")    # d4 vacated
        self.assertEqual(game.en_passant, "-")
        self.assertEqual((game.half_move, game.full_move), (0, 2))

    def test_white_captures_en_passant(self):
        game = Game("rnbqkbnr/pppp1ppp/8/3Pp3/8/8/PPP1PPPP/RNBQKBNR w KQkq e6 0 3")
        self.assertTrue(game.validate_move("d5", "e6"))
        game.play("d5", "e6")
        self.assertEqual(game.board[2][4], "P")    # e6
        self.assertEqual(game.board[3][4], ".")    # captured pawn on e5 is gone
        self.assertEqual(game.board[3][3], ".")

    def test_en_passant_target_is_set_and_cleared(self):
        game = Game(START)
        game.play("e2", "e4")
        self.assertEqual(game.en_passant, "e3")
        game.play("c7", "c5")
        self.assertEqual(game.en_passant, "c6")
        game.play("g1", "f3")
        self.assertEqual(game.en_passant, "-")

    def test_h_file_double_push_sets_target(self):
        # Regression for the "abcdefg" typo in square_name.
        white = Game("4k3/8/8/8/8/8/7P/4K3 w - - 0 1")
        white.play("h2", "h4")
        self.assertEqual(white.en_passant, "h3")

        black = Game("4k3/7p/8/8/8/8/8/4K3 b - - 0 1")
        black.play("h7", "h5")
        self.assertEqual(black.en_passant, "h6")

    def test_en_passant_expires_after_one_move(self):
        game = Game(self.BLACK_EP)
        game.play("a7", "a6")
        game.play("a2", "a3")
        self.assertFalse(game.validate_move("d4", "e3"))

    def test_en_passant_that_exposes_own_king_is_illegal(self):
        # Capturing removes both pawns from rank 4 and opens the queen's line to a4.
        game = Game("8/8/8/8/k2Pp2Q/8/8/4K3 b - d3 0 1")
        self.assertFalse(game.validate_move("e4", "d3"))
        self.assertTrue(game.validate_move("e4", "e3"))


class PromotionTest(unittest.TestCase):
    def test_promotion_piece_is_required(self):
        game = Game("4k3/P7/8/8/8/8/8/4K3 w - - 0 1")
        self.assertFalse(game.validate_move("a7", "a8"))
        self.assertFalse(game.validate_move("a7", "a8", "k"))
        for piece in "qrbn":
            with self.subTest(piece=piece):
                self.assertTrue(game.validate_move("a7", "a8", piece))
        with self.assertRaises(ValueError):
            game.play("a7", "a8")

    def test_promotion_piece_rejected_on_normal_move(self):
        game = Game("4k3/8/8/8/8/8/P7/4K3 w - - 0 1")
        self.assertFalse(game.validate_move("a2", "a3", "q"))

    def test_white_promotes_to_rook(self):
        game = Game("4k3/P7/8/8/8/8/8/4K3 w - - 0 1")
        game.play("a7", "a8", "r")
        self.assertEqual(game.board[0][0], "R")
        self.assertEqual(game.board[1][0], ".")
        self.assertEqual(game.status(), "check")

    def test_black_promotes_with_capture(self):
        game = Game("4k3/8/8/8/8/8/p7/1R2K3 b - - 0 1")
        self.assertTrue(game.validate_move("a2", "b1", "q"))
        game.play("a2", "b1", "q")
        self.assertEqual(game.board[7][1], "q")
        self.assertEqual(game.board[6][0], ".")

    def test_promoting_on_a_rook_removes_castling_right(self):
        game = Game("r3k3/1P6/8/8/8/8/8/4K3 w q - 0 1")
        game.play("b7", "a8", "q")
        self.assertEqual(game.castling, "-")


class CastlingEdgeTest(unittest.TestCase):
    def test_attacked_b_file_square_does_not_block_queenside(self):
        # The rook on b8 attacks b1, but the king only crosses e1, d1 and c1.
        game = Game("1r2k3/8/8/8/8/8/8/R3K3 w Q - 0 1")
        self.assertTrue(game.validate_move("e1", "c1"))

    def test_no_rights_means_no_castling(self):
        game = Game("r3k2r/8/8/8/8/8/8/R3K2R w - - 0 1")
        self.assertFalse(game.validate_move("e1", "g1"))
        self.assertFalse(game.validate_move("e1", "c1"))


class HelperTest(unittest.TestCase):
    def test_square_name_matches_squares_table(self):
        for name, pos in SQUARES.items():
            with self.subTest(square=name):
                self.assertEqual(square_name(pos), name)

    def test_pawn_attack_directions(self):
        white = Game("4k3/8/8/8/4P3/8/8/4K3 w - - 0 1").board
        self.assertTrue(is_square_attacked(white, (3, 3), "w"))    # d5
        self.assertTrue(is_square_attacked(white, (3, 5), "w"))    # f5
        self.assertFalse(is_square_attacked(white, (3, 4), "w"))   # e5, straight ahead
        self.assertFalse(is_square_attacked(white, (5, 3), "w"))   # d3, behind

        black = Game("4k3/8/8/4p3/8/8/8/4K3 w - - 0 1").board
        self.assertTrue(is_square_attacked(black, (4, 3), "b"))    # d4
        self.assertTrue(is_square_attacked(black, (4, 5), "b"))    # f4
        self.assertFalse(is_square_attacked(black, (2, 3), "b"))   # d6, behind

    def test_sliders_are_blocked_by_pieces(self):
        open_file = Game("4k3/8/8/8/8/8/8/R3K3 w - - 0 1").board
        blocked = Game("4k3/8/8/8/8/8/P7/R3K3 w - - 0 1").board
        self.assertTrue(is_square_attacked(open_file, (0, 0), "w"))    # a8
        self.assertFalse(is_square_attacked(blocked, (0, 0), "w"))


if __name__ == "__main__":
    unittest.main()