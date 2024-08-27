from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Constants
BOARD_SIZE = 5

# Game variables
board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
captured_by_player1 = []
captured_by_player2 = []
current_player = 'Player 1'

# Initialize the board with pieces
def initialize_board():
    global board, captured_by_player1, captured_by_player2, current_player
    board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    captured_by_player1 = []
    captured_by_player2 = []
    current_player = 'Player 1'

    # Player 1 pieces
    board[0][0] = 'P1'
    board[0][1] = 'P2'
    board[0][2] = 'P3'
    board[0][3] = 'H1'
    board[0][4] = 'H2'

    # Player 2 pieces
    board[4][0] = 'p4'
    board[4][1] = 'p5'
    board[4][2] = 'p6'
    board[4][3] = 'h1'
    board[4][4] = 'h2'

initialize_board()

# Check if a piece selection is valid
def is_valid_selection(row, col):
    """Check if the selected piece belongs to the current player."""
    piece = board[row][col]
    if current_player == 'Player 1' and piece in ['P1','P2','P3', 'H1', 'H2']:
        return True
    elif current_player == 'Player 2' and piece in ['p5','p4','p6', 'h1', 'h2']:
        return True
    return False

def move_piece(x, y, move):
    global board, captured_by_player1, captured_by_player2, current_player
    piece = board[x][y]
    opponent_pieces = ['p1','p2','p3','p4','p5','p6', 'h1', 'h2'] if piece.isupper() else ['P1','P2','P3','P4','P5','P6', 'H1', 'H2']
    player_pieces = ['P1','P2','P3','P4','P5','P6', 'H1', 'H2']if piece.isupper() else ['p1','p2','p3','p4','p5','p6', 'h1', 'h2']
    new_x, new_y = x, y

    # Calculate new position based on move
    if piece.lower() in ['p1', 'p2', 'p3', 'p4', 'p5', 'p6']:  # Pawn
        if move == 'L':
            new_y -= 1
        elif move == 'R':
            new_y += 1
        elif move == 'F':
            new_x += 1 if current_player == 'Player 1' else -1
        elif move == 'B':
            # Prevent moving "backward" from initial row
            if (current_player == 'Player 1' and x == 0) or (current_player == 'Player 2' and x == BOARD_SIZE - 1):
                return False
            new_x -= 1 if current_player == 'Player 1' else 1
    elif piece.lower() == 'h1':  # Hero1
        if move == 'L':
            new_y -= 2
        elif move == 'R':
            new_y += 2
        elif move == 'F':
            new_x += 2 if current_player == 'Player 1' else -2
        elif move == 'B':
            # Prevent moving "backward" from initial row
            if (current_player == 'Player 1' and x == 0) or (current_player == 'Player 2' and x == BOARD_SIZE - 1):
                return False
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

    # Check if new position is out of bounds
    if not (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE):
        return False

    # Prevent moving onto a piece of the same player
    if board[new_x][new_y] in player_pieces:
        return False

    # Capture opponent piece if present
    if board[new_x][new_y] in opponent_pieces:
        print(f"{board[new_x][new_y]} captured!")

        # Track captured pieces
        if current_player == 'Player 1':
            captured_by_player1.append(board[new_x][new_y])
        else:
            captured_by_player2.append(board[new_x][new_y])

        board[new_x][new_y] = '.'

    # Move piece to new position
    board[x][y] = '.'
    board[new_x][new_y] = piece

    # Check for a winner after moving the piece
    check_winner()

    return True

def check_winner():
    """Check if a player has captured 5 pieces and declare the winner."""
    if len(captured_by_player1) >= 5:
        print("Player 1 wins!")
        reset_game()
    elif len(captured_by_player2) >= 5:
        print("Player 2 wins!")
        reset_game()

def reset_game():
    """Reset the game to its initial state."""
    print("Resetting game...")
    initialize_board()

# Switch player turn
def switch_player():
    global current_player
    current_player = 'Player 2' if current_player == 'Player 1' else 'Player 1'

# API endpoint to get game state
@app.route('/game_state', methods=['GET'])
def game_state():
    return jsonify(board=board, current_player=current_player)

# API endpoint to handle piece selection
@app.route('/select_piece', methods=['POST'])
def select_piece():
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')
    
    if is_valid_selection(row, col):
        piece = board[row][col]
        return jsonify(valid=True, piece=piece)
    else:
        return jsonify(valid=False, message="Invalid selection!")

# API endpoint to handle piece movement
@app.route('/move_piece', methods=['POST'])
def move():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    move = data.get('move')

    if move_piece(x, y, move):
        switch_player()
        return jsonify(success=True, board=board, current_player=current_player)
    else:
        return jsonify(success=False, message="Invalid move!")

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
