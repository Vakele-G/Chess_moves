import sys
from game_functions import *


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
    move = input("\nEnter a move (eg. e2 e4) or 'q' to quit: ").strip().lower()
    if move == "q":
        break
    else:
        move = move.split()

    while not new_game.validate_move(move[0], move[1]):
        move = input("Invalid move. Try again: ").strip().split()

    new_game.play(move[0], move[1])
    print_board(new_game.board)
    print()

print("Goodbye!")



"""Right now, illegal moves are able to be played(step into or ignore checks).
Checks, checkmate, enpassant and promotion are not implemented"""