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
if is_checkmate(new_game.board, new_game.active_color, new_game.en_passant, new_game.squares):
    print("Checkmate! This shouldn't happen at game start.")
elif is_stalemate(new_game.board, new_game.active_color, new_game.en_passant, new_game.squares):
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
        move_parts = move.split()
        if len(move_parts) < 2:
            print("Invalid move format. Use: from_square to_square [promotion_piece]")
            continue
        sq1, sq2 = move_parts[0], move_parts[1]
        promotion_piece = move_parts[2] if len(move_parts) > 2 else None

    # Check if this is a pawn promotion move
    pos1 = new_game.squares[sq1]
    pos2 = new_game.squares[sq2]
    piece = new_game.board[pos1[0]][pos1[1]]
    is_promotion = False
    
    if piece in "Pp":
        if (piece == "P" and pos2[0] == 0) or (piece == "p" and pos2[0] == 7):
            is_promotion = True
            if not promotion_piece:
                while True:
                    promotion_piece = input("Pawn promotion! Choose piece (Q/R/B/N): ").strip().upper()
                    if piece == "p":  # black pawn
                        promotion_piece = promotion_piece.lower()
                    if promotion_piece in (["Q", "R", "B", "N"] if piece == "P" else ["q", "r", "b", "n"]):
                        break
                    print("Invalid choice. Choose Q, R, B, or N.")

    while not new_game.validate_move(sq1, sq2, promotion_piece):
        move = input("Invalid move. Try again: ").strip().lower()
        move_parts = move.split()
        if len(move_parts) < 2:
            continue
        sq1, sq2 = move_parts[0], move_parts[1]
        promotion_piece = move_parts[2] if len(move_parts) > 2 else None
        
        # Re-check for promotion
        pos1 = new_game.squares[sq1]
        pos2 = new_game.squares[sq2]
        piece = new_game.board[pos1[0]][pos1[1]]
        is_promotion = False
        
        if piece in "Pp":
            if (piece == "P" and pos2[0] == 0) or (piece == "p" and pos2[0] == 7):
                is_promotion = True
                if not promotion_piece:
                    while True:
                        promotion_piece = input("Pawn promotion! Choose piece (Q/R/B/N): ").strip().upper()
                        if piece == "p":  # black pawn
                            promotion_piece = promotion_piece.lower()
                        if promotion_piece in (["Q", "R", "B", "N"] if piece == "P" else ["q", "r", "b", "n"]):
                            break
                        print("Invalid choice. Choose Q, R, B, or N.")

    new_game.play(sq1, sq2, promotion_piece)
    print_board(new_game.board)
    print()
    
    # Check game state after move
    if is_checkmate(new_game.board, new_game.active_color, new_game.en_passant, new_game.squares):
        winner = "White" if new_game.active_color == "b" else "Black"
        print(f"Checkmate! {winner} wins!")
        game_over = True
    elif is_stalemate(new_game.board, new_game.active_color, new_game.en_passant, new_game.squares):
        print("Stalemate! The game is a draw.")
        game_over = True
    elif is_check(new_game.board, new_game.active_color):
        color_name = "White" if new_game.active_color == "w" else "Black"
        print(f"{color_name} is in check!")