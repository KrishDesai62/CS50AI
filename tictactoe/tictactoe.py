"""
Tic Tac Toe Player
"""

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
    x = 0
    y = 0

    for row in board:
        for cell in row:
            if cell == X:
                x += 1
            elif cell == O:
                y += 1
    if x <= y:
        return X
    else:
        return O
    """
    Returns player who has the next turn on a board.
    """


def actions(board):
    empty_tuple = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                empty_tuple.add((i, j))
    return empty_tuple


    """
    Returns set of all possible actions (i, j) available on the board.
    """


def result(board, action):
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid action")
    
    new_board = [row[:] for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board



    """
    Returns the board that results from making move (i, j) on the board.
    """


def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None


    """
    Returns the winner of the game, if there is one.
    """


def terminal(board):
    if winner(board) is not None:
        return True
    if actions(board) == set():
        return True
    return False
    """
    Returns True if game is over, False otherwise.
    """


def utility(board):
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """


def minimax(board):
    if terminal(board):
        return None

    if player(board) == X:
        return max_value(board)[1]
    else:
        return min_value(board)[1]
    
def max_value(board):
    if terminal(board):
        return utility(board), None

    best_value = float("-inf")
    best_action = None

    for action in actions(board):
        val, _ = min_value(result(board, action))
        if val > best_value:
            best_value = val
            best_action = action

    return best_value, best_action

def min_value(board):
    if terminal(board):
        return utility(board), None

    best_value = float("inf")
    best_action = None

    for action in actions(board):
        val, _ = max_value(result(board, action))
        if val < best_value:
            best_value = val
            best_action = action

    return best_value, best_action




        

    """
    Returns the optimal action for the current player on the board.
    """
