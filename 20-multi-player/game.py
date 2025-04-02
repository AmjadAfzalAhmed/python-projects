# defining game class that handles the game
class Game:
    def __init__(self, id):
        self.p1Went = False # if player 1 has not played
        self.p2Went = False # if player 2 has not played
        self.ready = False # if player 2 has not joined
        self.id = id # game id
        self.moves = [None, None] # player 1 and player 2 moves
        self.wins = [0,0] # player 1 and player 2 wins
        self.ties = 0 # number of ties
        self.ties = 0

    def get_player_move(self, p): # gets the player's move
        """
        :param p: [0,1] 
        :return: Move
        """
        return self.moves[p] # returns the player's move

    def play(self, player, move): # plays the game
        self.moves[player] = move # sets the player's move
        if player == 0:
            self.p1Went = True # player 1 has played
        else:
            self.p2Went = True # player 2 has played

    def connected(self): # checks if the players are connected
        return self.ready # returns the ready status

    def bothWent(self): # checks if both players have played
        return self.p1Went and self.p2Went # returns the player's status

    def winner(self): # returns the winner
        p1 = self.moves[0].upper()[0] # player 1 move
        p2 = self.moves[1].upper()[0] # player 2 move

        winner = -1 # no winner
        if p1 == "R" and p2 == "S": # player 1 wins
            winner = 0 # player 1 wins
        elif p1 == "S" and p2 == "R": # player 2 wins
            winner = 1 # player 2 wins
        elif p1 == "P" and p2 == "R": # player 1 wins
            winner = 0 # player 1 wins
        elif p1 == "R" and p2 == "P": # player 2 wins
            winner = 1 # player 2 wins
        elif p1 == "S" and p2 == "P": # player 1 wins
            winner = 0 # player 1 wins
        elif p1 == "P" and p2 == "S": # player 2 wins
            winner = 1 # player 2 wins

        return winner # returns the winner

    def resetWent(self): # resets the player's status
        self.p1Went = False # player 1 has not played
        self.p2Went = False # player 2 has not played