"""Perft ("performance test") counts every legal line of play to a fixed depth.

The expected numbers are the standard reference values from the Chess
Programming Wiki. Matching them is strong evidence that castling, en passant,
promotion, pins and check handling are all correct together.

If one fails, the assertion message shows expected vs actual for that depth, and
the shallowest failing depth tells you roughly where the bug lives.
Each child position is re-created via Game(to_fen()), so this also exercises
to_fen() and the strict FEN validation on thousands of real positions.
"""
import unittest

from src.game_functions import Game, get_all_moves, square_name

PROMOTIONS = ("Q", "R", "B", "N", "q", "r", "b", "n")


def legal_moves(game):
    """All legal moves as (from_square, to_square, promotion_or_None)."""
    seen = set()
    result = []
    for move in get_all_moves(
        game.board, game.active_color, game.en_passant, game.squares, game.castling
    ):
        promo = move[2] if len(move) > 2 and move[2] in PROMOTIONS else None
        key = (move[0], move[1], promo)
        if key in seen:
            continue
        seen.add(key)
        sq1, sq2 = square_name(move[0]), square_name(move[1])
        if game.validate_move(sq1, sq2, promo):
            result.append((sq1, sq2, promo))
    return result


def perft(game, depth):
    if depth == 1:
        return len(legal_moves(game))
    total = 0
    for sq1, sq2, promo in legal_moves(game):
        child = Game(game.to_fen())
        child.play(sq1, sq2, promo)
        total += perft(child, depth - 1)
    return total


POSITIONS = {
    "start": (
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        [20, 400, 8902],
    ),
    "kiwipete (castling, pins, en passant)": (
        "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
        [48, 2039],               # depth 3 is 97862 (slow)
    ),
    "endgame (en passant discovered checks)": (
        "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1",
        [14, 191, 2812],
    ),
    "promotions and castling rights": (
        "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1",
        [6, 264, 9467],
    ),
    "promotion into check": (
        "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8",
        [44, 1486],
    ),
    "middlegame": (
        "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10",
        [46, 2079],
    ),
}


class PerftTest(unittest.TestCase):
    def test_reference_positions(self):
        for name, (fen, expected_counts) in POSITIONS.items():
            for depth, expected in enumerate(expected_counts, start=1):
                with self.subTest(position=name, depth=depth):
                    self.assertEqual(perft(Game(fen), depth), expected)


if __name__ == "__main__":
    unittest.main()