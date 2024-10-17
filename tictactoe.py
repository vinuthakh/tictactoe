import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    # Count the number of X's and O's on the board
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    # X always starts first, so if they are equal, it's X's turn; otherwise, it's O's turn
    return X if x_count == o_count else O
    
def actions(board):
    # A set of all possible actions (i, j) where the board cell is EMPTY
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY}

def result(board, action):
    i, j = action
    if board[i][j] is not EMPTY:
        raise ValueError("Invalid action: Cell is already occupied")

    # Create a new board copy
    new_board = [row[:] for row in board]
    # Place the current player's move on the new board
    new_board[i][j] = player(board)
    
    return new_board

def winner(board):
    # Check rows, columns, and diagonals for a winner
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
    
    return None

def terminal(board):
    """
    Returns True if the game is over (either a win or a tie), False otherwise.
    """
    # The game is over if there's a winner
    if winner(board) is not None:
        return True
    
    # The game is over if there are no empty spaces left
    if all(cell is not EMPTY for row in board for cell in row):
        return True
    
    # Otherwise, the game is not over
    return False


def utility(board):
    winning_player = winner(board)
    if winning_player == X:
        return 1
    elif winning_player == O:
        return -1
    else:
        return 0

def minimax(board):
    if terminal(board):
        return None
    
    current_player = player(board)
    
    if current_player == X:
        best_value = -math.inf
        best_action = None
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
        return best_action
    else:
        best_value = math.inf
        best_action = None
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action
        return best_action

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
