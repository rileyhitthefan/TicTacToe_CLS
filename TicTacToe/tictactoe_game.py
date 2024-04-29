import tkinter as tk
from tkinter import messagebox
from tictactoe_cls import TicTacToe, CollectiveLearning

p1 = 'CLS'
p2 = 'Human'

class TicTacToeGame: 
    def __init__(self, master): 
        self.master = master 
        self.game = TicTacToe(p1, p2)
        self.cls = CollectiveLearning(p2, p1) # initalize ai player
        self.buttons = []
        self.create_board()
    
    def create_board(self):
        # create 3x3 board
        for i in range(3):
            row = []
            # create buttons
            for j in range(3):
                button = tk.Button(self.master, text=' ', width=10, height=5, command=lambda i=i, j=j: self.move(i, j))
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)
    
    def move(self, i, j):
        if not self.game.isEnd and self.game.board[i][j] == 0: 
            self.buttons[i][j].config(text='X') # human player: X
            self.game.updateState((i, j)) # update game state
            outcome = self.game.outcome() # update game outcome
            if outcome is None:
                move = self.cls.selection(self.game) # ai player
                self.buttons[move[0]][move[1]].config(text='O') # ai player: O
                self.game.updateState(move) # update game state
                outcome = self.game.outcome()
                if outcome is not None:
                    self.endGame(outcome) # determine game outcome
            if outcome is not None:
                self.endGame(outcome)
    
    def endGame(self, outcome):
        if outcome == 1:
            messagebox.showinfo('Game Over', 'You win!')
        elif outcome == -1:
            messagebox.showinfo('Game Over', 'AI wins!')
        else:
            messagebox.showinfo('Game Over', 'Tie!')
        self.reset_board()
        
    def reset_board(self):
        for row in self.buttons:
            for button in row:
                button.config(text='')
        self.game.reset()

def main():
    root = tk.Tk()
    root.title('Tic Tac Toe')
    game = TicTacToeGame(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()