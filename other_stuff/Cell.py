

class Cell:
    def __init__(self):
        self.bomb = False
        self.revealed = False
        self.neighbour_mines = 0
        self.flagged = False
