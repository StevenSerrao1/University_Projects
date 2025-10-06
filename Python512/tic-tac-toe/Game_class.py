class Game:
    """Handles scoreboard tracking and replay loop for Tic-Tac-Toe matches.

    Use:
        game = Game()
        game.run(player_one, player_two, Board)
    """

    def __init__(self):
        # Shared scoreboard for the whole session
        self.scoreboard = {"X": 0, "O": 0, "Draws": 0}

    def run(self, player_one, player_two, board):
        """Run repeated matches using Board.setup_game and manage scoreboard & replay."""
        play_again = True

        # Main replay loop: play matches with the same players until they opt out
        while play_again:
            # Play a single match; Board.setup_game returns 'X','O', or 'Draw'
            result = board.setup_game(player_one, player_two)

            # Update scoreboard based on result
            if result == "X":
                self.scoreboard["X"] += 1
            elif result == "O":
                self.scoreboard["O"] += 1
            elif result == "Draw":
                self.scoreboard["Draws"] += 1

            # Display scoreboard after the match
            print("\n===== SCOREBOARD =====")
            print(f"{player_one.name} (X) Wins: {self.scoreboard['X']}")
            print(f"{player_two.name} (O) Wins: {self.scoreboard['O']}")
            print(f"Draws: {self.scoreboard['Draws']}")
            print("======================\n")

            # Prompt for replay; keep asking until valid input
            while True:
                endgame = input('Would you like to play again? (y/n): ').strip().lower()
                if endgame == 'y':
                    # Start a new round with the same players; board resets inside setup_game
                    break
                elif endgame == 'n':
                    print("Thanks for playing! Goodbye.")
                    play_again = False
                    break
                else:
                    print("Invalid input. Type 'y' or 'n'.")