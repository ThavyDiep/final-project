import tkinter as tk
from PIL import Image, ImageTk
import random

class MemoryMatchGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Match Game")
        self.moves = 0
        self.first_card = None
        self.matched_cards = set()
        self.images = self.load_images()
        self.placeholder = self.create_placeholder()  # Placeholder image
        self.card_values = self.generate_cards()
        self.buttons = [[None for _ in range(4)] for _ in range(4)]
        self.create_board()

    def load_images(self):
        # Load and resize images for the game
        fruit_names = ["img1.jpg", "img2.jpg", "img3.jpg", "img4.jpg", 
                       "img5.jpg", "img6.jpg", "img7.jpg", "img8.jpg"]
        images = []
        for fruit in fruit_names:
            img = Image.open(fruit).convert("RGB")  # Ensure image is in RGB mode
            img = img.resize((100, 100))  # Resize to 100x100 pixels
            images.append(ImageTk.PhotoImage(img))
        return images * 2  # Duplicate for pairs

    def create_placeholder(self):
        # Create a blank placeholder image with a solid background color (light gray)
        placeholder_img = Image.new("RGB", (100, 100), (200, 200, 200))  # Light gray background
        return ImageTk.PhotoImage(placeholder_img)

    def generate_cards(self):
        indices = list(range(16))  # 16 cards for a 4x4 grid
        random.shuffle(indices)
        return indices

    def create_board(self):
        for i in range(4):
            for j in range(4):
                btn = tk.Button(self.root, image=self.placeholder, 
                                command=lambda i=i, j=j: self.on_card_click(i, j))
                btn.grid(row=i, column=j, padx=5, pady=5)  # Add padding between buttons
                self.buttons[i][j] = btn

    def on_card_click(self, row, col):
        if (row, col) in self.matched_cards or self.buttons[row][col]["state"] == "disabled":
            return
        
        card_index = row * 4 + col
        image_index = self.card_values[card_index]
        self.buttons[row][col].config(image=self.images[image_index], state="disabled")
        
        if not self.first_card:
            self.first_card = (row, col)
        else:
            self.moves += 1
            first_row, first_col = self.first_card
            first_index = first_row * 4 + first_col
            #debug logging
            print(self.card_values)
            if self.card_values[first_index] == self.card_values[card_index]:
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
        self.buttons[row1][col1].config(image=self.placeholder, state="normal")
        self.buttons[row2][col2].config(image=self.placeholder, state="normal")

    def show_victory_message(self):
        victory_message = f"Congratulations! You won in {self.moves} moves."
        victory_label = tk.Label(self.root, text=victory_message, font=("Arial", 16))
        victory_label.grid(row=4, column=0, columnspan=4)

# Main application
root = tk.Tk()
game = MemoryMatchGame(root)
root.mainloop()



