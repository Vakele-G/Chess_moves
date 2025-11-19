import sys
from chess_game_functions import generate_board, print_board, check_castling_rights, game_state, white_pawn_moves, black_pawn_moves


fen_string =  sys.argv[1]

board = generate_board(fen_string)     # generate board

print_board(board)

game_state(fen_string)
print(f"White pawn moves: {white_pawn_moves(board)}")
print(f"Black pawn moves: {black_pawn_moves(board)}")
