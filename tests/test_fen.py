import unittest

from src.game_functions import Game, parse_fen

START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

VALID_FENS = [
    START,
    "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1",
    "rnbqkbnr/ppp1pppp/8/8/3pP3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
    "4k3/P7/8/8/8/8/8/4K3 w - - 0 1",      # pawn on the 7th rank is fine
    "4k3/8/8/8/8/8/8/4K2R b K - 0 1",      # right 'K' is backed by a rook on h1
    "4k3/8/8/8/8/8/8/R3K3 w Q - 100 80",
]

# (fen, regex that the error message must match)
INVALID_FENS = [
    ("4k3/8/8/8/8/8/8/4K3 w - -", "6 fields"),
    ("4k3/8/8/8/8/8/4K3 w - - 0 1", "8 ranks"),
    ("4k4/8/8/8/8/8/8/4K3 w - - 0 1", "describes 9 squares"),
    ("4k2/8/8/8/8/8/8/4K3 w - - 0 1", "describes 7 squares"),
    ("4x3/8/8/8/8/8/8/4K3 w - - 0 1", "Invalid character"),
    ("4k3/8/8/8/8/8/8/44 w - - 0 1", "adjacent digits"),
    ("4k3/8/8/8/8/8/8/4K3 x - - 0 1", "Side to move"),
    ("4k3/8/8/8/8/8/8/4K3 w qk - 0 1", "Castling field"),
    ("4k3/8/8/8/8/8/8/4K3 w KQkqx - 0 1", "Castling field"),
    ("4k3/8/8/8/8/8/8/4K3 w - e4 0 1", "En passant square must be"),
    ("4k3/8/8/8/8/8/8/4K3 w - - -1 1", "Half-move clock"),
    ("4k3/8/8/8/8/8/8/4K3 w - - x 1", "must be integers"),
    ("4k3/8/8/8/8/8/8/4K3 w - - 0 0", "at least 1"),
    ("4k3/8/8/8/8/8/8/8 w - - 0 1", "exactly one"),
    ("4k3/8/8/8/8/8/8/3KK3 w - - 0 1", "exactly one"),
    ("4k3/8/8/8/8/8/8/P3K3 w - - 0 1", "first or eighth"),
    ("P3k3/8/8/8/8/8/8/4K3 w - - 0 1", "first or eighth"),
    ("4k3/8/8/PPPPPPPP/P7/8/8/4K3 w - - 0 1", "more than 8 pawns"),
    ("4k3/8/8/8/8/8/8/4K3 w K - 0 1", "piece placement"),       # no rook on h1
    ("r3k3/8/8/8/8/8/8/4K3 w k - 0 1", "piece placement"),      # no rook on h8
    ("4k3/8/8/8/4P3/8/8/4K3 w - e3 0 1", "rank 6"),             # wrong rank for White to move
    ("4k3/8/8/8/8/8/8/4K3 b - e3 0 1", "two squares"),          # no pawn that could have just moved
    ("7k/8/8/8/8/8/8/4K2R w - - 0 1", "in check but"),          # Black in check, White to move
    ("8/8/8/8/8/8/4k3/4K3 w - - 0 1", "in check but"),          # adjacent kings
]


class ParseFenTest(unittest.TestCase):
    def test_valid_fens_load_and_round_trip(self):
        for fen in VALID_FENS:
            with self.subTest(fen=fen):
                self.assertEqual(Game(fen).to_fen(), fen)

    def test_invalid_fens_are_rejected_for_the_right_reason(self):
        for fen, reason in INVALID_FENS:
            with self.subTest(fen=fen):
                with self.assertRaisesRegex(ValueError, reason):
                    parse_fen(fen)

    def test_parsed_fields(self):
        state = parse_fen("rnbqkbnr/ppp1pppp/8/8/3pP3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
        self.assertEqual(state["active_color"], "b")
        self.assertEqual(state["castling"], "KQkq")
        self.assertEqual(state["en_passant"], "e3")
        self.assertEqual((state["half_move"], state["full_move"]), (0, 1))
        self.assertEqual(state["board"][4][3], "p")   # d4
        self.assertEqual(state["board"][4][4], "P")   # e4
        self.assertEqual(state["board"][7][4], "K")   # e1
        self.assertEqual(state["board"][0][4], "k")   # e8

    def test_extra_whitespace_is_tolerated(self):
        self.assertEqual(Game("  " + START + "  ").to_fen(), START)

    def test_fen_case_is_significant(self):
        # Regression: lower-casing a FEN turns White's pieces into Black's.
        with self.assertRaises(ValueError):
            parse_fen(START.lower())


if __name__ == "__main__":
    unittest.main()