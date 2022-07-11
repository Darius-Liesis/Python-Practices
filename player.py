import random
import math

#Defining a Player class
class Player:
    def __init__(self, letter):
        #Letter is X or O
        self.letter = letter
        
    def get_move(self, game):
        pass

#Using the theory of Minimizing and Maximizing the Utility function, we create a computer, that chooses the most optimal choice, always    
class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())    #Randomly chooses a square if there are all available squares
        else:    #Get's the square based off of the MiniMax algorithm
            square = self.minimax(game, self.letter)['position']
        return square
    
    def minimax(self, state, player):
        max_player = self.letter  # Since X is human, they are considered the Maximum player
        other_player = 'O' if player == 'X' else 'X'   #Whichever player a Human is not, the computer will be
        
        #Firstly, checking if the last move resulted in a win
        if state.current_winner == other_player:
            #Transforming the information into a dictionary
            #The dictionary will have position and score, in order to gauge an outcome
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)
                   }
        #If there are empty squares left, but no winner yet, then it returns 0 as a draw state
        elif not state.empty_squares():
            return {'position': None,
                    'score': 0
                   }
        
        if player == max_player:    #If the computer player is X, each score should maximize the value.
            best = {'position': None,
                    'score': -math.inf
                   }
        else:    #If the computer player is O, each score should minimize the value.
            best = {'position': None,
                    'score': math.inf
                   }
            
        for possible_move in state.available_moves():
            #The beginning of the algorithm. As such, it has to:
            #1. Try the chosen spot and make a move there;
            state.make_move(possible_move, player)
            #2. Simulate the game after that move using Recursion;
            sim_score = self.minimax(state, other_player)
            #3. Undo the move, return to the state beforehand;
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move
            #4. Update the dictionaries as necessary
            if player == max_player:    #Case of maximizing for X
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:     #Case of minimizing for O
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

#Using Inherritances to create random players 
class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
        
    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
        
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move from 0 to 8:')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError   #If no ValueError was raised
                valid_square = True 
            except ValueError:
                print("Invalid square, try again.")
        return val