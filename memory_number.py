import tkinter as tk
import random
import time

class MemoryMatchGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Match Game")
        self.moves = 0
        self.first_card = None
        self.matched_cards = set()
        self.card_values = self.generate_cards()
        self.buttons = [[None for _ in range(4)] for _ in range(4)]
        self.create_board()

    def generate_cards(self):
        values = list(range(1, 9)) * 2  # 8 pairs of numbers for a 4x4 grid
        random.shuffle(values)
        return values

    def create_board(self):
        for i in range(4):
            for j in range(4):
                btn = tk.Button(self.root, text="", width=8, height=4, 
                                command=lambda i=i, j=j: self.on_card_click(i, j))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def on_card_click(self, row, col):
        if (row, col) in self.matched_cards or self.buttons[row][col]["state"] == "disabled":
            return
        
        card_index = row * 4 + col
        self.buttons[row][col].config(text=str(self.card_values[card_index]), state="disabled")
        
        if not self.first_card:
            self.first_card = (row, col)
        else:
            self.moves += 1
            first_row, first_col = self.first_card
            if self.card_values[first_row * 4 + first_col] == self.card_values[card_index]:
                # It's a match!
                self.matched_cards.add((row, col))
                self.matched_cards.add((first_row, first_col))
                if len(self.matched_cards) == 16:
                    self.show_victory_message()
            else:
                # Not a match; reset after a short delay
                self.root.after(500, lambda: self.reset_cards(row, col, first_row, first_col))
            self.first_card = None

    def reset_cards(self, row1, col1, row2, col2):
        self.buttons[row1][col1].config(text="", state="normal")
        self.buttons[row2][col2].config(text="", state="normal")

    def show_victory_message(self):
        victory_message = f"Congratulations! You won in {self.moves} moves."
        victory_label = tk.Label(self.root, text=victory_message, font=("Arial", 16))
        victory_label.grid(row=4, column=0, columnspan=4)

# Main application
root = tk.Tk()
game = MemoryMatchGame(root)
root.mainloop()



