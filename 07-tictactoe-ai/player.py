import math
import random

class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        available = game.available_moves()
        if not available:
            return None  # Prevent error if no moves left
        return random.choice(available)


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + "'s turn. Input move (0-8): ").strip()

            if not square.isdigit():  # Ensures input is a number
                print("Invalid input! Please enter a number between 0 and 8.")
                
                continue  # This was outside the while loop

            val = int(square)  # Convert to integer safely

            if val not in game.available_moves():
                print("Invalid square. Try again!")
            else:
                valid_square = True  # Valid input, exit loop

        return val


class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.letter)['position']
        return square
    
    def minimax(self, state, player):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        # check if previous move is a winner
        if state.current_winner == other_player:
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1)
            if other_player == max_player else -1 * 
            (state.num_empty_squares() + 1)}
        
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}# each score should maximize
        else:
            best = {'position':None, 'score': math.inf} # each score should minimize

        for possible_move in state.available_moves():
            state.make_move(possible_move,player)
            sim_score = self.minimax(state, other_player) 

            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best