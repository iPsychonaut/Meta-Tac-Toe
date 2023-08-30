# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 11:53:55 2023

@author: ian.michael.bollinger@gmail.com with the help of ChatGPT 4.0

Meta-Tac-Toe is an exciting twist on the classic game of Tic-Tac-Toe.
The game board is a 3x3 grid, and each cell in this grid contains another 3x3 grid known as a "small board".
The objective is to win the "meta-board" by securing three small boards in a row, either horizontally, vertically, or diagonally.

"""
import pygame
import sys, subprocess

try:
    # Initialize Pygame
    pygame.init()
except:
    # if module not found try installing pygame
    pygame_cmd = ['conda',
                  'install', '-y',
                  '-c', 'conda-forge',
                  'pygame==2.5.1']
    print(f"CMD:\t{' '.join(pygame_cmd)}")
    mamba_result = subprocess.check_call(pygame_cmd,
                                         stdout=subprocess.DEVNULL,
                                         stderr=subprocess.DEVNULL)
    if mamba_result == 0:
        print(f'PASS:\tSuccessfully installed: pygame')
    else:
        print(f'ERROR:\tUnable to install: pygame')

# Constants
WINDOW_SIZE = (900, 900)
GRID_SIZE = 3
META_GRID_SIZE = GRID_SIZE * GRID_SIZE
GRID_CELL_SIZE = WINDOW_SIZE[0] // META_GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)

# Initialize font
pygame.font.init()
myfont = pygame.font.SysFont('Avenir', 30)

# Create screen object
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set window title
pygame.display.set_caption('Meta-Tac-Toe')

# Initialize game state variables
meta_board = [[[[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
               for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
meta_state = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_board = None
current_player = 'X'
winner = None

# Function to draw the meta-board and small boards
def draw_meta_board():    
    # Loop through each of the 3x3 meta boards to draw the small boards inside them
    for meta_x in range(GRID_SIZE):
        for meta_y in range(GRID_SIZE):
            x_offset = meta_x * GRID_SIZE * GRID_CELL_SIZE
            y_offset = meta_y * GRID_SIZE * GRID_CELL_SIZE
            border_color = WHITE  # Default color

            # Highlight the next board to play in
            if current_board is not None:
                if (meta_x, meta_y) == current_board and meta_state[meta_x][meta_y] == ' ':
                    border_color = GREEN
            
            # Highlight the whole meta-board when the player has free choice
            elif current_board is None:
                border_color = GREEN
            
            # Draw the internal grid lines for the small boards
            for x in range(1, GRID_SIZE):
                pygame.draw.line(screen, border_color,
                                 (x_offset + x * GRID_CELL_SIZE, y_offset),
                                 (x_offset + x * GRID_CELL_SIZE, y_offset + GRID_SIZE * GRID_CELL_SIZE),
                                 2)
                pygame.draw.line(screen, border_color,
                                 (x_offset, y_offset + x * GRID_CELL_SIZE),
                                 (x_offset + GRID_SIZE * GRID_CELL_SIZE, y_offset + x * GRID_CELL_SIZE),
                                 2)

            # Draw the external border for each small board
            pygame.draw.rect(screen, border_color,
                             (x_offset, y_offset, GRID_SIZE * GRID_CELL_SIZE, GRID_SIZE * GRID_CELL_SIZE),
                             5)

# Function to draw X and O pieces on the board
def draw_pieces():
    for meta_x in range(GRID_SIZE):
        for meta_y in range(GRID_SIZE):
            x_offset = meta_x * GRID_SIZE * GRID_CELL_SIZE
            y_offset = meta_y * GRID_SIZE * GRID_CELL_SIZE

            # Check if this small board has a winner
            small_winner = meta_state[meta_x][meta_y]

            # If a winner exists, draw a large symbol
            if small_winner != ' ':
                x = x_offset + GRID_CELL_SIZE // 2 + GRID_CELL_SIZE
                y = y_offset + GRID_CELL_SIZE // 2 + GRID_CELL_SIZE
                size = GRID_SIZE * GRID_CELL_SIZE // 2 - 10
                
                # Draw square behind the winner's large symbol
                pygame.draw.rect(screen,
                                 BLACK,
                                 (x - size, y - size, 2 * size, 2 * size))
                
                # Draw the winner's large symbol
                if small_winner == 'X':
                    pygame.draw.line(screen,
                                     WHITE,
                                     (x - size, y - size),
                                     (x + size, y + size),
                                     5)
                    pygame.draw.line(screen,
                                     WHITE,
                                     (x + size, y - size),
                                     (x - size, y + size),
                                     5)
                elif small_winner == 'O':
                    pygame.draw.circle(screen,
                                       WHITE,
                                       (x, y),
                                       size,
                                       5)
            else:
                # Draw small pieces
                for i in range(GRID_SIZE):
                    for j in range(GRID_SIZE):
                        x = x_offset + i * GRID_CELL_SIZE
                        y = y_offset + j * GRID_CELL_SIZE
                        
                        # DESCRIPTION
                        if meta_board[meta_x][meta_y][i][j] == 'X':
                            pygame.draw.line(screen,
                                             WHITE,
                                             (x + 10, y + 10),
                                             (x + GRID_CELL_SIZE - 10, y + GRID_CELL_SIZE - 10),
                                             5)
                            pygame.draw.line(screen,
                                             WHITE,
                                             (x + GRID_CELL_SIZE - 10, y + 10),
                                             (x + 10, y + GRID_CELL_SIZE - 10),
                                             5)
                        elif meta_board[meta_x][meta_y][i][j] == 'O':
                            pygame.draw.circle(screen,
                                               WHITE,
                                               (x + GRID_CELL_SIZE // 2, y + GRID_CELL_SIZE // 2),
                                               GRID_CELL_SIZE // 2 - 10,
                                               5)

# Function to check for a winner in a small board
def check_winner_small_board(board):
    """
    Check if there is a winner in the given 3x3 small board.

    Parameters
    ----------
    board : list of list of str
        The 3x3 board to check.

    Returns
    -------
    str or None
        Returns 'X' or 'O' if there is a winner, otherwise returns None.
    """
    # Check each row for a winner
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]
    
    # Check each column for a winner
    for col in range(GRID_SIZE):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]
    
    # Check the diagonals for a winner
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    
    return None

# Function to update small board with the winner's symbol
def update_small_board_winner(meta_x, meta_y, winner):
    """
    Update the small board at coordinates (meta_x, meta_y) with the winner's symbol.

    Parameters
    ----------
    meta_x : int
        The x-coordinate of the meta board.
    meta_y : int
        The y-coordinate of the meta board.
    winner : str
        The winner's symbol ('X' or 'O').
    """
    # Fill every cell of the small board with the winner's symbol
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            meta_board[meta_x][meta_y][i][j] = winner

# Function to check for a winner in the meta-board
def check_winner_meta_board():
    """
    Check if there's a winner in the meta-board.
    Updates the global variable 'winner' if a winner is found.
    """
    global winner
    
    # Check each row in the meta-board for a winner
    for row in meta_state:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            winner = row[0]
            return
    
    # Check each column in the meta-board for a winner
    for col in range(GRID_SIZE):
        if meta_state[0][col] == meta_state[1][col] == meta_state[2][col] and meta_state[0][col] != ' ':
            winner = meta_state[0][col]
            return
    
    # Check the diagonals in the meta-board for a winner
    if meta_state[0][0] == meta_state[1][1] == meta_state[2][2] and meta_state[0][0] != ' ':
        winner = meta_state[0][0]
        return
    if meta_state[0][2] == meta_state[1][1] == meta_state[2][0] and meta_state[0][2] != ' ':
        winner = meta_state[0][2]
        return

# Main game loop
running = True
while running:
    screen.fill(BLACK)
    draw_meta_board()

    # Render turn text
    turn_text = f"{current_player}'s Turn"
    text_surface = myfont.render(turn_text, False, LIGHT_BLUE)
    screen.blit(text_surface, (WINDOW_SIZE[0] // 2 - text_surface.get_width() // 2, 10))

    # Check for game events
    for event in pygame.event.get():
        
        # User input to Quit
        if event.type == pygame.QUIT:
            running = False

        # User Placement
        if event.type == pygame.MOUSEBUTTONDOWN and winner is None:
            # Get the position the user clicked in terms of game
            x, y = event.pos
            meta_x = x // (GRID_SIZE * GRID_CELL_SIZE)
            meta_y = y // (GRID_SIZE * GRID_CELL_SIZE)
            inner_x = (x % (GRID_SIZE * GRID_CELL_SIZE)) // GRID_CELL_SIZE
            inner_y = (y % (GRID_SIZE * GRID_CELL_SIZE)) // GRID_CELL_SIZE
            
            # Check if the clicked cell is valid for placement
            if current_board is None or (current_board == (meta_x, meta_y) and meta_state[meta_x][meta_y] == ' ') or meta_state[meta_x][meta_y] != ' ':
                if meta_board[meta_x][meta_y][inner_x][inner_y] == ' ':
                    meta_board[meta_x][meta_y][inner_x][inner_y] = current_player
                    small_winner = check_winner_small_board(meta_board[meta_x][meta_y])

                    # Check if a user won a small game with the last placement
                    if small_winner:
                        meta_state[meta_x][meta_y] = small_winner
                        update_small_board_winner(meta_x, meta_y, small_winner)
                        check_winner_meta_board()

                    # Set the next board for following player to play in
                    current_board = (inner_x, inner_y)
                    if meta_state[current_board[0]][current_board[1]] != ' ':
                        current_board = None
                    
                    # Set current player
                    current_player = 'O' if current_player == 'X' else 'X'

    # Draw each player's pieces
    draw_pieces()

    # Check if a user won the meta-game
    if winner:
        font = pygame.font.Font(None, 100)
        text = font.render(f"Player {winner} wins!", True, LIGHT_BLUE)
        screen.blit(text, (WINDOW_SIZE[0] // 4, WINDOW_SIZE[1] // 4))
    
    # Update the pygame display
    pygame.display.update()

# Quit the game and system exit on closing
pygame.quit()
sys.exit()