"""Minimax Chess AI Class"""

class chessPlayer(object):
    
    def __init__(self, player):
        self.player=player
        self.values=self.init_values()

    # Initiates the values of each piece as a dictionary
    def init_values():
        values={
            (0, "pawn"):-1,
            (0, "rook"):-5,
            (0, "knight"):-3,
            (0, "bishop"):-3, 
            (0, "queen"):-9, 
            (0, "king"):-500,
            (1, "pawn"):1,
            (1, "rook"):5, 
            (1, "knight"):3, 
            (1, "bishop"):3, 
            (1, "queen"):9,
            (1, "king"):500, 
        }
        return values

    # Returns the value of a given board based on the pieces
    def value(self, board):
        result=0
        for row in range(8):
            for col in range(8):
                color=board[row][col][0]
                piece=board[row][col][1]
                if color is not None:
                    val=self.values[(color, piece)]
                    result+=val
        return val
    
    def terminal(self, board):

    # Minmax algo where white is minimizing and black is maximizing
    def minimax(self, board):

    
    def maximize(self, board):
    
    def minimize(self, board):
