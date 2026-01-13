import sys
from game_functions import generate_board, print_board, game_state, white_pawn_moves, black_pawn_moves, white_rook_moves, black_rook_moves, white_knight_moves, black_knight_moves, white_bishop_moves, black_bishop_moves
from game_functions import Game


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

print("/////////////////////////////////////////////////")
print("Type 'new game' to begin a fresh game as white OR")
fen_string = input("enter a FEN string to play from that position: ").strip().lower()

if fen_string == "new game":
    new_game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
else:
    new_game = Game(fen_string)

print()
print_board(new_game.board)

while True:
    move = input("\nEnter a move (eg. e2 e4): ")
    move = move.strip().split()
    new_game.play(move[0], move[1])

    print_board(new_game.board)
    print()


"""Right now, illegal moves are able to be played. Checks, checkmate, enpassant and promotion are not implemented"""