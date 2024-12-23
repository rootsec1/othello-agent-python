#!/usr/bin/python

import json
import socket
import sys
from copy import deepcopy

#
# Directions to check for potential flips: 8 neighbors
#
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


def switch_player(player):
    """
    Switches from player 1 to 2 or player 2 to 1.
    """
    return 2 if player == 1 else 1


def get_all_valid_moves(board, player):
    """
    Returns a list of all valid moves for the given player in the format:
    [(row, col, flips), ...]
    where 'flips' is a list of positions of opponent pieces that would be flipped
    by placing on (row, col).
    """
    valid_moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == 0:  # empty square
                flips = get_flips_if_valid(board, r, c, player)
                if flips:
                    valid_moves.append((r, c, flips))
    return valid_moves


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

        # If we ended on one of player's own pieces, all potential_flips are valid
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player and potential_flips:
            flips.extend(potential_flips)

    return flips


def make_move(board, row, col, player, flips):
    """
    Applies the move on (row, col) for 'player', flipping all 'flips' positions.
    Returns the modified board (in-place).
    """
    board[row][col] = player
    for (r, c) in flips:
        board[r][c] = player
    return board


def get_move(player, board):
    """
    A simplified two-step heuristic for Othello moves:
      1) Minimize the opponent's next-move possibilities (mobility).
      2) If there's a tie, choose the move that flips the most pieces now.

    Returns a (row, col) move or None if no valid moves.
    """
    valid_moves = get_all_valid_moves(board, player)
    if not valid_moves:
        return None  # No valid moves

    best_move = None
    min_opponent_moves = float('inf')
    best_flip_count = -1

    for (row, col, flips) in valid_moves:
        # Simulate the move on a temporary board
        temp_board = deepcopy(board)
        make_move(temp_board, row, col, player, flips)

        # Count how many moves the opponent will have
        opponent_valid_moves = get_all_valid_moves(
            temp_board, switch_player(player))
        next_moves_count = len(opponent_valid_moves)

        # Choose the move that yields fewer moves for the opponent
        if next_moves_count < min_opponent_moves:
            best_move = (row, col)
            min_opponent_moves = next_moves_count
            best_flip_count = len(flips)
        elif next_moves_count == min_opponent_moves:
            # Tie-break by the number of pieces flipped immediately
            if len(flips) > best_flip_count:
                best_move = (row, col)
                best_flip_count = len(flips)

    return list(best_move)


def prepare_response(move):
    """
    Encodes the move into a bytes object with a newline for sending via socket.
    """
    response_str = f"{move}\n".encode()
    print(f"sending {response_str!r}")
    return response_str


def main():
    """
    Main client loop:
      - Connect to the Othello server via a TCP socket
      - Receive board states in JSON
      - Compute a move using our simplified heuristic
      - Send the move back to the server
    """
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 1337
    host = sys.argv[2] if len(sys.argv) > 2 else socket.gethostname()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        while True:
            data = sock.recv(1024)
            if not data:
                print("connection to server closed")
                break

            json_data = json.loads(data.decode("UTF-8"))
            board, max_turn_time, player = (
                json_data["board"],
                json_data["maxTurnTime"],
                json_data["player"],
            )
            print(
                f"Player={player}, MaxTurnTime={max_turn_time}, Board={board}"
            )

            move = get_move(player, board)  # Use our simplified heuristic
            response = prepare_response(move)
            sock.sendall(response)


if __name__ == "__main__":
    main()
