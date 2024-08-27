import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
BOARD_SIZE = 5
CELL_SIZE = 100
MARGIN = 5
WINDOW_SIZE = BOARD_SIZE * (CELL_SIZE + MARGIN) + MARGIN
FPS = 30
BUTTON_SIZE = 80
BUTTON_Y_OFFSET = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BUTTON_COLOR = LIGHT_GRAY
BUTTON_HOVER_COLOR = DARK_GRAY

# Create the screen
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + BUTTON_Y_OFFSET))
pygame.display.set_caption('5x5 Chess Game')

# Font
font = pygame.font.SysFont('Arial', 24)

# Game variables
board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = 'Player 1'

# Initialize the board with pieces
def initialize_board():
    global board
    board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    # Player 1 pieces
    board[0][0] = 'P1'
    board[0][1] = 'P1'
    board[0][2] = 'P1'
    board[0][3] = 'H1'
    board[0][4] = 'H2'

    # Player 2 pieces
    board[4][0] = 'p1'
    board[4][1] = 'p1'
    board[4][2] = 'p1'
    board[4][3] = 'h1'
    board[4][4] = 'h2'

# Draw the game board
def draw_board():
    screen.fill(WHITE)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = GREEN if (row + col) % 2 == 0 else BLUE
            pygame.draw.rect(screen, color, [(MARGIN + CELL_SIZE) * col + MARGIN,
                                             (MARGIN + CELL_SIZE) * row + MARGIN,
                                             CELL_SIZE, CELL_SIZE])

            piece = board[row][col]
            if piece != '.':
                draw_piece(row, col, piece)

# Draw a piece with visual differentiation
def draw_piece(row, col, piece):
    x = (MARGIN + CELL_SIZE) * col + MARGIN
    y = (MARGIN + CELL_SIZE) * row + MARGIN
    radius = CELL_SIZE // 4
    color = BLACK
    text_color = WHITE
    if piece.isupper():
        color = RED
        text_color = WHITE
    else:
        color = BLACK
        text_color = LIGHT_GRAY

    pygame.draw.circle(screen, color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), radius)
    text = font.render(piece, True, text_color)
    screen.blit(text, (x + CELL_SIZE // 2 - text.get_width() // 2,
                       y + CELL_SIZE // 2 - text.get_height() // 2))

# Draw buttons for moves
def draw_buttons(piece):
    moves = []
    if piece == 'P1' or piece == 'p1':  # Pawn
        moves = ['L', 'R', 'F', 'B']
    elif piece == 'H1' or piece == 'h1':  # Hero1
        moves = ['L', 'R', 'F', 'B']
    elif piece == 'H2' or piece == 'h2':  # Hero2
        moves = ['FL', 'FR', 'BL', 'BR']

    button_positions = []
    for i, move in enumerate(moves):
        x = 50 + i * (BUTTON_SIZE + 10)
        y = WINDOW_SIZE + BUTTON_Y_OFFSET - BUTTON_SIZE
        button_positions.append((x, y, move))

        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_COLOR
        if x < mouse_pos[0] < x + BUTTON_SIZE and y < mouse_pos[1] < y + BUTTON_SIZE:
            color = BUTTON_HOVER_COLOR

        pygame.draw.rect(screen, color, (x, y, BUTTON_SIZE, BUTTON_SIZE))
        pygame.draw.rect(screen, BLACK, (x, y, BUTTON_SIZE, BUTTON_SIZE), 2)  # Button border
        text = font.render(move, True, BLACK)
        screen.blit(text, (x + BUTTON_SIZE // 2 - text.get_width() // 2,
                           y + BUTTON_SIZE // 2 - text.get_height() // 2))

    return button_positions

# Check if a piece selection is valid
def is_valid_selection(row, col):
    global current_player
    piece = board[row][col]
    if current_player == 'Player 1' and piece in ['P1', 'H1', 'H2']:
        return True
    elif current_player == 'Player 2' and piece in ['p1', 'h1', 'h2']:
        return True
    return False

# Handle piece movement
def move_piece(x, y, move):
    global board
    piece = board[x][y]
    opponent_pieces = ['p1', 'h1', 'h2'] if piece.isupper() else ['P1', 'H1', 'H2']
    new_x, new_y = x, y

    if piece.lower() == 'p1':  # Pawn
        if move == 'L':
            new_y -= 1
        elif move == 'R':
            new_y += 1
        elif move == 'F':
            new_x += 1 if current_player == 'Player 1' else -1
        elif move == 'B':
            new_x -= 1 if current_player == 'Player 1' else 1
    elif piece.lower() == 'h1':  # Hero1
        if move == 'L':
            new_y -= 2
        elif move == 'R':
            new_y += 2
        elif move == 'F':
            new_x += 2 if current_player == 'Player 1' else -2
        elif move == 'B':
            new_x -= 2 if current_player == 'Player 1' else 2
    elif piece.lower() == 'h2':  # Hero2
        if move == 'FL':
            new_x += 2 if current_player == 'Player 1' else -2
            new_y -= 2
        elif move == 'FR':
            new_x += 2 if current_player == 'Player 1' else -2
            new_y += 2
        elif move == 'BL':
            new_x -= 2 if current_player == 'Player 1' else 2
            new_y -= 2
        elif move == 'BR':
            new_x -= 2 if current_player == 'Player 1' else 2
            new_y += 2

    if not (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE):
        return False

    if board[new_x][new_y] in opponent_pieces:
        print(f"{board[new_x][new_y]} captured!")
        board[new_x][new_y] = '.'

    board[x][y] = '.'
    board[new_x][new_y] = piece
    return True

# Switch player turn
def switch_player():
    global current_player
    current_player = 'Player 2' if current_player == 'Player 1' else 'Player 1'

# Main game loop
initialize_board()
selected_piece = None
selected_pos = None
button_positions = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = y // (CELL_SIZE + MARGIN)
            col = x // (CELL_SIZE + MARGIN)

            if y < WINDOW_SIZE:  # Click on board
                if not selected_piece:
                    if is_valid_selection(row, col):
                        selected_piece = board[row][col]
                        selected_pos = (row, col)
                        button_positions = draw_buttons(selected_piece)
                    else:
                        print("Invalid selection!")
                else:
                    for (bx, by, move) in button_positions:
                        if bx < x < bx + BUTTON_SIZE and by < y < by + BUTTON_SIZE:
                            if move_piece(selected_pos[0], selected_pos[1], move):
                                switch_player()
                                selected_piece = None
                                selected_pos = None
                                button_positions = []
                            else:
                                print("Invalid move!")
            else:  # Click on buttons area
                if selected_piece:
                    for (bx, by, move) in button_positions:
                        if bx < x < bx + BUTTON_SIZE and by < y < by + BUTTON_SIZE:
                            if move_piece(selected_pos[0], selected_pos[1], move):
                                switch_player()
                                selected_piece = None
                                selected_pos = None
                                button_positions = []
                            else:
                                print("Invalid move!")

    # Draw the game board
    draw_board()
    
    # Draw move buttons if a piece is selected
    if selected_piece:
        button_positions = draw_buttons(selected_piece)
    
    # Draw player turn indicator
    turn_text = font.render(f"{current_player}'s Turn", True, BLACK)
    screen.blit(turn_text, (10, WINDOW_SIZE + 10))

    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

