# Othello Bot (Python)

This repository provides a **simple Othello bot** written in Python. It connects to an Othello server over TCP, receives board updates, and responds with moves based on a **two-step heuristic**.

![Othello - Atomic Games](https://github.com/user-attachments/assets/667fc039-1b15-4c54-925f-45ef75b7a454)


## Overview

Othello (also known as Reversi) is played on an 8×8 board. Each turn, a player places a piece such that it **flips** (converts) any contiguous line(s) of the opponent’s pieces trapped between the new piece and another of the player’s existing pieces. The aim is to have the majority of your colored pieces on the board at the end of the game.

This client:
1. **Connects** to a running Othello server (e.g., via `othello.jar`).
2. **Receives** the board state (`board`), the current player (`player`), and other info in JSON.
3. **Determines** a move using a **simple, effective** heuristic.
4. **Sends** the chosen move `[row, col]` back to the server.

---

## Key Features

1. **Simple Two-Step Heuristic**  
   - **Minimize Opponent Mobility**: Prefer moves that leave the opponent fewer valid moves.  
   - **Tie-Break by Immediate Flips**: If multiple moves yield the same opponent mobility, pick the one that flips the most pieces right now.

2. **Easy to Understand**  
   - The code is short, heavily commented, and avoids complex algorithms like Minimax.

3. **Socket-Based**  
   - Automatically connects to a TCP-based Othello game server.

---

## How It Works

1. **Receive Board State**: The server sends the board in JSON.  
2. **Find All Valid Moves**:  
   - For each empty square, check if placing our piece there can flip at least one line of opponent pieces.  
3. **Evaluate Each Move**:  
   - Temporarily place a piece there and see **how many valid moves** the opponent would have next.  
   - **Fewer opponent moves** is better.  
   - If there’s a tie, prefer the move that **flips the most** pieces immediately.  
4. **Send the Move**: The final `[row, col]` is sent back to the server.

---

## Detailed Logic Explanation

Our bot’s decision-making is centered on two concepts: **opponent mobility** and **immediate flips**.

1. **Opponent Mobility**  
   - After identifying all our valid moves, we temporarily make each possible move and check how many moves the **opponent** would have on their next turn.  
   - We prioritize moves that minimize the opponent’s mobility. This often forces the opponent into fewer (and possibly worse) moves, giving us a strategic advantage.

2. **Immediate Flips**  
   - If multiple moves produce the same (minimal) number of opponent moves, we choose the move that flips the **greatest** number of opponent pieces right away.  
   - This gives us a small material advantage on the board if all else is equal.

In other words, **the bot first looks to restrict what the opponent can do** next, and then **it looks to maximize its own immediate gain** in terms of flipped pieces.

---

## Usage Instructions

### Prerequisites
- **Python 3.6+**  
- A **game server** that listens for connections on a TCP port (e.g., `othello.jar`).

### Running the Client

1. **Start the Othello server**, for example:
   ```bash
   java -jar othello.jar
   ```
   This should launch a server listening on a port (often `1337` by default). Browser to [http://localhost:8080](http://localhost:8080) for the web interface.

2. **Run the client** (this repo’s code):
   ```bash
   python client.py
   ```
   - By default, it attempts to connect on `port=1337` and `host=socket.gethostname()`.
   - You can override this by specifying a port or host:
     ```bash
     python client.py 1337 localhost
     ```

The client will:
- Connect to the server.  
- Print each `board` state it receives, along with the `player` and any timing info.  
- Compute a move via the two-step heuristic.  
- Send back `[row, col]`.

---

## Code Explanation

### 1. `get_move(player, board)`
Determines the best move with this logic:
1. Gather **all valid moves** (each includes positions to flip).
2. For each move, **simulate** the board and count how many moves the opponent would have next.
3. Choose the move that **minimizes** the opponent’s mobility.
4. If there’s a tie, choose the move that **flips** the most pieces immediately.

### 2. `get_all_valid_moves(board, player)`
Loops over every board cell. If it’s empty (`0`), checks if placing a piece there flips any opponent pieces.

### 3. `get_flips_if_valid(board, row, col, player)`
Implements the Othello flipping rules:  
- Explores 8 directions from `(row, col)`.  
- Gathers contiguous opponent pieces until hitting the player’s own piece or the board edge.  
- If a player piece is reached, all “trapped” opponent pieces are flippable.

### 4. `make_move(board, row, col, player, flips)`
Places the piece and **flips** all identified opponent pieces in place.

### 5. `prepare_response(move)`
Encodes the final `[row, col]` move into a socket-friendly message ending with a newline.

### 6. `main()`
Sets up the **TCP connection**, then loops:
- **Reads** the board state from the server.
- **Invokes** `get_move(player, board)`.
- **Sends** the chosen move back to the server.

---

## Further Improvements

- **Add Corner/Edge Preferences**: Corners and edges can be crucial in Othello. You could weight these positions more heavily when deciding a move.  
- **Piece Count Parity**: Factor in the net difference in piece counts (yours vs. opponent’s) if you want a simple measure of material advantage.  
