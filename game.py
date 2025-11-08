
def main():
    board = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    moves = generate_moves(board)
    print(moves)
    print(board)
    for row in board:                      # print board
        print(*row)



def parse_fen(fen):
    fen_pieces, to_move, castling_rights, ep, hm, fm = fen.split(" ")
    pieces = [[]]
    for char in fen:
        if char.isdigit():
            pieces[-1].extend(["_"] * int(char))
        elif char == "/":
            pieces.append([])
        elif char == " ":
            break
        else:
            pieces[-1].append(char)
    #print(*pieces,sep = "\n")
    return pieces


def generate_moves(board):
    pawn_moves = pawn_start_moves(board) + pawn_other_moves(board) + 
    return pawn_moves
    raise NotImplementedError("This function is not implemented yet.")


def pawn_start_moves(board): #For white pawns only
    moves = 0
    for row_idx, row in enumerate(board):
        for col_idx, sq in enumerate(row):
            if board[row_idx][col_idx] == "P":
                #a2 pawn
                if (row_idx, col_idx) in [(6, 0)]:
                    if board[row_idx-1][col_idx] == "_":
                        moves += 1
                    if board[row_idx-2][col_idx] == "_":
                        moves += 1
                    if board[row_idx-1][col_idx+1] in ["r","n","b","q","k","p"]:
                        moves += 1
                #b2 to g2 pawns
                if (row_idx, col_idx) in [(6, 1),(6,2),(6,3),(6,4),(6,5),(6,6)]:
                    if board[row_idx-1][col_idx] == "_":
                        moves += 1
                    if board[row_idx-2][col_idx] == "_":
                        moves += 1
                    if board[row_idx-1][col_idx+1] in ["r","n","b","q","k","p"]:
                        moves += 1
                    if board[row_idx-1][col_idx-1] in ["r","n","b","q","k","p"]:
                        moves += 1
                #h2 pawn
                if (row_idx, col_idx) in [(6, 7)]:
                    if board[row_idx-1][col_idx] == "_":
                        moves += 1
                    if board[row_idx-2][col_idx] == "_":
                        moves += 1
                    if board[row_idx-1][col_idx-1] in ["r","n","b","q","k","p"]:
                        moves += 1
    return moves


def pawn_other_moves(board): #For white pawns only
    moves = 0
    for row_idx, row in enumerate(board):
        for col_idx, sq in enumerate(row):
            if board[row_idx][col_idx] == "P":
                if board[row_idx][col_idx] not in board[6]:
                    if board[row_idx][col_idx] in [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)]:
                        if board[row_idx-1][col_idx] == "_":
                            moves += 1
                        if board[row_idx-1][col_idx+1] in ["r","n","b","q","k","p"]:
                            moves += 1
                    if board[row_idx][col_idx] in [(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7)]:
                        if board[row_idx-1][col_idx] == "_":
                            moves += 1
                        if board[row_idx-1][col_idx-1] in ["r","n","b","q","k","p"]:
                            moves += 1

                    if board[row_idx-1][col_idx] == "_":
                        moves += 1
                    if board[row_idx-1][col_idx+1] in ["r","n","b","q","k","p"]:
                            moves += 1
                    if board[row_idx-1][col_idx-1] in ["r","n","b","q","k","p"]:
                            moves += 1
    return moves


def knight_moves(board):
     #code 50 unique moves for outer 2 rows and cols
     moves = 0
     for row_idx, row in enumerate(board):
         for col_idx, sq in enumerate(row):
             if board[row_idx][col_idx] == "K":
                ...

def apply_move(board, move):
    raise NotImplementedError("This function is not implemented yet.")

main()