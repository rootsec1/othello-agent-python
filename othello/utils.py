"""
Utility functions for the Othello bot, including:
- Direction definitions
- Player switching
- Valid move checking
- Move application
- Socket response preparation
"""

from copy import deepcopy

# Directions to check for potential flips: 8 neighbors
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


def switch_player(player):
    """
    Switches from player 1 to player 2, or player 2 to player 1.
    """
    return 2 if player == 1 else 1


def prepare_response(move):
    """
    Encodes the move (row, col) into a bytes object with a newline for sending via socket.
    """
    if move is None:
        # If no valid move, we might pass a special marker like [-1, -1]
        # but the server might interpret that differently. Adjust as needed.
        move = [-1, -1]
    response_str = f"{move}\n".encode()
    print(f"sending {response_str!r}")
    return response_str


def get_flips_if_valid(board, row, col, player):
    """
    Checks if placing a piece for 'player' at (row, col) is valid.
    Returns a list of positions of opponent pieces that would be flipped if valid,
    or an empty list if invalid.
    """
    opponent = switch_player(player)
    flips = []

    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        potential_flips = []

        # Move in the direction while we see opponent pieces
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            potential_flips.append((r, c))
            r += dr
            c += dc

        # If we ended on the player's own piece and have flipped opponent pieces in between
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player and potential_flips:
            flips.extend(potential_flips)

    return flips


def get_all_valid_moves(board, player):
    """
    Returns a list of all valid moves for the given player in the format:
    [(row, col, flips), ...]
    where 'flips' is a list of positions of opponent pieces that would be flipped.
    """
    valid_moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == 0:  # empty square
                flips = get_flips_if_valid(board, r, c, player)
                if flips:
                    valid_moves.append((r, c, flips))
    return valid_moves


def make_move(board, row, col, player, flips):
    """
    Applies the move on (row, col) for 'player', flipping all 'flips' positions.
    Returns the modified board (in-place).
    """
    board[row][col] = player
    for (r, c) in flips:
        board[r][c] = player
    return board


def simulate_move(board, row, col, player, flips):
    """
    Returns a DEEP COPY of the board after the move is made, 
    so as not to modify the original board in-place.
    """
    from copy import deepcopy
    temp_board = deepcopy(board)
    make_move(temp_board, row, col, player, flips)
    return temp_board
