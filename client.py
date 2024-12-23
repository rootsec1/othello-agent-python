#!/usr/bin/python
"""
Entrypoint for the Othello/Reversi AI Client.

Usage:
  python client.py [port] [host]

If no port or host is provided, defaults are:
  port = 1337
  host = socket.gethostname()
"""

import json
import socket
import sys

from othello.bot import get_move
from othello.utils import prepare_response


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

            # Parse the JSON from the server
            json_data = json.loads(data.decode("UTF-8"))
            board = json_data["board"]
            max_turn_time = json_data["maxTurnTime"]
            player = json_data["player"]
            print(f"Player={player}, MaxTurnTime={max_turn_time}, Board={board}")

            # Compute move using the simplified heuristic
            move = get_move(player, board)

            # Prepare and send the move
            response = prepare_response(move)
            sock.sendall(response)


if __name__ == "__main__":
    main()
