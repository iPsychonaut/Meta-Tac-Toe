# Meta-Tac-Toe

## Introduction

Meta-Tac-Toe is an exciting variation of the classic game Tic-Tac-Toe. It's a game within a game! 
In Meta-Tac-Toe, you have a 3x3 meta-board, and each cell of this meta-board contains another 3x3 board, termed as a "small board". 
The objective is to win the meta-board by securing three small boards in a row, either horizontally, vertically, or diagonally.

## How to Play

1. Players alternate turns to place their symbol ('X' or 'O') in an empty cell within a small board.
2. The choice of which small board to play in is determined by the cell in which the previous player made their move.
3. If a player wins in a small board, their symbol occupies the entire small board.
4. The first player to align three of their symbols on the meta-board wins the game.

## Installation

The game requires Python and Pygame to be installed. If Pygame is not installed, the script will attempt to install it using conda.

## Code Structure

1. `pygame` is used for rendering the game board and handling user input.
2. The `draw_meta_board()` function is responsible for drawing both the meta-board and the small boards, including any 'X' or 'O' symbols.
3. The `draw_pieces()` function draws the symbols ('X' or 'O') in the respective cells.
4. The `check_winner_small_board()` function checks for a winner in a small board and returns the winning symbol or None.
5. The `update_small_board_winner()` function updates a small board with the winner's symbol.
6. The `check_winner_meta_board()` function checks for a winner in the meta-board and updates a global variable if a winner is found.

## Authors

- ian.michael.bollinger@gmail.com
- With the assistance of ChatGPT 4.0
