def generate_board(fen_string: str) -> list:
    board_string, to_move, castling_rights, en_passant, half_move, full_move = fen_string.split(" ")

    # Error Handling:
    # chess pieces
    for piece in board_string:
        if piece.lower() not in "12345678/rnbqkp":
            raise ValueError("Invalid chess piece or square")

    # number of squares in each row
    row1, row2, row3, row4, row5, row6, row7, row8 = board_string.split("/")
    for row in (row1, row2, row3, row4, row5, row6, row7, row8):
        if len(row) > 8 or len(row) < 1 or "9" in row:
            raise ValueError("Invalid number of squares in a row")

    # white or black players  
    if to_move.lower() != "w" and to_move != "b":
        raise ValueError("Only white or black can play")
    
    # en passant squares
    if en_passant != "-" and len(en_passant) != 2 and en_passant not in "abcdefgh12345678":
        raise ValueError("Invalid en passant square")
    
    # half and full moves
    if int(half_move) < 0 or int(full_move) < 0:
        raise ValueError("Move counter cannot be negative or a float")
    
    board = [[],[],[],[],[],[],[],[]]
    count =0
    empty_square = 0

    for pos in board_string:
        if pos == "/":
            count += 1
        if pos.isdigit():
            while empty_square != int(pos):
                empty_square += 1
                board[count].append(".")
        elif pos != "/":
            board[count].append(pos)
        empty_square = 0

    return board


def print_board(board: list) -> None:
    for row in board:                      # print board
        print(*row)
        

def game_state(fen_string: str) -> None:
    to_move = fen_string.split(" ")[1]
    en_passant = fen_string.split(" ")[3]
    half_move = fen_string.split(" ")[4]
    full_move = fen_string.split(" ")[5]

    if to_move == "w":  # print to move
        print("\nWhite to move")
    elif to_move == "b":
        print("\nBlack to move")

    print(check_castling_rights(fen_string))
    if en_passant == "-":   # print en passant square
        print("No en passant square")
    else:
        print(f"En passant square: {en_passant}")


def check_castling_rights(fen_string: str) -> str:

    castling_rights = fen_string.split(" ", 3)[2]
    match castling_rights:
        case "-":
            return "Neither side can castle"
        case "KQkq":
            return "White can castle both sides\n" \
                   "Black can castle both sides"
        case "KQk":
            return "White can castle both sides\n" \
                   "Black can castle kingside"           
        case "KQq":
            return "White can castle both sides\n" \
                   "Black can castle queenside"           
        case "Kkq":
            return "White can castle kingsides\n" \
                   "Black can castle both sides"         
        case "Qkq":
            return "White can castle queenside\n" \
            "Black can castle both sides"           
        case "KQ":
            return "White can castle both sides"
        case "kq":
            return "Black can castle both sides"
        case "Kk":
            return "White can castle kingside\n" \
                   "Black can castle kingside"          
        case "Qq":
            return "White can castle queenside\n" \
                   "Black can castle queenside"            
        case "Kq":
            return "White can castle kingside\n" \
                "Black can castle queenside"           
        case "Qk":
            return "White can castle queenside\n" \
                   "Black can castle kingside"           
        case "K":
            return "White can castle kingside"
        case "k":
            return "Black can castle kingside"       
        case "Q":
            return "White can castle queenside"
        case "q":
            return "Black can castle queenside"
        case _:
            raise ValueError("Invalid castling rights")


def white_pawn_moves(board: list) -> int:
    moves_frm_to = []
    for row in range(8):
        for col in range(8):
            if row > 0:
                if board[row][col] == "P":
                    if board[row-1][col] == ".":
                        moves_frm_to.append([(row, col), (row-1, col)])
                    if row > 0:
                        if row == 6 and board[row-2][col] == ".":
                            moves_frm_to.append([(row, col), (row-2, col)])
                    if row > 0 and col > 0 and board[row-1][col-1].islower():
                        moves_frm_to.append([(row, col), (row-1, col-1)])
                    if row > 0 and col > 7 and board[row-1][col+1].islower():
                        moves_frm_to.append([(row, col), (row-1, col+1)])

    return len(moves_frm_to)            


def black_pawn_moves(board: list) -> int:
    moves_frm_to = []
    for row in range(8):
        for col in range(8):
            if row < 7:
                if board[row][col] == "p":
                    if board[row+1][col] == ".":
                        moves_frm_to.append([(row, col), (row+1, col)])
                    if row < 7:
                        if row == 1 and board[row+2][col] == ".":
                            moves_frm_to.append([(row, col), (row+2, col)])
                    if row < 7 and col > 0 and board[row+1][col-1].islower():
                        moves_frm_to.append([(row, col), (row+1, col-1)])
                    if row < 7 and col > 7 and board[row+1][col+1].islower():
                        moves_frm_to.append([(row, col), (row+1, col+1)])
    return len(moves_frm_to)


def board_to_fen(board: list) -> str: # convert board array to a fen string
    fen_rows = []
    for row in board:
        empty_run = 0
        fen_row = ""
        for square in row:
            if square == ".":
                empty_run += 1
            else:
                if empty_run:
                    fen_row += str(empty_run)
                    empty_run = 0
                fen_row += square
        if empty_run:
            fen_row += str(empty_run)
        fen_rows.append(fen_row)
    return "/".join(fen_rows)

def generate_moves(board: list) -> list: # Return list of all possible moves
    raise NotImplementedError("This function is not implemented yet.")

def apply_move(board, move):
    raise NotImplementedError("This function is not implemented yet.")