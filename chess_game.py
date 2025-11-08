import sys
from chess_game_functions import generate_board, check_castling_rights, game_state, white_pawn_moves


fen_string =  "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

board = generate_board(fen_string)     # generate board

for row in board:                      # print board
    print(*row)

game_state(fen_string)

print(white_pawn_moves(board))

