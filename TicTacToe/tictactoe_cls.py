import numpy as np
import random

row = 3
col = 3

# TicTacToe game from user MJeremy2017 on GitHub
class TicTacToe:
    def __init__(self, p1, p2):
        self.board = np.zeros((row, col))
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False 
        self.boardHash = None # hash containing current board state
        self.playerSymbol = 1 # p1 plays first, p1 = 1, p2 = -1

    def getHash(self):
        self.boardHash = str(self.board.reshape(col * row))
        return self.boardHash

    def outcome(self):
        # row
        for i in range(row):
            if sum(self.board[i, :]) == 3: # p1 wins
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3: # p2 wins
                self.isEnd = True
                return -1
        # col
        for i in range(col):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1
        # diagonal
        diag_sum1 = sum([self.board[i, i] for i in range(col)])
        diag_sum2 = sum([self.board[i, col - i - 1] for i in range(col)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1
        # tie
        if len(self.availablePositions()) == 0: # no available positions
            self.isEnd = True
            return 0
        # not end
        self.isEnd = False 
        return None
    
    def availablePositions(self):
        positions = []
        for i in range(row):
            for j in range(col):
                if self.board[i, j] == 0:
                    positions.append((i, j))  # need to be tuple
        return positions
    
    def updateState(self, position):
        self.board[position] = self.playerSymbol
        # switch to another player
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1
    
    # reset game
    def reset(self):
        self.board = np.zeros((row, col))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

class CollectiveLearning:
    def __init__(self, p1, p2, beta_reward = 0.5, beta_punishment = 0.5):
        self.p1 = p1
        self.p2 = p2
        self.STM = {}  # initialize STM
        self.LOG = []  # initialize LOG to store game history
        self.beta_reward = beta_reward
        self.beta_punishment = beta_punishment
    
    def updateSTM(self, LOG, outcome):
        # update probabilities based on game outcome
        for state, move in LOG: # loop through game history
            if state not in self.STM:
                self.STM[state] = np.random.rand(row, col)
            nplays = len(self.STM[state]) # number of possible plays
            
        # algedonic reward: increase possibility
        if outcome == 1:
            reward = self.beta_reward * (1 - self.STM[state][move])
            self.STM[state][move] += reward
            normal = reward / (nplays - 1)
            for j in range(len(self.STM[state])):
                if j != move and (self.STM[state][j] != 0).any():
                    self.STM[state][j] -= normal
                    
        # algedonic punishment: decrease possibility 
        else:
            punishment = self.beta_punishment/2 * self.STM[state][move]
            self.STM[state][move] -= punishment
            normal = punishment / (nplays - 1)
            for j in range(len(self.STM[state])):
                if j != move and (self.STM[state][j] != 0).any():
                    self.STM[state][j] += normal

    def selection(self, state):
        state_key = state.getHash() # hash containing current board state
        if state_key not in self.STM:
            self.STM[state_key] = np.random.rand(row, col) # initialize probabilities for new state
        probability = self.STM[state_key] # get probabilities for current state 
        available_positions = state.availablePositions() 
        
        # select move with highest probability
        probabilities = np.array([probability[pos] for pos in available_positions])
        max_prob = max(probabilities) # highest probability
        max_pos = [pos for pos in available_positions if probability[pos] == max_prob] # possible moves with highest probability
        return random.choice(max_pos)
    
    def train(self, epochs):
        for i in range(epochs):
            game = TicTacToe(self.p1, self.p2)
            # loop through game
            while not game.isEnd:
                move = self.selection(game)
                game.updateState(move)
                outcome = game.outcome()
                self.LOG.append((game.getHash(), move)) # update LOG with current play state
                self.updateSTM(self.LOG, outcome) # update STM with game history

if __name__ == "__main__":
    learner = CollectiveLearning("p1", "p2")
    learner.train(500)

