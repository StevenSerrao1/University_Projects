import Player_class as pc
import random
from Game_class import Game
# Imports below are to create a formatted board
from rich.console import Console
from rich.table import Table

# Initialize Rich console for formatted board output
console = Console()

# Initialize the Game class tot handle leaderboard and replay logic
game = Game()

class Board:
    # Class-level scoreboard shared across matches
    # NOTE: scoreboard & replay logic have been extracted to Game_class.py.
    # The attribute was intentionally removed so Game handles scoreboard now.

    def __init__(self):
        square: int  # Placeholder for potential future extensions

    @staticmethod
    def print_board(grid: list):
        """Render the current Tic-Tac-Toe grid in a visually clear table."""
        print('')
        table = Table(show_header=False, show_lines=True)
        for _ in range(3):
            table.add_column()  # Each column represents a Tic-Tac-Toe cell
        for row in grid:
            table.add_row(*row)  # Spread row cells into table
        console.print(table)

    @staticmethod
    def check_win(grid: list, symbol: str) -> bool:
        """
        Determine if the given symbol ('X' or 'O') has a winning combination.
        Checks rows, columns, and diagonals systematically.
        """
        # Check each row for a complete match
        for row in grid:
            if all(cell == symbol for cell in row):
                return True

        # Check each column for a complete match
        for col in range(3):
            if all(grid[row][col] == symbol for row in range(3)):
                return True

        # Check diagonals
        if all(grid[i][i] == symbol for i in range(3)):
            return True
        if all(grid[i][2 - i] == symbol for i in range(3)):
            return True

        # No winning combination found
        return False

    @staticmethod
    def setup_game(player_one: pc.Player, player_two: pc.Player):
        """Run a single Tic-Tac-Toe game, handling turns and input.
        Updates the Board.scoreboard when the game ends."""
        # Explicitly instantiate a 3x3 2D grid (fresh board each match)
        grid = [
            [" ", " ", " "],  # Row 0
            [" ", " ", " "],  # Row 1
            [" ", " ", " "]   # Row 2
        ]

        # Map 1-9 input to grid coordinates
        cell_to_coords = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 9: (2, 2)
        }

        game_active = True  # Control the game loop
        turns = 1           # Track turn number for alternating players and tie detection
        Board.print_board(grid)  # Show empty board

        while game_active:
            current_player = player_one if turns % 2 != 0 else player_two

            # Human player move
            if current_player.orientation == "Human":
                try:
                    choice = int(input(f'({turns}) {current_player.name} ({current_player.symbol}) move (1-9): '))
                except ValueError:
                    print("Please enter a valid number.")
                    continue

                if choice not in cell_to_coords:
                    print("Invalid choice. Pick a number between 1 and 9.")
                    continue

                row, col = cell_to_coords[choice]

                if grid[row][col] != " ":
                    print("Square already taken. Choose another one.")
                    continue

            # CPU player move
            else:
                # Gather empty cells
                empty_cells = [num for num, (r, c) in cell_to_coords.items() if grid[r][c] == " "]

                # Helper to test a prospective move for a given symbol
                def would_win(cell_num: int, symbol: str) -> bool:
                    r, c = cell_to_coords[cell_num]
                    # Make a shallow copy of grid to simulate the move
                    simulated = [row.copy() for row in grid]
                    simulated[r][c] = symbol
                    return Board.check_win(simulated, symbol)

                my_sym = current_player.symbol
                opp_sym = "O" if my_sym == "X" else "X"

                choice = None

                # 1) Try to win if possible
                for cell in empty_cells:
                    if would_win(cell, my_sym):
                        choice = cell
                        break

                # 2) Block opponent from winning
                if choice is None:
                    for cell in empty_cells:
                        if would_win(cell, opp_sym):
                            choice = cell
                            break

                # 3) Take the centre if available
                if choice is None and 5 in empty_cells:
                    choice = 5

                # 4) Prefer corners next
                if choice is None:
                    corners = [1, 3, 7, 9]
                    available_corners = [c for c in corners if c in empty_cells]
                    if available_corners:
                        # pick a random corner among available corners to vary play
                        choice = random.choice(available_corners)

                # 5) Otherwise, pick a random available space
                if choice is None:
                    # fallback to any empty cell (shouldn't be empty list unless board full)
                    if empty_cells:
                        choice = random.choice(empty_cells)
                    else:
                        # defensive fallback; shouldn't occur because tie handled by turns == 9
                        choice = 1

                row, col = cell_to_coords[choice]
                print(f'({turns}) {current_player.name} ({current_player.symbol}) move: {choice}')

            # Update the board and display
            grid[row][col] = current_player.symbol
            Board.print_board(grid)

            # Check for a win
            if Board.check_win(grid, current_player.symbol):
                print(f"{current_player.name} ({current_player.symbol}) wins!")
                # Scoreboard update moved to Game_class.py — return the winner symbol
                return current_player.symbol

            # Check for a tie
            if turns == 9:
                print("It's a tie!")
                # Scoreboard update moved to Game_class.py — return draw marker
                return "Draw"

            turns += 1  # Next turn

    @staticmethod
    def start_game():
        """Handle multiple games, player selection, scoreboard display, and replay with the same players."""
        print('============ Welcome to TIC-TAC-TOE ============\n------------------------------------------------\n')

        # Choose mode and create players once; replay uses the same players
        while True:
            try:
                vs_choice = int(input('Choose your mode:\n1.) Player vs. Player\n2.) Player vs. CPU\nSelect 1 or 2: '))
                if vs_choice == 1:
                    player_one = pc.Player(input('\nPlayer 1, enter your name: '), 'X', 'Human')
                    player_two = pc.Player(input('Player 2, enter your name: '), 'O', 'Human')
                    break
                elif vs_choice == 2:
                    player_one = pc.Player(input('\nPlayer 1, enter your name: '), 'X', 'Human')
                    player_two = pc.Player('CPU', 'O', 'Computer')
                    break
                else:
                    print("Invalid choice. Try again.")
            except ValueError as e:
                print(f"Error: {e}. Enter 1 or 2.")
                continue

        # Run replay logic
        game.run(player_one, player_two, Board)