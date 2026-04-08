class Game:
    def __init__(self, fen_string):
        self.board = generate_board(fen_string)
        self.full_move = fen_string.split(" ")[5]
        self.active_color : str = fen_string.split(" ")[1]
        self.en_passant : str = fen_string.split(" ")[3]  # Store en passant square
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

    def play(self, sq1, sq2, promotion_piece=None) -> None:
        pos1 = self.squares[sq1]
        pos2 = self.squares[sq2]
        piece = self.board[pos1[0]][pos1[1]]

        self.board[pos1[0]][pos1[1]] = "."
        
        # Handle en passant capture
        if piece in "Pp" and self.en_passant != "-":
            ep_pos = self.squares.get(self.en_passant)
            if ep_pos and (pos1[0], pos1[1]) != (ep_pos[0], ep_pos[1]):
                # Check if this is an en passant move
                if piece == "P" and pos2 == ep_pos:
                    # White captures black pawn en passant - remove black pawn at pos1's row
                    self.board[pos1[0]][pos2[1]] = "."
                elif piece == "p" and pos2 == ep_pos:
                    # Black captures white pawn en passant - remove white pawn at pos1's row
                    self.board[pos1[0]][pos2[1]] = "."
        
        # Handle pawn promotion
        if promotion_piece:
            self.board[pos2[0]][pos2[1]] = promotion_piece
        else:
            self.board[pos2[0]][pos2[1]] = piece

        # Update en passant square
        new_en_passant = "-"
        if piece in "Pp":
            # Check if pawn moved 2 squares
            if piece == "P" and pos1[0] == 6 and pos2[0] == 4:
                # White pawn moved 2 squares from rank 2 to rank 4
                # En passant square is rank 3 (row 5) at same column
                new_en_passant = self._pos_to_square((5, pos2[1]))
            elif piece == "p" and pos1[0] == 1 and pos2[0] == 3:
                # Black pawn moved 2 squares from rank 7 to rank 5
                # En passant square is rank 6 (row 2) at same column
                new_en_passant = self._pos_to_square((2, pos2[1]))
        
        self.en_passant = new_en_passant

        if self.active_color == "w":
            self.active_color = "b"
        elif self.active_color == "b":
            self.active_color = "w"
    
    def _pos_to_square(self, pos):
        """Convert board position (row, col) to algebraic notation (e.g., 'e4')"""
        row, col = pos
        files = "abcdefgh"
        ranks = "87654321"
        return files[col] + ranks[row]
    
    def validate_move(self, sq1, sq2, promotion_piece=None) -> bool:
        pos1 = self.squares[sq1] # (7,4)
        pos2 = self.squares[sq2] # (6,4)
        piece_to_move:str = self.board[pos1[0]][pos1[1]]

        if self.active_color == "w" and piece_to_move.islower():
            return False
        if self.active_color == "b" and piece_to_move.isupper():
            return False
        
        # Check if this is a pawn promotion move
        is_promotion = False
        if piece_to_move in "Pp":
            if (piece_to_move == "P" and pos2[0] == 0) or (piece_to_move == "p" and pos2[0] == 7):
                is_promotion = True
        
        valid = False  # Initialize valid
        
        match piece_to_move: #board[7][4]
            case "P":
                if is_promotion:
                    if promotion_piece and promotion_piece.upper() in "QRBN":
                        valid = [pos1, pos2, promotion_piece.upper()] in white_pawn_moves(self.board, self.en_passant, self.squares)
                    else:
                        return False  # Must specify promotion piece
                else:
                    # Check for regular moves or en passant
                    white_moves = white_pawn_moves(self.board, self.en_passant, self.squares)
                    valid = [pos1, pos2] in white_moves or [pos1, pos2, "EP"] in white_moves
            case "p":
                if is_promotion:
                    if promotion_piece and promotion_piece.lower() in "qrbn":
                        valid = [pos1, pos2, promotion_piece.lower()] in black_pawn_moves(self.board, self.en_passant, self.squares)
                    else:
                        return False  # Must specify promotion piece
                else:
                    # Check for regular moves or en passant
                    black_moves = black_pawn_moves(self.board, self.en_passant, self.squares)
                    valid = [pos1, pos2] in black_moves or [pos1, pos2, "EP"] in black_moves
            case "R":
                valid = [pos1, pos2] in white_rook_moves(self.board)
            case "r":
                valid = [pos1, pos2] in black_rook_moves(self.board)
            case "N":
                valid = [pos1, pos2] in white_knight_moves(self.board)
            case "n":
                valid = [pos1, pos2] in black_knight_moves(self.board)
            case "B":
                valid = [pos1, pos2] in white_bishop_moves(self.board)
            case "b":
                valid = [pos1, pos2] in black_bishop_moves(self.board)
            case "Q":
                valid = [pos1, pos2] in white_queen_moves(self.board)
            case "q":
                valid = [pos1, pos2] in black_queen_moves(self.board)
            case "K":
                valid = [pos1, pos2] in white_king_moves(self.board)
            case "k":
                valid = [pos1, pos2] in black_king_moves(self.board)

        if not valid:
            return False
        
        board_copy = [row[:] for row in self.board]
        board_copy[pos1[0]][pos1[1]] = "."
        
        # Check if this is an en passant capture
        is_en_passant = piece_to_move in "Pp" and self.en_passant != "-" and pos2 == self.squares.get(self.en_passant)
        
        if is_en_passant:
            # Remove the captured pawn (it's on the same rank as the capturing pawn)
            board_copy[pos1[0]][pos2[1]] = "."
        
        # For promotion, place the promoted piece instead of the pawn
        if is_promotion and promotion_piece:
            board_copy[pos2[0]][pos2[1]] = promotion_piece
        else:
            board_copy[pos2[0]][pos2[1]] = piece_to_move

        if is_check(board_copy, self.active_color):
            return False

        return True


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


def white_pawn_moves(board: list, en_passant: str = "-", squares_dict = None) -> list:
    moves_frm_to = []
    
    # Convert en_passant square to coordinates if available
    ep_pos = None
    if en_passant != "-" and squares_dict:
        ep_pos = squares_dict.get(en_passant)
    
    for row in range(8):
        for col in range(8):
            if row > 0:
                if board[row][col] == "P":
                    # Normal forward move
                    if board[row-1][col] == ".":
                        if row-1 == 0:  # Promotion rank
                            # Add promotion moves (Q, R, B, N)
                            moves_frm_to.append([(row, col), (row-1, col), "Q"])  # Queen promotion
                            moves_frm_to.append([(row, col), (row-1, col), "R"])  # Rook promotion
                            moves_frm_to.append([(row, col), (row-1, col), "B"])  # Bishop promotion
                            moves_frm_to.append([(row, col), (row-1, col), "N"])  # Knight promotion
                        else:
                            moves_frm_to.append([(row, col), (row-1, col)])
                    
                    # Double move from starting position
                    if row == 6 and board[row-2][col] == "." and board[row-1][col] == ".":
                        moves_frm_to.append([(row, col), (row-2, col)])
                    
                    # Captures
                    if row > 0 and col > 0 and board[row-1][col-1].islower():
                        if row-1 == 0:  # Promotion rank
                            moves_frm_to.append([(row, col), (row-1, col-1), "Q"])  # Queen promotion
                            moves_frm_to.append([(row, col), (row-1, col-1), "R"])  # Rook promotion
                            moves_frm_to.append([(row, col), (row-1, col-1), "B"])  # Bishop promotion
                            moves_frm_to.append([(row, col), (row-1, col-1), "N"])  # Knight promotion
                        else:
                            moves_frm_to.append([(row, col), (row-1, col-1)])
                    
                    if row > 0 and col < 7 and board[row-1][col+1].islower():
                        if row-1 == 0:  # Promotion rank
                            moves_frm_to.append([(row, col), (row-1, col+1), "Q"])  # Queen promotion
                            moves_frm_to.append([(row, col), (row-1, col+1), "R"])  # Rook promotion
                            moves_frm_to.append([(row, col), (row-1, col+1), "B"])  # Bishop promotion
                            moves_frm_to.append([(row, col), (row-1, col+1), "N"])  # Knight promotion
                        else:
                            moves_frm_to.append([(row, col), (row-1, col+1)])
                    
                    # En passant captures (white pawn on rank 5)
                    if ep_pos and row == 3:  # White pawn on rank 5 (board[3])
                        # Check left diagonal en passant
                        if col > 0 and (row-1, col-1) == ep_pos:
                            moves_frm_to.append([(row, col), (row-1, col-1), "EP"])
                        # Check right diagonal en passant
                        if col < 7 and (row-1, col+1) == ep_pos:
                            moves_frm_to.append([(row, col), (row-1, col+1), "EP"])
    
    return moves_frm_to


def black_pawn_moves(board: list, en_passant: str = "-", squares_dict = None) -> list:
    moves_frm_to = []
    
    # Convert en_passant square to coordinates if available
    ep_pos = None
    if en_passant != "-" and squares_dict:
        ep_pos = squares_dict.get(en_passant)
    
    for row in range(8):
        for col in range(8):
            if row < 7:
                if board[row][col] == "p":
                    # Normal forward move
                    if board[row+1][col] == ".":
                        if row+1 == 7:  # Promotion rank
                            # Add promotion moves (q, r, b, n)
                            moves_frm_to.append([(row, col), (row+1, col), "q"])  # Queen promotion
                            moves_frm_to.append([(row, col), (row+1, col), "r"])  # Rook promotion
                            moves_frm_to.append([(row, col), (row+1, col), "b"])  # Bishop promotion
                            moves_frm_to.append([(row, col), (row+1, col), "n"])  # Knight promotion
                        else:
                            moves_frm_to.append([(row, col), (row+1, col)])
                    
                    # Double move from starting position
                    if row == 1 and board[row+2][col] == "." and board[row+1][col] == ".":
                        moves_frm_to.append([(row, col), (row+2, col)])
                    
                    # Captures
                    if row < 7 and col > 0 and board[row+1][col-1].isupper():
                        if row+1 == 7:  # Promotion rank
                            moves_frm_to.append([(row, col), (row+1, col-1), "q"])  # Queen promotion
                            moves_frm_to.append([(row, col), (row+1, col-1), "r"])  # Rook promotion
                            moves_frm_to.append([(row, col), (row+1, col-1), "b"])  # Bishop promotion
                            moves_frm_to.append([(row, col), (row+1, col-1), "n"])  # Knight promotion
                        else:
                            moves_frm_to.append([(row, col), (row+1, col-1)])
                    
                    if row < 7 and col < 7 and board[row+1][col+1].isupper():
                        if row+1 == 7:  # Promotion rank
                            moves_frm_to.append([(row, col), (row+1, col+1), "q"])  # Queen promotion
                            moves_frm_to.append([(row, col), (row+1, col+1), "r"])  # Rook promotion
                            moves_frm_to.append([(row, col), (row+1, col+1), "b"])  # Bishop promotion
                            moves_frm_to.append([(row, col), (row+1, col+1), "n"])  # Knight promotion
                        else:
                            moves_frm_to.append([(row, col), (row+1, col+1)])
                    
                    # En passant captures (black pawn on rank 4)
                    if ep_pos and row == 4:  # Black pawn on rank 4 (board[4])
                        # Check left diagonal en passant
                        if col > 0 and (row+1, col-1) == ep_pos:
                            moves_frm_to.append([(row, col), (row+1, col-1), "EP"])
                        # Check right diagonal en passant
                        if col < 7 and (row+1, col+1) == ep_pos:
                            moves_frm_to.append([(row, col), (row+1, col+1), "EP"])
    
    return moves_frm_to


def white_rook_moves(board: list) -> int:
    moves = []
    directions = [
        (1, 0),   # down
        (-1, 0),  # up
        (0, 1),   # right
        (0, -1)   # left
    ]

    for row in range(8):
        for col in range(8):
            if board[row][col] == "R":
                for r, c in directions:
                    nr, nc = row + r, col + c
                    # keep sliding until off board
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        if board[nr][nc] in "RNBKQP": # Friendly block
                            break
                        elif board[nr][nc] in "rnbkqp": # Capture
                            moves.append([(row, col), (nr, nc)])
                            break
                        elif board[nr][nc] == ".": # Empty square
                            moves.append([(row, col), (nr, nc)])
                            nr += r
                            nc += c
    return moves


def black_rook_moves(board: list) -> int:
    moves = []
    directions = [
        (1, 0),   # down
        (-1, 0),  # up
        (0, 1),   # right
        (0, -1)   # left
    ]

    for row in range(8):
        for col in range(8):
            if board[row][col] == "r":
                for r, c in directions:
                    nr, nc = row + r, col + c
                    # keep sliding until off board
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        if board[nr][nc] in "rnbkqp": # Friendly block
                            break
                        elif board[nr][nc] in "RNBKQP": # Capture
                            moves.append([(row, col), (nr, nc)])
                            break
                        elif board[nr][nc] == ".": # Empty square
                            moves.append([(row, col), (nr, nc)])
                            nr += r
                            nc += c
    return moves


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
    return moves_frm_to


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
    return moves_frm_to


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
    return moves


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
    return moves


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
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),     # Rook-like
        (-1, -1), (-1, 1), (1, -1), (1, 1)    # Bishop-like
    ]

    # Find ALL white queens (not just the first)
    for r in range(8):
        for c in range(8):
            if board[r][c] == "Q":
                # Generate moves for THIS queen
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        target = board[nr][nc]
                        if target == ".":
                            moves.append([(r, c), (nr, nc)])
                        elif target.islower():  # Capture black
                            moves.append([(r, c), (nr, nc)])
                            break
                        else:  # Blocked by white
                            break
                        nr += dr
                        nc += dc

    return moves


def black_queen_moves(board: list) -> list:
    moves = []
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),     # Rook-like
        (-1, -1), (-1, 1), (1, -1), (1, 1)    # Bishop-like
    ]

    # Find ALL black queens (not just the first)
    for r in range(8):
        for c in range(8):
            if board[r][c] == "q":
                # Generate moves for THIS queen
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        target = board[nr][nc]
                        if target == ".":
                            moves.append([(r, c), (nr, nc)])
                        elif target.isupper():  # Capture white
                            moves.append([(r, c), (nr, nc)])
                            break
                        else:  # Blocked by black
                            break
                        nr += dr
                        nc += dc

    return moves


def find_king(board: list, active_color: str) -> tuple:
    king = 'K' if active_color == 'w' else 'k'
    for row in range(8):
        for col in range(8):
            if board[row][col] == king:
                return (row, col)


def get_all_opponent_moves(board: list, active_color: str) -> list:
    # Returns moves for the opposite color
    # color 'w' → get black moves
    # color 'b' → get white moves
    all_moves = []
    if active_color == 'w':
        # Collect all black piece moves
        all_moves.extend(black_pawn_moves(board))
        all_moves.extend(black_rook_moves(board))
        all_moves.extend(black_knight_moves(board))
        all_moves.extend(black_bishop_moves(board))
        all_moves.extend(black_queen_moves(board))
        all_moves.extend(black_king_moves(board))
    else:
        # Collect all white piece moves
        all_moves.extend(white_pawn_moves(board))
        all_moves.extend(white_rook_moves(board))
        all_moves.extend(white_knight_moves(board))
        all_moves.extend(white_bishop_moves(board))
        all_moves.extend(white_queen_moves(board))
        all_moves.extend(white_king_moves(board))

    return all_moves


def is_check(board: list, active_color: str) -> bool:
    king_pos = find_king(board, active_color)
    opponent_moves = get_all_opponent_moves(board, active_color)
    
    for move in opponent_moves:
        if move[1] == king_pos:  # move[1] is destination
            return True
    
    return False


def has_legal_move(board: list, active_color: str, en_passant: str = "-", squares_dict = None) -> bool:
    """Check if the active player has at least one legal move."""
    # Get all possible moves for the active player
    if active_color == 'w':
        all_moves = []
        all_moves.extend(white_pawn_moves(board, en_passant, squares_dict))
        all_moves.extend(white_rook_moves(board))
        all_moves.extend(white_knight_moves(board))
        all_moves.extend(white_bishop_moves(board))
        all_moves.extend(white_queen_moves(board))
        all_moves.extend(white_king_moves(board))
    else:
        all_moves = []
        all_moves.extend(black_pawn_moves(board, en_passant, squares_dict))
        all_moves.extend(black_rook_moves(board))
        all_moves.extend(black_knight_moves(board))
        all_moves.extend(black_bishop_moves(board))
        all_moves.extend(black_queen_moves(board))
        all_moves.extend(black_king_moves(board))
    
    # Test each move to see if it leaves the king in check
    for move in all_moves:
        pos1, pos2 = move[0], move[1]
        special_move = move[2] if len(move) > 2 else None
        piece = board[pos1[0]][pos1[1]]
        
        # Create a copy of the board and make the move
        board_copy = [row[:] for row in board]
        board_copy[pos1[0]][pos1[1]] = "."
        
        # Handle en passant capture
        if piece in "Pp" and special_move == "EP":
            # Remove the captured pawn
            board_copy[pos1[0]][pos2[1]] = "."
            board_copy[pos2[0]][pos2[1]] = piece
        # Handle promotion
        elif special_move and special_move not in "EP":
            board_copy[pos2[0]][pos2[1]] = special_move
        else:
            board_copy[pos2[0]][pos2[1]] = piece
        
        # Check if this move leaves us in check
        if not is_check(board_copy, active_color):
            return True  # Found a legal move
    
    return False  # No legal moves


def is_checkmate(board: list, active_color: str, en_passant: str = "-", squares_dict = None) -> bool:
    """Check if the active player is in checkmate."""
    return is_check(board, active_color) and not has_legal_move(board, active_color, en_passant, squares_dict)


def is_stalemate(board: list, active_color: str, en_passant: str = "-", squares_dict = None) -> bool:
    """Check if the game is in stalemate (not in check but no legal moves)."""
    return not is_check(board, active_color) and not has_legal_move(board, active_color, en_passant, squares_dict)


def generate_moves(board: list) -> list: # Return list of all possible moves
    raise NotImplementedError("This function is not implemented yet.")


def apply_move(board, move):
    raise NotImplementedError("This function is not implemented yet.")
