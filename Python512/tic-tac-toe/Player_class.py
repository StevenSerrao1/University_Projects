class Player:
    # Create lists to hold allowed properties
    allowed_orientations = ['Human', 'Computer']
    allowed_symbols = ['X', 'O']

    # Constructor to type check the player initialization
    def __init__(self, name, symbol, orientation):
        if orientation not in self.allowed_orientations:
            raise ValueError("Orientation must be 'Human' or 'Computer'!")
        if symbol not in self.allowed_symbols:
            raise ValueError("Symbol must be 'X' or 'O'!")
        self.name = name
        self.symbol = symbol
        self.orientation = orientation