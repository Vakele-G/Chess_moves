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

# Check initial game state
if is_checkmate(new_game.board, new_game.active_color):
    print("Checkmate! This shouldn't happen at game start.")
elif is_stalemate(new_game.board, new_game.active_color):
    print("Stalemate! This shouldn't happen at game start.")
elif is_check(new_game.board, new_game.active_color):
    color_name = "White" if new_game.active_color == "w" else "Black"
    print(f"{color_name} is in check!")

game_over = False

while not game_over:
    move = input("\nEnter a move (eg. e2 e4) or 'q' to quit: ").strip().lower()
    if move == "q":
        print("Goodbye.")
        break
    else:
        move = move.split()

    while not new_game.validate_move(move[0], move[1]):
        move = input("Invalid move. Try again: ").strip().split()

    new_game.play(move[0], move[1])
    print_board(new_game.board)
    print()
    
    # Check game state after move
    if is_checkmate(new_game.board, new_game.active_color):
        winner = "White" if new_game.active_color == "b" else "Black"
        print(f"Checkmate! {winner} wins!")
        game_over = True
    elif is_stalemate(new_game.board, new_game.active_color):
        print("Stalemate! The game is a draw.")
        game_over = True
    elif is_check(new_game.board, new_game.active_color):
        color_name = "White" if new_game.active_color == "w" else "Black"
        print(f"{color_name} is in check!")