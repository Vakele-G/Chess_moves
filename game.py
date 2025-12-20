import sys
from game_functions import generate_board, print_board, game_state, white_pawn_moves, black_pawn_moves, white_rook_moves, black_rook_moves, white_knight_moves, black_knight_moves, white_bishop_moves, black_bishop_moves
from game_functions import Game

fen_string =  sys.argv[1]
'''
board = generate_board(fen_string)  # create 2d array of chess board

print_board(board)

game_state(fen_string)  # print state of game details
print(f"White pawn moves: {white_pawn_moves(board)}")
print(f"Black pawn moves: {black_pawn_moves(board)}")
print(f"White rook moves: {white_rook_moves(board)}")
print(f"Black rook moves: {black_rook_moves(board)}")
print(f"White knight moves: {white_knight_moves(board)}")
print(f"Black knight moves: {black_knight_moves(board)}")
print(f"White bishop moves: {white_bishop_moves(board)}")
print(f"Black bishop moves: {black_bishop_moves(board)}")
'''

new_game = Game(fen_string)
print_board(new_game.board)

while True:
    move = input("\nEnter a move (eg. e2 e4): ")
    move = move.strip().split()
    new_game.play(move[0], move[1])

    print_board(new_game.board)
    print()