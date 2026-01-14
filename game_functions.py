class Game:
    def __init__(self, fen_string):
        self.board = generate_board(fen_string)
        self.full_move = fen_string.split(" ")[5]
        self.to_move = fen_string.split(" ")[1]
        self.squares = {"a1": (7,0),
                        "a2":(6,0),
                        "a3":(5,0),
                        "a4":(4,0),
                        "a5":(3,0),
                        "a6":(2,0),
                        "a7":(1,0),
                        "a8":(0,0),
                        "b1": (7,1),
                        "b2":(6,1),
                        "b3":(5,1),
                        "b4":(4,1),
                        "b5":(3,1),
                        "b6":(2,1),
                        "b7":(1,1),
                        "b8":(0,1),
                        "c1": (7,2),
                        "c2":(6,2),
                        "c3":(5,2),
                        "c4":(4,2),
                        "c5":(3,2),
                        "c6":(2,2),
                        "c7":(1,2),
                        "c8":(0,2),
                        "d1": (7,3),
                        "d2":(6,3),
                        "d3":(5,3),
                        "d4":(4,3),
                        "d5":(3,3),
                        "d6":(2,3),
                        "d7":(1,3),
                        "d8":(0,3),
                        "e1": (7,4),
                        "e2":(6,4),
                        "e3":(5,4),
                        "e4":(4,4),
                        "e5":(3,4),
                        "e6":(2,4),
                        "e7":(1,4),
                        "e8":(0,4),
                        "f1": (7,5),
                        "f2":(6,5),
                        "f3":(5,5),
                        "f4":(4,5),
                        "f5":(3,5),
                        "f6":(2,5),
                        "f7":(1,5),
                        "f8":(0,5),
                        "g1": (7,6),
                        "g2":(6,6),
                        "g3":(5,6),
                        "g4":(4,6),
                        "g5":(3,6),
                        "g6":(2,6),
                        "g7":(1,6),
                        "g8":(0,6),
                        "h1": (7,7),
                        "h2":(6,7),
                        "h3":(5,7),
                        "h4":(4,7),
                        "h5":(3,7),
                        "h6":(2,7),
                        "h7":(1,7),
                        "h8":(0,7)}

    def play(self, sq1, sq2) -> None:
        pos1 = self.squares[sq1]
        pos2 = self.squares[sq2]
        piece = self.board[pos1[0]][pos1[1]]

        self.board[pos1[0]][pos1[1]] = "."
        self.board[pos2[0]][pos2[1]] = piece
    
    def validate_move(self, sq1, sq2) -> bool:
        pos1 = self.squares[sq1]
        pos2 = self.squares[sq2]

        match self.board[pos1[0]][pos2[1]]:
            case "P":
                return True if [pos1, pos2] in white_pawn_moves(self.board) else False
            case "p":
                return True if [pos1, pos2] in black_pawn_moves(self.board) else False
            case "R":
                return True if [pos1, pos2] in white_rook_moves(self.board) else False
            case "r":
                return True if [pos1, pos2] in black_rook_moves(self.board) else False
            case "N":
                return True if [pos1, pos2] in white_knight_moves(self.board) else False
            case "n":
                return True if [pos1, pos2] in black_knight_moves(self.board) else False
            case "B":
                return True if [pos1, pos2] in white_bishop_moves(self.board) else False
            case "b":
                return True if [pos1, pos2] in black_bishop_moves(self.board) else False
            case "Q":
                return True if [pos1, pos2] in white_queen_moves(self.board) else False
            case "q":
                return True if [pos1, pos2] in black_queen_moves(self.board) else False
            case "K":
                return True if [pos1, pos2] in white_king_moves(self.board) else False
            case "k":
                return True if [pos1, pos2] in black_king_moves(self.board) else False

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


def white_pawn_moves(board: list) -> list:
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
    return moves_frm_to


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


def white_king_moves(board: list) -> list:
    moves = []

    # All 8 possible king directions
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1)
    ]

    # Find the white king
    king_pos = None
    for r in range(8):
        for c in range(8):
            if board[r][c] == "K":
                king_pos = (r, c)
                break
        if king_pos:
            break

    if king_pos is None:
        return moves

    kr, kc = king_pos

    # Generate legal moves
    for dr, dc in directions:
        nr, nc = kr + dr, kc + dc

        # Check board bounds
        if 0 <= nr < 8 and 0 <= nc < 8:
            target = board[nr][nc]

            # Empty square or capture black piece
            if target not in "RNBQKP":
                moves.append([(kr, kc), (nr, nc)])

    return moves


def black_king_moves(board: list) -> list:
    moves = []

    # All 8 possible king directions
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1)
    ]

    # Find the white king
    king_pos = None
    for r in range(8):
        for c in range(8):
            if board[r][c] == "k":
                king_pos = (r, c)
                break
        if king_pos:
            break

    if king_pos is None:
        return moves

    kr, kc = king_pos

    # Generate legal moves
    for dr, dc in directions:
        nr, nc = kr + dr, kc + dc

        # Check board bounds
        if 0 <= nr < 8 and 0 <= nc < 8:
            target = board[nr][nc]

            # Empty square or capture black piece
            if target not in "rnbqkp":
                moves.append([(kr, kc), (nr, nc)])

    return moves
                

def white_queen_moves(board: list) -> list:
    moves = []

    # 8 directions: rook + bishop combined
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),     # Rook-like
        (-1, -1), (-1, 1), (1, -1), (1, 1)    # Bishop-like
    ]

    # Find the white queen
    queen_pos = None
    for r in range(8):
        for c in range(8):
            if board[r][c] == "Q":
                queen_pos = (r, c)
                break
        if queen_pos:
            break

    if queen_pos is None:
        return moves

    qr, qc = queen_pos

    # Explore each direction
    for dr, dc in directions:
        nr, nc = qr + dr, qc + dc

        while 0 <= nr < 8 and 0 <= nc < 8:
            target = board[nr][nc]

            if target == ".":
                moves.append([(qr, qc), (nr, nc)])
            elif target.islower():  # Capture black piece
                moves.append([(qr, qc), (nr, nc)])
                break
            else:  # Blocked by white piece
                break

            nr += dr
            nc += dc

    return moves


def black_queen_moves(board: list) -> list:
    moves = []

    # 8 directions: rook + bishop combined
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),     # Rook-like
        (-1, -1), (-1, 1), (1, -1), (1, 1)    # Bishop-like
    ]

    # Find the white queen
    queen_pos = None
    for r in range(8):
        for c in range(8):
            if board[r][c] == "q":
                queen_pos = (r, c)
                break
        if queen_pos:
            break

    if queen_pos is None:
        return moves

    qr, qc = queen_pos

    # Explore each direction
    for dr, dc in directions:
        nr, nc = qr + dr, qc + dc

        while 0 <= nr < 8 and 0 <= nc < 8:
            target = board[nr][nc]

            if target == ".":
                moves.append([(qr, qc), (nr, nc)])
            elif target.isupper():  # Capture white piece
                moves.append([(qr, qc), (nr, nc)])
                break
            else:  # Blocked by black piece
                break

            nr += dr
            nc += dc

    return moves


def generate_moves(board: list) -> list: # Return list of all possible moves
    raise NotImplementedError("This function is not implemented yet.")


def apply_move(board, move):
    raise NotImplementedError("This function is not implemented yet.")

# King queen moves function do not work properly
# validate method might be broke as well