import unittest
from game_functions import generate_board, board_to_fen

class ViewFenTest(unittest.TestCase):
    def test_board(self):
        self.assertEqual(generate_board("rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq e3 0 1"),
                                       [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], 
                                        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], 
                                        ['.', '.', '.', '.', '.', '.', '.', '.'], 
                                        ['.', '.', '.', '.', '.', '.', '.', '.'], 
                                        ['.', '.', '.', 'P', '.', '.', '.', '.'], 
                                        ['.', '.', '.', '.', '.', '.', '.', '.'], 
                                        ['P', 'P', 'P', '.', 'P', 'P', 'P', 'P'], 
                                        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']])
        
    def test_fen_string(self):
        with self.assertRaises(ValueError):
            generate_board("rnbqkbnrr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq e3 0 1")   # extra black rook
            generate_board("rnbqkbnr/pppppppp/9/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq e3 0 1")    # extra empty square
            generate_board("rnbqkbnrr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq e3 0 1 8") # extra parameter
            generate_board("rnbqkbnrr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR L KQkq e3 0 1")   # not "w" or "b" to play

    def test_board_to_fen(self):
        board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'P', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', '.', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ]
        self.assertEqual(
            board_to_fen(board),
            "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR",
        )

    def test_board_to_fen_all_empty_row_compression(self):
        board = [['.' for _ in range(8)] for _ in range(8)]
        board[0][0] = 'K'
        board[7][7] = 'k'
        self.assertEqual(
            board_to_fen(board),
            "K7/8/8/8/8/8/8/7k",
        )


if __name__ == '__main__':
    unittest.main()
