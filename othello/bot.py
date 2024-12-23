"""
Othello bot logic using a simplified two-step heuristic:
  1) Minimize the opponent's next-move possibilities (mobility).
  2) Tie-break by the number of pieces flipped immediately.
"""

from math import inf
from .utils import (
    switch_player,
    get_all_valid_moves,
    simulate_move
)


def get_move(player, board):
    """
    Finds the best move for 'player' using the two-step heuristic:
      1) Minimize the opponent's mobility next turn
      2) Tie-break: maximize immediate flips
    Returns [row, col] or None if no valid moves.
    """
    valid_moves = get_all_valid_moves(board, player)
    if not valid_moves:
        return None  # No valid moves

    best_move = None
    min_opponent_moves = inf
    best_flip_count = -1

    for (row, col, flips) in valid_moves:
        # Create a temporary board after making this move
        temp_board = simulate_move(board, row, col, player, flips)

        # Count how many moves the opponent will have
        opponent_moves = get_all_valid_moves(temp_board, switch_player(player))
        next_moves_count = len(opponent_moves)

        # Evaluate based on two-step heuristic
        if next_moves_count < min_opponent_moves:
            best_move = (row, col)
            min_opponent_moves = next_moves_count
            best_flip_count = len(flips)
        elif next_moves_count == min_opponent_moves:
            # Tie-break using the number of pieces flipped
            if len(flips) > best_flip_count:
                best_move = (row, col)
                best_flip_count = len(flips)

    return list(best_move)  # Convert tuple to list for consistency
