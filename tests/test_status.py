import unittest

from src.game_functions import Game, has_insufficient_material

START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def play_all(game, *moves):
    for move in moves:
        game.play(*move.split())
    return game


class CheckmateStalemateTest(unittest.TestCase):
    def test_start_position_has_no_status(self):
        self.assertIsNone(Game(START).status())

    def test_fools_mate(self):
        game = play_all(Game(START), "f2 f3", "e7 e5", "g2 g4", "d8 h4")
        self.assertEqual(game.status(), "checkmate")
        self.assertEqual(game.active_color, "w")

    def test_back_rank_mate(self):
        game = play_all(Game("6k1/5ppp/8/8/8/8/8/R3K3 w - - 0 1"), "a1 a8")
        self.assertEqual(game.status(), "checkmate")

    def test_stalemate(self):
        game = Game("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1")
        self.assertEqual(game.status(), "stalemate")

    def test_check(self):
        game = Game("4k3/8/8/8/8/8/8/4RK2 b - - 0 1")
        self.assertEqual(game.status(), "check")


class FiftyMoveRuleTest(unittest.TestCase):
    def test_draw_when_clock_reaches_100(self):
        game = Game("4k3/8/8/8/8/8/8/R3K3 w - - 99 80")
        self.assertIsNone(game.status())
        game.play("a1", "a2")
        self.assertEqual(game.half_move, 100)
        self.assertEqual(game.status(), "fifty_move")

    def test_loading_a_position_already_at_100(self):
        self.assertEqual(Game("4k3/8/8/8/8/8/8/R3K3 w - - 100 80").status(), "fifty_move")

    def test_pawn_move_resets_clock(self):
        game = Game("4k3/8/8/8/8/8/P7/4K3 w - - 99 80")
        game.play("a2", "a3")
        self.assertEqual(game.half_move, 0)
        self.assertIsNone(game.status())

    def test_capture_resets_clock(self):
        game = Game("4k3/8/8/8/8/8/r7/R3K3 w - - 40 30")
        game.play("a1", "a2")
        self.assertEqual(game.half_move, 0)

    def test_checkmate_beats_fifty_move_draw(self):
        game = Game("6k1/5ppp/8/8/8/8/8/R3K3 w - - 99 80")
        game.play("a1", "a8")
        self.assertEqual(game.half_move, 100)
        self.assertEqual(game.status(), "checkmate")


class InsufficientMaterialTest(unittest.TestCase):
    DRAWN = [
        "4k3/8/8/8/8/8/8/4K3",     # K v K
        "4k3/8/8/8/8/8/8/2B1K3",   # K+B v K
        "4k3/8/8/8/8/8/8/1N2K3",   # K+N v K
        "4kb2/8/8/8/8/8/8/2B1K3",  # bishops on the same colour (c1 and f8 are both dark)
    ]
    NOT_DRAWN = [
        "2b1k3/8/8/8/8/8/8/2B1K3",  # bishops on opposite colours
        "4k3/8/8/8/8/8/8/1NN1K3",   # two knights
        "4kb2/8/8/8/8/8/8/1N2K3",   # knight v bishop
        "4k3/8/8/8/8/8/P7/4K3",     # a pawn can promote
        "4k3/8/8/8/8/8/8/R3K3",     # a rook can mate
    ]

    def test_drawn_positions(self):
        for placement in self.DRAWN:
            with self.subTest(placement=placement):
                game = Game(f"{placement} w - - 0 1")
                self.assertTrue(has_insufficient_material(game.board))
                self.assertEqual(game.status(), "insufficient_material")

    def test_positions_that_are_not_drawn(self):
        for placement in self.NOT_DRAWN:
            with self.subTest(placement=placement):
                game = Game(f"{placement} w - - 0 1")
                self.assertFalse(has_insufficient_material(game.board))
                self.assertNotEqual(game.status(), "insufficient_material")

    def test_draw_is_detected_right_after_the_last_mating_piece_is_captured(self):
        # Black's bishop takes White's last rook, leaving K v K+B.
        game = Game("4k3/8/8/8/8/8/7R/4K1b1 b - - 0 1")
        self.assertIsNone(game.status())
        game.play("g1", "h2")
        self.assertEqual(game.status(), "insufficient_material")


class CounterAndFenTest(unittest.TestCase):
    def test_full_move_number_increments_after_black_moves(self):
        game = Game(START)
        game.play("e2", "e4")
        self.assertEqual(game.full_move, 1)
        game.play("e7", "e5")
        self.assertEqual(game.full_move, 2)

    def test_to_fen_through_an_opening(self):
        game = Game(START)
        game.play("e2", "e4")
        self.assertEqual(game.to_fen(), "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
        game.play("e7", "e5")
        self.assertEqual(game.to_fen(), "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2")
        game.play("g1", "f3")
        self.assertEqual(game.to_fen(), "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2")


if __name__ == "__main__":
    unittest.main()