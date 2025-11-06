import sys
from chess_game_functions import generate_board, check_castling_rights


fen_string =  sys.argv[1]

to_move = fen_string.split(" ")[1]
en_passant = fen_string.split(" ")[3]
half_move = fen_string.split(" ")[4]
full_move = fen_string.split(" ")[5]


board = generate_board(fen_string)     # generate board
for row in board:                      # print board
    print(*row)


if to_move == "w":  # print to move
    print("\nWhite to move")
elif to_move == "b":
    print("\nBlack to move")


print(check_castling_rights(fen_string))    # print castling rights


if en_passant == "-":   # print en passant square
    print("No en passant square")
else:
    print(f"En passant square: {en_passant}")


print(f"Halfmove clock: {half_move}")   # print halfmove clock
print(f"Fullmove number: {full_move}")  # print fullmove number
