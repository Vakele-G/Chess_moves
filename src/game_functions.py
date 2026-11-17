import re

class Game:

    def __init__(self, fen_string :str):
        state = parse_fen(fen_string)

        self.board = state["board"]
        self.half_move = state["half_move"]
        self.full_move = state["full_move"]
        self.active_color : str = state["active_color"]
        self.en_passant : str = state["en_passant"]  # Store en passant square
        self.castling : str = state["castling"]
        self.squares = SQUARES

    def play(self, sq1 :str, sq2 :str, promotion_piece :str|None = None) -> None:
        """Play a validated move and update all game state.

        Raises:
            ValueError: if the move is illegal or malformed.
        """
        if not self.validate_move(sq1, sq2, promotion_piece):
            raise ValueError(f"Illegal move: {sq1} {sq2}")

        start = self.squares[sq1]
        end = self.squares[sq2]
        piece = self.board[start[0]][start[1]]
        captured = self.board[end[0]][end[1]]

        reaches_last_rank = (
            (piece == "P" and end[0] == 0) or (piece == "p" and end[0] == 7)
            )

        is_castling = piece in "Kk" and abs(end[1] - start[1]) == 2
        is_en_passant = (
            piece in "Pp"
            and self.en_passant != "-"
            and end == self.squares[self.en_passant]
            and captured == "."
        )

        # Defensive check: an en passant target must really have a pawn.
        if is_en_passant:
            adjacent = (start[0], end[1])
            expected_pawn = "p" if piece == "P" else "P"
            if self.board[adjacent[0]][adjacent[1]] != expected_pawn:
                raise ValueError("No pawn available for en passant capture")

        # Build the move descriptor understood by apply_move_to_board().
        if is_castling:
            flag = "O-O" if end[1] > start[1] else "O-O-O"
            move = [start, end, flag]
        elif is_en_passant:
            move = [start, end, "EP"]
        elif reaches_last_rank:
            promoted = (
                promotion_piece.upper()
                if piece == "P"
                else promotion_piece.lower()
            )
            move = [start, end, promoted]
        else:
            move = [start, end]

        self.board = apply_move_to_board(self.board, move)

        self._update_castling_rights(piece, start, end, captured)

        # En passant is only available immediately after a two-square push.
        self.en_passant = "-"
        if piece in "Pp" and abs(end[0] - start[0]) == 2:
            middle = ((start[0] + end[0]) // 2, start[1])
            self.en_passant = square_name(middle)

        # The half-move clock resets on a pawn move or a capture.
        if piece in "Pp" or captured != "." or is_en_passant:
            self.half_move = 0
        else:
            self.half_move += 1

        # The full-move number increases after Black's move.
        if self.active_color == "b":
            self.full_move += 1

        self.active_color = opponent(self.active_color)
    
    def _pos_to_square(self, pos):
        """Convert board position (row, col) to algebraic notation (e.g., 'e4')"""
        row, col = pos
        files = "abcdefgh"
        ranks = "87654321"
        return files[col] + ranks[row]
    
    def validate_move(self, sq1 :str, sq2 :str, promotion_piece :str|None = None) -> bool:
        """Return True if the move is legal for the side to move.
         
        It rejects:
        - unknown squares, empty start squares, same-square moves
        - moving the opponent's piece
        - illegal piece movement
        - moves that leave your own king in check
        - missing promotion piece, or a promotion piece on an ordinary move
        """

        if sq1 not in self.squares or sq2 not in self.squares:
            return False
        if sq1 == sq2:
            return False

        start = self.squares[sq1]
        end = self.squares[sq2]
        piece = self.board[start[0]][start[1]]

        if piece == "." or piece_color(piece) != self.active_color:
            return False

        reaches_last_rank = (
            (piece == "P" and end[0] == 0) or (piece == "p" and end[0] == 7)
        )

        if reaches_last_rank:
            if not promotion_piece or promotion_piece.upper() not in ("Q","R","B","N"):
                return False
            promotion_piece = (promotion_piece.upper() if piece == "P" else promotion_piece.lower())
        elif promotion_piece:
            # A promotion piece is meaningless on a non-promotion move.
            return False

        if piece in "Pp":
            moves = (
                white_pawn_moves(self.board, self.en_passant, self.squares)
                if piece == "P"
                else black_pawn_moves(self.board, self.en_passant, self.squares)
            )
        elif piece in "Kk":
            moves = (
                white_king_moves(self.board, self.castling)
                if piece == "K"
                else black_king_moves(self.board, self.castling)
            )
        else:
            moves = PIECE_MOVE_FUNCTIONS[piece](self.board)

        matching = [m for m in moves if m[0] == start and m[1] == end]
        if not matching:
            return False

        # For promotions, the exact chosen piece must be generated.
        if reaches_last_rank and [start, end, promotion_piece] not in matching:
            return False

        move = [start, end, promotion_piece] if reaches_last_rank else matching[0]
        board_copy = apply_move_to_board(self.board, move)
        return not is_check(board_copy, self.active_color)

    def _update_castling_rights(self, piece :str, start :tuple[int, int], end :tuple[int, int], captured :str) -> None:
        """Remove castling rights after a king/rook moves or rook capture."""
        rights = set() if self.castling == "-" else set(self.castling)

        # Moving the king loses both rights for that colour.
        if piece == "K":
            rights -= {"K", "Q"}
        elif piece == "k":
            rights -= {"k", "q"}

        # A rook that leaves its home square loses that side's right.
        if piece == "R":
            if start == (7, 7):
                rights.discard("K")
            elif start == (7, 0):
                rights.discard("Q")
        elif piece == "r":
            if start == (0, 7):
                rights.discard("k")
            elif start == (0, 0):
                rights.discard("q")

        # A rook captured on its home square loses that side's right.
        if captured == "R":
            if end == (7, 7):
                rights.discard("K")
            elif end == (7, 0):
                rights.discard("Q")
        elif captured == "r":
            if end == (0, 7):
                rights.discard("k")
            elif end == (0, 0):
                rights.discard("q")

        self.castling = "".join(c for c in "KQkq" if c in rights) or "-"

    def status(self) -> str | None:
        """Return 'check', checkmate', 'stalemate', 'fifth_move', 'insufficient_material' or None."""
        in_check = is_check(self.board, self.active_color)
        if not has_legal_move(self.board, self.active_color, self.en_passant, self.squares, self.castling):
            return "checkmate" if in_check else "stalemate"

        if self.half_move >= 100:
            return "fifty_move"
        if has_insufficient_material(self.board):
            return "insufficient_material"
        
        return "check" if in_check else None

    def to_fen(self) -> str:
        """Return the complete current position as a FEN string."""

        return " ".join(
            [
                board_to_fen(self.board),
                self.active_color,
                self.castling,
                self.en_passant,
                str(self.half_move),
                str(self.full_move),
            ]
        )
    

KNIGHT_OFFSETS = (
        (2, 1), (2, -1),
        (-2, 1), (-2, -1),
        (1, 2), (1, -2),
        (-1, 2), (-1, -2)
    )

BiSHOP_DIRECTIONS = (
        (1, 1),   # down-right
        (1, -1),  # down-left
        (-1, 1),  # up-right
        (-1, -1)  # up-left
    )

ROOK_DIRECTIONS = (
        (1, 0),   # down
        (-1, 0),  # up
        (0, 1),   # right
        (0, -1)   # left
    )

KING_DIRECTIONS = (
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    )


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


def king_moves(board :list, color :str, castling_rights :str = "-") -> list:
    """Return king moves for `color`, including legal castling moves."""
    start = find_king(board, color)

    if start is None:
        return []

    moves = []
    king_row, king_col = start

    for direction_row, direction_col in KING_DIRECTIONS:
        new_row, new_col = king_row + direction_row, king_col + direction_col

        if not in_bounds(new_row, new_col):
            continue
        target = board[new_row][new_col]

        # Empty square or enemy piece. (Friendly pieces block)
        if target == "." or piece_color(target) != color:
            moves.append([(king_row, king_col), (new_row, new_col)])

    moves.extend(_castling_moves(board, color, castling_rights))
    return moves


def white_king_moves(board: list, castling_rights :str = "-") -> list:
   return king_moves(board, "w", castling_rights)


def black_king_moves(board: list, castling_rights :str = "-") -> list:
    return king_moves(board, "b", castling_rights)
                

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


def _castling_moves(board :list, color :str, castling_rights :str) -> list:
    """Return all fully legal castling moves for `color`.

    Each move is [king_start, king_end, flag]:
        [..., "O-O"]   kingside
        [..., "O-O-O"] queenside

    Checks:
        - the FEN still grants the right;
        - the king and rook are on their home squares;
        - every square between them is empty;
        - the king is not in check;
        - the king does not cross or land on an attacked square.
    """
    if not castling_rights or castling_rights == "-":
        return []

    row = 7 if color == "w" else 0
    king = "K" if color == "w" else "k"
    rook = "R" if color == "w" else "r"
    enemy = opponent(color)
    rights = set(castling_rights)
    moves = []

    # The king must still be on e1/e8 and must not be in check.
    if board[row][4] != king:
        return moves

    if is_square_attacked(board, (row, 4), enemy):
        return moves

    # Kingside: f and g must be empty.
    kingside_right = "K" if color == "w" else "k"
    if kingside_right in rights:
        if (
            board[row][5] == "."
            and board[row][6] == "."
            and board[row][7] == rook
        ):
            if not any(
                is_square_attacked(board, (row, col), enemy)
                for col in (4, 5, 6)
            ):
                moves.append([(row, 4), (row, 6), "O-O"])

    # Queenside: b, c and d must be empty. The b-square may be attacked;
    # the king only crosses e1-d1-c1.
    queenside_right = "Q" if color == "w" else "q"
    if queenside_right in rights:
        if (
            board[row][1] == "."
            and board[row][2] == "."
            and board[row][3] == "."
            and board[row][0] == rook
        ):
            if not any(
                is_square_attacked(board, (row, col), enemy)
                for col in (4, 3, 2)
            ):
                moves.append([(row, 4), (row, 2), "O-O-O"])

    return moves


def get_all_moves(board: list,color: str,en_passant: str = "-",squares_dict: dict | None = None, castling_rights: str = "-") -> list:
    """Return all pseudo-legal moves for `color`.
    Pseudo-legal means the piece movement is correct, but the move may leave the moving side's own king in check.
    """
    if color == "w":
        moves = []
        moves.extend(white_pawn_moves(board, en_passant, squares_dict))
        moves.extend(white_rook_moves(board))
        moves.extend(white_knight_moves(board))
        moves.extend(white_bishop_moves(board))
        moves.extend(white_queen_moves(board))
        moves.extend(white_king_moves(board, castling_rights))
        return moves

    moves = []
    moves.extend(black_pawn_moves(board, en_passant, squares_dict))
    moves.extend(black_rook_moves(board))
    moves.extend(black_knight_moves(board))
    moves.extend(black_bishop_moves(board))
    moves.extend(black_queen_moves(board))
    moves.extend(black_king_moves(board, castling_rights))
    return moves


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


def is_check(board :list, active_color :str) -> bool:
    king_pos = find_king(board, active_color)

    if king_pos is None:
        return False
    
    return is_square_attacked(board, king_pos, opponent(active_color))


def has_legal_move(board: list, active_color: str, en_passant: str = "-", squares_dict: dict|None = None, castling_rights: str = "-") -> bool:
    """Return True if active side has at least one legal move."""
    for move in get_all_moves(board, active_color, en_passant, squares_dict, castling_rights):
        board_copy = apply_move_to_board(board, move)

        if not is_check(board_copy, active_color):
            return True

    return False


def is_checkmate(board :list, active_color :str, en_passant :str = "-", squares_dict :dict|None = None, castling_rights: str = "-") -> bool:
    """Check if the active player is in checkmate."""
    return is_check(board, active_color) and not has_legal_move(board, active_color, en_passant, squares_dict, castling_rights)


def is_stalemate(board: list, active_color: str, en_passant: str = "-", squares_dict :dict|None = None, castling_rights: str = "-") -> bool:
    """Check if the game is in stalemate (not in check but no legal move exits)."""
    return not is_check(board, active_color) and not has_legal_move(board, active_color, en_passant, squares_dict, castling_rights)


def has_insufficient_material(board :list) -> bool:
    """True when neither side can possibly deliver checkmate.

    Covers: K v K, K+B v K, K+N v K, and positions where the only
    other pieces are bishops that all stand on the same colour of square.
    (Two knights can still mate with cooperation, so that is NOT counted.)
    """
    minors = []
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece in (".", "K", "k"):
                continue
            if piece.lower() in "nb":
                minors.append((piece.lower(), (r + c) % 2))
            else:
                return False  # a pawn, rook or queen can always force mate

    if len(minors) <= 1:
        return True
    return all(p == "b" for p, _ in minors) and len({shade for _, shade in minors}) == 1


def apply_move_to_board(board :list, move :list) -> list:
    """Return a copy of `board` after applying a move.

    A move is [from_pos, to_pos] with an optional third item:
        "EP"          -> en passant capture
        "O-O"         -> king-side castling
        "O-O-O"       -> queen-side castling
        "Q"/"R"/"B"/"N" (or lowercase) -> promotion piece

    This helper does NOT update castling rights, en passant target,
    move counters or the active colour. Game.play() owns that state.
    """
    result = [row[:] for row in board]

    start, end = move[0], move[1]
    special = move[2] if len(move) > 2 else None
    piece = result[start[0]][start[1]]

    # Remove the moving piece first.
    result[start[0]][start[1]] = "."

    if special == "EP":
        # The captured pawn is beside the destination, not on it.
        result[start[0]][end[1]] = "."

    elif special in ("O-O", "O-O-O"):
        # Castling: move the rook to its new square too.
        row = start[0]
        if special == "O-O":
            rook_from, rook_to = (row, 7), (row, 5)
        else:
            rook_from, rook_to = (row, 0), (row, 3)

        result[rook_to[0]][rook_to[1]] = result[rook_from[0]][rook_from[1]]
        result[rook_from[0]][rook_from[1]] = "."

    # Promotion replaces the pawn; otherwise place the original piece.
    if special and special not in ("EP", "O-O", "O-O-O"):
        result[end[0]][end[1]] = special
    else:
        result[end[0]][end[1]] = piece

    return result


def generate_moves(board: list) -> list: # Return list of all possible moves
    raise NotImplementedError("This function is not implemented yet.")


def apply_move(board, move):
    raise NotImplementedError("This function is not implemented yet.")




# ------HELPER FUNCTIONS------

def in_bounds(row :int, col :int) -> bool:
    """Return True when (row, col) is on the 8x8 board."""
    return 0 <= row < 8 and 0 <= col < 8

def square_name(position :tuple[int, int]) -> str:
    """
    Convert (row, col) to algebraic notation,
    e.g. (7, 4) -> 'e1'.
    """
    row, col = position
    return "abcdefgh"[col] + "87654321"[row]

def piece_color(piece :str) -> str | None:
    """Return 'w', 'b', or None for an empty square."""
    if piece == ".":
        return None
    return "w" if piece.isupper() else "b"

def opponent(color: str) -> str:
    """Return the opposite colour."""
    return "b" if color == "w" else "w"

def find_king(board :list, active_color :str) -> tuple | None:
    king = 'K' if active_color == 'w' else 'k'
    for row in range(8):
        for col in range(8):
            if board[row][col] == king:
                return (row, col)

def is_square_attacked(board :list, pos :tuple[int, int], by_color :str) -> bool:
    """Return True if any piece of `by_color` attacks `pos`.

    Pinned pieces still count as attacking. This matches the FIDE rule
    """
    row, col = pos

    # Pawn attacks.
    # A white pawn attacks upward, so it must be one row below the target.
    # A black pawn is one row above.
    pawn = "P" if by_color == "w" else "p"
    pawn_row = row + 1 if by_color == "w" else row - 1

    for dc in (-1, 1):
        pc = col + dc
        if in_bounds(pawn_row, pc) and board[pawn_row][pc] == pawn:
            return True

    # Knight attacks.
    knight = "N" if by_color == "w" else "n"
    for dr, dc in KNIGHT_OFFSETS:
        r, c = row + dr, col + dc
        if in_bounds(r, c) and board[r][c] == knight:
            return True

    # King attacks.
    king = "K" if by_color == "w" else "k"
    for dr, dc in KING_DIRECTIONS:
        r, c = row + dr, col + dc
        if in_bounds(r, c) and board[r][c] == king:
            return True

    # Rook and queen attacks.
    rook = "R" if by_color == "w" else "r"
    queen = "Q" if by_color == "w" else "q"

    for dr, dc in ROOK_DIRECTIONS:
        r, c = row + dr, col + dc

        while in_bounds(r, c):
            piece = board[r][c]

            if piece != ".":
                if piece == rook or piece == queen:
                    return True
                break

            r += dr
            c += dc

    # Bishop and queen attacks.
    bishop = "B" if by_color == "w" else "b"

    for dr, dc in BiSHOP_DIRECTIONS:
        r, c = row + dr, col + dc

        while in_bounds(r, c):
            piece = board[r][c]

            if piece != ".":
                if piece == bishop or piece == queen:
                    return True
                break

            r += dr
            c += dc

    return False


PIECE_MOVE_FUNCTIONS = {
        "R": white_rook_moves,
        "r": black_rook_moves,
        "N": white_knight_moves,
        "n": black_knight_moves,
        "B": white_bishop_moves,
        "b": black_bishop_moves,
        "Q": white_queen_moves,
        "q": black_queen_moves,
        }


def parse_fen(fen_string: str) -> dict:
    """Parse and validate a complete FEN string.

    Returns a dict with:
        board, active_color, castling, en_passant, half_move, full_move

    Raises:
        ValueError: for any malformed field, with a human-readable message.
    """
    fields = fen_string.strip().split()
    if len(fields) != 6:
        raise ValueError(
            "FEN must have 6 fields: placement, turn, castling, "
            "en passant, half-move, full-move"
        )

    placement, active_color, castling, en_passant, half_move, full_move = fields

    # --- Piece placement -------------------------------------------------
    ranks = placement.split("/")
    if len(ranks) != 8:
        raise ValueError("FEN placement must contain exactly 8 ranks")

    board = []
    for rank_index, rank in enumerate(ranks):
        row = []
        previous_was_digit = False

        for char in rank:
            if char.isdigit():
                if previous_was_digit:
                    raise ValueError(
                        f"Rank {8 - rank_index} has adjacent digits: {rank!r}"
                    )

                count = int(char)
                if not 1 <= count <= 8:
                    raise ValueError(
                        f"Invalid empty-square count {char!r} "
                        f"in rank {rank!r}"
                    )

                row.extend(["."] * count)
                previous_was_digit = True

            elif char in PIECE_CHARS:
                row.append(char)
                previous_was_digit = False

            else:
                raise ValueError(
                    f"Invalid character {char!r} in rank {rank!r}"
                )

        if len(row) != 8:
            raise ValueError(
                f"Rank {8 - rank_index} describes {len(row)} squares, "
                f"expected 8: {rank!r}"
            )

        board.append(row)

    # --- Side to move ----------------------------------------------------
    if active_color not in ("w", "b"):
        raise ValueError("Side to move must be 'w' or 'b'")

    # --- Castling rights -------------------------------------------------
    if castling != "-" and (
        not castling or not CASTLING_RE.fullmatch(castling)
    ):
        raise ValueError(
            "Castling field must be '-' or a subset of 'KQkq' in that order"
        )

    # --- En passant target ----------------------------------------------
    if en_passant != "-" and not EN_PASSANT_RE.fullmatch(en_passant):
        raise ValueError(
            "En passant square must be '-' or a square on rank 3 or 6"
        )

    # --- Move counters ---------------------------------------------------
    try:
        half_move_int = int(half_move)
        full_move_int = int(full_move)
    except ValueError as exc:
        raise ValueError(
            "Half-move and full-move counters must be integers"
        ) from exc

    if half_move_int < 0:
        raise ValueError("Half-move clock cannot be negative")
    if full_move_int < 1:
        raise ValueError("Full-move number must be at least 1")

    # --- Exactly one king per side --------------------------------------
    flat = "".join("".join(row) for row in board)
    if flat.count("K") != 1 or flat.count("k") != 1:
        raise ValueError(
            "FEN must contain exactly one white king and one black king"
        )

    # --- Pawns can't stand on the first or last rank ---------------------
    if any(c in "Pp" for c in board[0] + board[7]):
        raise ValueError("Pawns cannot be on the first or eighth rank")

    # --- Sane piece counts ----------------------------------------------
    for pawn, side in (("P", "White"), ("p", "Black")):
        if flat.count(pawn) > 8:
            raise ValueError(f"{side} has more than 8 pawns")
    if sum(ch.isupper() for ch in flat) > 16 or sum(ch.islower() for ch in flat) > 16:
        raise ValueError("A side cannot have more than 16 pieces")

    # --- Castling rights must match king/rook placement ------------------
    for right, king_pos, king, rook_pos, rook in (
        ("K", (7, 4), "K", (7, 7), "R"),
        ("Q", (7, 4), "K", (7, 0), "R"),
        ("k", (0, 4), "k", (0, 7), "r"),
        ("q", (0, 4), "k", (0, 0), "r"),
    ):
        if right in castling and (
            board[king_pos[0]][king_pos[1]] != king
            or board[rook_pos[0]][rook_pos[1]] != rook
        ):
            raise ValueError(f"Castling right '{right}' doesn't match the piece placement")

    # --- En passant target must be consistent with the position ----------
    if en_passant != "-":
        col = "abcdefgh".index(en_passant[0])
        if active_color == "w":
            # Black just pushed: target on rank 6, black pawn on rank 5, rank 7 empty.
            if en_passant[1] != "6":
                raise ValueError("With White to move, the en passant square must be on rank 6")
            target_row, pawn_row, origin_row, pawn = 2, 3, 1, "p"
        else:
            if en_passant[1] != "3":
                raise ValueError("With Black to move, the en passant square must be on rank 3")
            target_row, pawn_row, origin_row, pawn = 5, 4, 6, "P"

        if (
            board[target_row][col] != "."
            or board[origin_row][col] != "."
            or board[pawn_row][col] != pawn
        ):
            raise ValueError("En passant square doesn't match a pawn that just moved two squares")

    # --- The side NOT to move can't be in check --------------------------
    waiting = opponent(active_color)
    waiting_king = find_king(board, waiting)
    if is_square_attacked(board, waiting_king, active_color):
        raise ValueError(f"{'White' if waiting == 'w' else 'Black'} is in check but it isn't their turn")

    return {
        "board": board,
        "active_color": active_color,
        "castling": castling,
        "en_passant": en_passant,
        "half_move": half_move_int,
        "full_move": full_move_int,
    }


PIECE_CHARS = set("rnbqkpRNBQKP")
CASTLING_RE = re.compile(r"^K?Q?k?q?$")
EN_PASSANT_RE = re.compile(r"^[a-h][36]$")

SQUARES = {
    "a1": (7,0),
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
    "h8":(0,7)
    }