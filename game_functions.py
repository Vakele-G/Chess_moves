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


def white_rook_moves(board: list) -> int:
    moves_frm_to = []
    for row in range(8):
        c_row = row
        for col in range(8):
            c_col = col
            if board[row][col] == "R":
                while c_row > 0:
                    if board[c_row-1][c_col] == ".":
                        moves_frm_to.append([(c_row, c_col), (c_row-1, c_col)])
                        c_row -= 1
                    elif board[c_row-1][c_col] in "RNBQKP":
                        break
                    elif board[c_row-1][c_col] in "rnbqkp":
                        moves_frm_to.append([(c_row, c_col), (c_row-1, c_col)])
                        break
                c_row = row

                while row < 7:
                    if board[c_row-1][c_col] == ".":
                        moves_frm_to.append([(c_row, c_col), (c_row+1, c_col)])
                        c_row += 1
                    elif board[c_row+1][c_col] in "RNBQKP":
                        break
                    elif board[c_row+1][c_col] in "rnbqkp":
                        moves_frm_to.append([(c_row, c_col), (c_row+1, c_col)])
                        break
                c_row = row

                while col > 0:
                    if board[c_row][c_col-1] == ".":
                        moves_frm_to.append([(c_row, c_col), (c_row, c_col-1)])
                        c_col -= 1
                    elif board[c_row][c_col-1] in "RNBQKP":
                        break
                    elif board[c_row][c_col-1] in "rnbqkp":
                        moves_frm_to.append([(c_row, c_col), (c_row, c_col-1)])
                        break
                c_col = col

                while c_col < 7:
                    if board[c_row][c_col+1] == ".":
                        moves_frm_to.append([(c_row, c_col), (c_row, c_col+1)])
                        c_row += 1
                    elif board[c_row][c_col+1] in "RNBQKP":
                        break
                    elif board[c_row][c_col+1] in "rnbqkp":
                        moves_frm_to.append([(c_row, c_col), (c_row, c_col+1)])
                        break
                c_col = col
    return len(moves_frm_to)


def black_rook_moves(board: list) -> int:
    moves_frm_to = []
    for row in range(8):
        c_row = row
        for col in range(8):
            c_col = col
            if board[row][col] == "r":
                while c_row > 0:
                    if board[c_row-1][c_col] == ".":
                        moves_frm_to.append([(c_row, c_col), (c_row-1, c_col)])
                        c_row -= 1
                    elif board[c_row-1][c_col] in "rnbqkp":
                        break
                    elif board[c_row-1][c_col] in "RNBQKP":
                        moves_frm_to.append([(c_row, c_col), (c_row-1, c_col)])
                        break
                c_row = row

                while row < 7:
                    if board[c_row-1][c_col] == ".":
                        moves_frm_to.append([(c_row, c_col), (c_row+1, c_col)])
                        c_row += 1
                    elif board[c_row+1][c_col] in "rnbqkp":
                        break
                    elif board[c_row+1][c_col] in "RNBQKP":
                        moves_frm_to.append([(c_row, c_col), (c_row+1, c_col)])
                        break
                c_row = row

                while col > 0:
                    if board[c_row][c_col-1] == ".":
                        moves_frm_to.append([(c_row, c_col), (c_row, c_col-1)])
                        c_col -= 1
                    elif board[c_row][c_col-1] in "rnbqkp":
                        break
                    elif board[c_row][c_col-1] in "RNBQKP":
                        moves_frm_to.append([(c_row, c_col), (c_row, c_col-1)])
                        break
                c_col = col

                while c_col < 7:
                    if board[c_row][c_col+1] == ".":
                        moves_frm_to.append([(c_row, c_col), (c_row, c_col+1)])
                        c_row += 1
                    elif board[c_row][c_col+1] in "rnbqkp":
                        break
                    elif board[c_row][c_col+1] in "RNBQKP":
                        moves_frm_to.append([(c_row, c_col), (c_row, c_col+1)])
                        break
                c_col = col
    return len(moves_frm_to)


def white_knight_moves(board: list) -> int:
    moves_frm_to = []
    offsets =  [(2, 1), (2, -1),
                (-2, 1), (-2, -1),
                (1, 2), (1, -2),
                (-1, 2), (-1, -2)]
    
    for row in range(8):
        for col in range(8):
            if board[row][col] == "N":
                for r, c in offsets:
                    nr, nc = row + r, col + c
                    if nr < 8 and nr >= 0 and nc < 8 and nc >=0:
                        if board[nr][nc] in "RNBQKP":
                            pass
                        else:
                            moves_frm_to.append([(row, col), (nr, nc)])
    return len(moves_frm_to)


def black_knight_moves(board: list) -> int:
    moves_frm_to = []
    offsets =  [(2, 1), (2, -1),
                (-2, 1), (-2, -1),
                (1, 2), (1, -2),
                (-1, 2), (-1, -2)]
    
    for row in range(8):
        for col in range(8):
            if board[row][col] == "n":
                for r, c in offsets:
                    nr, nc = row + r, col + c
                    if nr < 8 and nr >= 0 and nc < 8 and nc >=0:
                        if board[nr][nc] in "rnbqkp":
                            pass
                        else:
                            moves_frm_to.append([(row, col), (nr, nc)])
    return len(moves_frm_to)


def white_bishop_moves(board: list) -> int:
    moves = []
    directions = [
        (1, 1),   # down-right
        (1, -1),  # down-left
        (-1, 1),  # up-right
        (-1, -1)  # up-left
    ]

    for row in range(8):
        for col in range(8):
            if board[row][col] == "B":
                for r, c in directions:
                    nr, nc = row + r, col + c
                    # keep sliding until off board
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        if board[nr][nc] in "RNBKQP":
                            break
                        elif board[nr][nc] in "rnbkqp":
                            moves.append([(row, col), (nr, nc)])
                            break
                        elif board[nr][nc] == ".":
                            moves.append([(row, col), (nr, nc)])
                            nr += r
                            nc += c
    return len(moves)


def black_bishop_moves(board: list) -> int:
    moves = []
    directions = [
        (1, 1),   # down-right
        (1, -1),  # down-left
        (-1, 1),  # up-right
        (-1, -1)  # up-left
    ]

    for row in range(8):
        for col in range(8):
            if board[row][col] == "b":
                for r, c in directions:
                    nr, nc = row + r, col + c
                    # keep sliding until off board
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        if board[nr][nc] in "rnbkqp":
                            break
                        elif board[nr][nc] in "RNBKQP":
                            moves.append([(row, col), (nr, nc)])
                            break
                        elif board[nr][nc] == ".":
                            moves.append([(row, col), (nr, nc)])
                            nr += r
                            nc += c
    return len(moves)

def generate_moves(board: list) -> list: # Return list of all possible moves
    raise NotImplementedError("This function is not implemented yet.")


def apply_move(board, move):
    raise NotImplementedError("This function is not implemented yet.")

