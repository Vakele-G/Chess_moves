import contextlib
import io
import pathlib
import sys
import unittest
from unittest.mock import patch


import game as cli                    # noqa: E402
from game_functions import Game       # noqa: E402

START = cli.START_FEN


def run(func, *args, inputs=()):
    """Call func with input() scripted, returning (result, captured stdout)."""
    out = io.StringIO()
    with patch("builtins.input", side_effect=list(inputs)), contextlib.redirect_stdout(out):
        result = func(*args)
    return result, out.getvalue()


def played(*moves):
    game = Game(START)
    for move in moves:
        game.play(*move.split())
    return game


class AskMoveTest(unittest.TestCase):
    def test_plain_move(self):
        result, _ = run(cli.ask_move, Game(START), inputs=["e2 e4"])
        self.assertEqual(result, ("e2", "e4", None))

    def test_quit(self):
        result, _ = run(cli.ask_move, Game(START), inputs=["q"])
        self.assertIsNone(result)

    def test_retries_until_legal_and_ignores_case(self):
        result, out = run(cli.ask_move, Game(START), inputs=["hello", "e2 e9", "e2 e5", "E2 E4"])
        self.assertEqual(result, ("e2", "e4", None))
        self.assertIn("Invalid move", out)
        self.assertIn("Illegal move", out)

    def test_can_quit_after_an_illegal_move(self):
        result, _ = run(cli.ask_move, Game(START), inputs=["e2 e5", "q"])
        self.assertIsNone(result)

    def test_promotion_prompt_reprompts_on_bad_choice(self):
        game = Game("4k3/P7/8/8/8/8/8/4K3 w - - 0 1")
        result, out = run(cli.ask_move, game, inputs=["a7 a8", "x", "n"])
        self.assertEqual(result, ("a7", "a8", "n"))
        self.assertIn("Invalid choice", out)

    def test_inline_promotion_piece_skips_the_prompt(self):
        game = Game("4k3/P7/8/8/8/8/8/4K3 w - - 0 1")
        result, out = run(cli.ask_move, game, inputs=["a7 a8 q"])   # a prompt would exhaust inputs
        self.assertEqual(result, ("a7", "a8", "q"))
        self.assertNotIn("Pawn promotion", out)

    def test_illegal_promotion_does_not_prompt(self):
        # The knight on a8 blocks the pawn, so asking "which piece?" would be wrong.
        game = Game("n3k3/P7/8/8/8/8/8/4K3 w - - 0 1")
        result, out = run(cli.ask_move, game, inputs=["a7 a8", "q"])
        self.assertIsNone(result)
        self.assertIn("Illegal move", out)
        self.assertNotIn("Pawn promotion", out)


class ReadGameTest(unittest.TestCase):
    def test_new_game(self):
        game, _ = run(cli.read_game, inputs=["new game"])
        self.assertEqual(game.to_fen(), START)

    def test_bad_fen_reprompts(self):
        game, out = run(cli.read_game, inputs=["not a fen", "NEW GAME"])
        self.assertEqual(game.to_fen(), START)
        self.assertIn("Invalid FEN", out)

    def test_fen_case_is_preserved(self):
        fen = "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1"
        game, _ = run(cli.read_game, inputs=[fen])
        self.assertEqual(game.castling, "KQkq")
        self.assertEqual(game.board[7][4], "K")


class ReportStatusTest(unittest.TestCase):
    def check(self, game, expected_over, expected_text):
        over, out = run(cli.report_status, game)
        self.assertEqual(over, expected_over)
        self.assertIn(expected_text, out)

    def test_checkmate(self):
        self.check(played("f2 f3", "e7 e5", "g2 g4", "d8 h4"), True, "Black wins")

    def test_stalemate(self):
        self.check(Game("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1"), True, "Stalemate")

    def test_fifty_move(self):
        self.check(Game("4k3/8/8/8/8/8/8/R3K3 w - - 100 80"), True, "fifty-move")

    def test_insufficient_material(self):
        self.check(Game("4k3/8/8/8/8/8/8/4K3 w - - 0 1"), True, "insufficient material")

    def test_check_does_not_end_the_game(self):
        self.check(Game("4k3/8/8/8/8/8/8/4RK2 b - - 0 1"), False, "Black is in check")

    def test_quiet_position_prints_nothing(self):
        over, out = run(cli.report_status, Game(START))
        self.assertFalse(over)
        self.assertEqual(out, "")


if __name__ == "__main__":
    unittest.main()