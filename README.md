# ♟️ Chess_moves

## Project Description

**Chess_moves** is a comprehensive **Python program** designed to analyze and play chess games. It takes a standard **FEN (Forsyth-Edwards Notation) string** as input, providing a detailed breakdown and **visual representation** of the specified chess position. From this starting position, users can continue to play a full, interactive **player-vs-player game** for both White and Black.

---

## 🛠️ Features Overview

* **FEN String Analysis:** Input any standard FEN string to instantly analyze and visualize the position, including whose turn it is, castling rights, and en passant target squares.
* **Visual Position Representation:** Turns FEN strings into a clear, visual representation of the chess board in the console (or potentially a graphical interface).
* **Full Player-vs-Player Game:** Play a full, interactive game of chess starting from the initial setup or any custom FEN position, complete with move validation.

---

## 💻 Technologies Used

* **VS Code** (Development Environment)
* **Python Programming Language**

---

## 📂 Code Structure Overview

The project is structured into three main files for modularity and testing:

| File Name | Purpose |
| :--- | :--- |
| `game_functions.py` | Contains all the core functions and/or classes for FEN parsing, board representation, piece movement, and move validation logic. |
| `game.py` | Implements the main game loop, user input handling, and flow for playing the game (ties the functions together). |
| `test_game.py` | Contains unit tests for functions, ensuring correctness of move validation, FEN parsing, and error handling. |

---

## 💡 Possible Approaches to Complete the Project

There are two primary ways to approach the implementation of a project like this, each with trade-offs:

### 1. Using a Third-Party Library (Recommended)

This approach significantly speeds up development by leveraging robust, battle-tested libraries for the complex logic.

* **Key Tool:** Use the widely-adopted `python-chess` library.
* **Pros:**
    * Handles the most difficult parts of chess programming: **FEN parsing**, **legal move generation**, **move validation** (including checks, checkmates, and stalemates) out-of-the-box.
    * Saves immense development time and reduces bugs.
* **Implementation Focus:** The project logic (`game.py`) will focus on user input/output (the game interface) and calling the library's methods.

### 2. Manual Implementation (Challenging)

This approach involves building all the chess logic from scratch.

* **Key Tool:** Pure Python using classes (e.g., `Board`, `Piece`) and data structures (e.g., arrays or dictionaries) to represent the board.
* **Pros:**
    * Gives the developer complete control and a deep understanding of chess engine logic.
    * Zero external dependencies.
* **Implementation Focus:**
    * **FEN Parsing:** Implementing the function to convert the FEN string into an internal board state.
    * **Move Validation:** The hardest part—writing custom logic to ensure every move is legal (e.g., pin detection, king safety, castling rules, en passant).

---

## 🚀 Basic Usage Examples

### 1. Analyzing a FEN String

Run the main game file, passing the FEN as a command-line argument:

```bash
python game.py "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"




"
Please create a comprehensive README.md file for my project based on the following information:


Project name: [Chess_moves]

Description: [a python program that takes in a fen string and prints out all information about that particular position. You can also continue playing from that position for both black and white]

Key features:

- [turn fen strings into a visual representation of a chess position]

- [play a full game of chess (player vs player)]


Technologies used: [vs code, python programming language]


The README should include:

1. Clear project title and description

2. Features overview

3. Possible approaches to complete the project


Code structure overview:

game_functions.py: contains all functions and/or classes to be used in the program

game.py: game logic implementation

test_game: unittests for functions, error handling, etc