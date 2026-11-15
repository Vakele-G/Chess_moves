from game_functions import *


START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
PROMOTION_PIECES = "QRBN"


def main() -> None:
    game = read_game()
    print()
    print_board(game.board)

    if report_status(game):
        return

    while True:
        move = ask_move(game)
        if move is None:
            print("Goodbye.")
            return

        game.play(*move) # The * unpacks 'move' into parameters
        print()
        print_board(game.board)
        print()

        if report_status(game):
            return


def read_game() -> Game:
    print("/////////////////////////////////////////////////")
    print('ENTER "new game" to begin game as white OR')

    while True:
        text = input("enter a FEN string to play from that position: ").strip()
        try:
            if text.lower() == "new game":
                return Game(START_FEN)
            else:
                return Game(text)
        except ValueError as e:
            print(f"Invalid FEN: {e}")


def report_status(game :Game) -> bool:
    """Print check/mate/stalemate info.
    Return True if the game is over.
    """
    status = game.status()
    if status == "checkmate":
        winner = "Black" if game.active_color == "w" else "White"
        print(f"Checkmate! {winner} wins!")
        return True
    if status == "stalemate":
        print("Stalemate! The game is a draw.")
        return True
    if status == "check":
        print(f"{'White' if game.active_color == 'w' else 'Black'} is in check!")
    return False


def ask_move(game :Game):
    """Return (sq1, sq2, promotion) for a legal move, or None to quit."""
    while True:
        text = input("\nEnter a move (eg. e2 e4) or 'q' to quit: ").strip().lower()
        if text == "q":
            return None

        parts = text.split()
        if len(parts) not in (2, 3) or parts[0] not in game.squares or parts[1] not in game.squares:
            print("Invalid move. Use: from_square to_square [promotion_piece]")
            continue

        sq1, sq2 = parts[0], parts[1]
        promo = parts[2] if len(parts) == 3 else None

        row, col = game.squares[sq1]
        piece = game.board[row][col]
        last_rank = 0 if piece == "P" else 7
        is_promotion = piece in ("P", "p") and game.squares[sq2][0] == last_rank

        # Only ask for a promotion piece if the move is otherwise legal.
        if is_promotion and promo is None:
            if game.validate_move(sq1, sq2, "Q" if piece == "P" else "q"):
                while True:
                    choice = input("Pawn promotion! Choose piece (Q/R/B/N): ").strip().lower()
                    if choice in ("q", "r", "b", "n"):
                        promo = choice
                        break
                    print("Invalid choice. Choose Q, R, B, or N.")

        if game.validate_move(sq1, sq2, promo):
            return sq1, sq2, promo
        print("Illegal move.")


if __name__ == "__main__":
    main()