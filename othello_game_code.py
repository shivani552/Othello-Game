import tkinter as tk
from tkinter import messagebox
import pygame

# Initialize the Pygame mixer once at the start
pygame.mixer.init()

# Load sound files
flip_sound = pygame.mixer.Sound("flip.wav")  # Change "flip_sound.wav" to your flip sound file

# Function to play flip sound
def play_flip_sound():
    flip_sound.play()

# First window
root = tk.Tk()
root.title("menu")
root.state('zoomed')  # Maximize the first window

# Define constants for players
BLACK = 0
WHITE = 1

# Initialize player images
player_images = [
    tk.PhotoImage(file="black_disc.png"),  # Change "black_piece.png" to the image file for the black piece
    tk.PhotoImage(file="white_disc.png")   # Change "white_piece.png" to the image file for the white piece
]

# Initialize game board state (8x8 grid with None for empty, 0 for black, 1 for white)
board_state = [[None for _ in range(8)] for _ in range(8)]

# Set the starting player (0 for black, 1 for white)
current_player = BLACK

def start_next_window():
    root.withdraw()  # Hide the current window
    next_window.state('zoomed')  # Maximize the next window

def exit_program():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()

def play_song1():
    try:
        pygame.mixer.music.load("Sakura sound.mp3")  # Change to your song file
        pygame.mixer.music.play()
    except pygame.error as e:
        messagebox.showerror("Error", f"Unable to play the song: {e}")

def play_song2():
    try:
        pygame.mixer.music.load("epic sound.mp3")  # Change to your song file
        pygame.mixer.music.play()
    except pygame.error as e:
        messagebox.showerror("Error", f"Unable to play the song: {e}")

def stop_song():
    pygame.mixer.music.stop()

def go_back():
    next_window.withdraw()  # Hide the current window
    root.state('zoomed')  # Maximize the first window
    root.deiconify()  # Show the first window

def start_third_window():
    next_window.withdraw()  # Hide the current window
    third_window.state('zoomed')  # Maximize the third window

def open_tutorial():
    tutorial_window.state('zoomed')  # Maximize the tutorial window
    tutorial_window.deiconify()  # Show the tutorial window

def close_tutorial():
    tutorial_window.withdraw()  # Hide the tutorial window
    root.state('zoomed')  # Maximize the first window
    root.deiconify()  # Show the first window

def is_valid_move(row, col, player):
    if board_state[row][col] is None:
        return True

    opponent = 1 - player
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    valid = False

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if r < 0 or r >= 8 or c < 0 or c >= 8 or board_state[r][c] != opponent:
            continue
        while 0 <= r < 8 and 0 <= c < 8:
            if board_state[r][c] == player:
                valid = True
                break
            elif board_state[r][c] is None:
                break
            r += dr
            c += dc
        if valid:
            break
    
    return valid

def apply_move(row, col, player):
    opponent = 1 - player
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    to_flip = []

    for dr, dc in directions:
        r, c = row + dr, col + dc
        potential_flips = []
        while 0 <= r < 8 and 0 <= c < 8:
            if board_state[r][c] == opponent:
                potential_flips.append((r, c))
            elif board_state[r][c] == player:
                to_flip.extend(potential_flips)
                break
            else:
                break
            r += dr
            c += dc

    for r, c in to_flip:
        board_state[r][c] = player

    board_state[row][col] = player

    if to_flip:
        play_flip_sound()  # Play flip sound when flips occur

    return to_flip

def count_cells():
    black_count = sum(row.count(BLACK) for row in board_state)
    white_count = sum(row.count(WHITE) for row in board_state)
    return black_count, white_count

# Load sound files
winner_sound = pygame.mixer.Sound("winner.wav")  # Change "winner_sound.wav" to your sound file

# Function to play winner sound
def play_winner_sound():
    winner_sound.play()

def display_bravo():
    bravo_window = tk.Toplevel(root)
    bravo_window.title("Bravo!")
    bravo_window.state('zoomed')  # Maximize the window

    # Add background image
    bravo_bg_image = tk.PhotoImage(file="winner-background.png")  # Change to your image file
    bravo_bg_label = tk.Label(bravo_window, image=bravo_bg_image)
    bravo_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bravo_bg_label.image = bravo_bg_image  # Keep a reference to avoid garbage collection
    
    bravo_label = tk.Label(bravo_window, text="Bravo!", font=("Arial", 40), bg='light yellow')
    bravo_label.place(relx=0.5, rely=0.5, anchor='center')



def declare_winner():
    black_count, white_count = count_cells()
    if black_count > white_count:
        winner = "Black"
    elif white_count > black_count:
        winner = "White"
    else:
        winner = "It's a tie!"

    winner_window = tk.Toplevel(root)
    winner_window.title("Winner")
    winner_window.state('zoomed')  # Maximize the window

    # Add background image
    winner_bg_image = tk.PhotoImage(file="winner-background.png")  # Change to your image file
    winner_bg_label = tk.Label(winner_window, image=winner_bg_image)
    winner_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    winner_bg_label.image = winner_bg_image  # Keep a reference to avoid garbage collection

    winner_label = tk.Label(winner_window, text=f"The winner is {winner}!", font=("Arial", 40), bg='light yellow')
    winner_label.place(relx=0.5, rely=0.5, anchor='center')

    play_winner_sound()  # Play winner sound
    display_bravo()  # Show "Bravo" after declaring the winner

def on_cell_click(event):
    global current_player, player_images

    widget = event.widget
    row = widget.grid_info()['row']
    col = widget.grid_info()['column']

    # Check if the clicked cell is empty
    if board_state[row][col] is not None:
        messagebox.showinfo("Invalid Move", "This cell is not empty!")
        return

    if not is_valid_move(row, col, current_player):
        messagebox.showinfo("Invalid Move", "This move is not valid!")
        return

    # Apply the move and flip the discs
    flipped_discs = apply_move(row, col, current_player)

    # Display the current player's image on the clicked cell
    current_image = player_images[current_player]
    widget.image = current_image  # Keep a reference to avoid garbage collection
    image_label = tk.Label(widget, image=current_image)
    image_label.place(relwidth=1, relheight=1)

    # Display the flipped discs
    for r, c in flipped_discs:
        cell = grid_frame.grid_slaves(row=r, column=c)[0]
        cell.image = current_image
        flip_label = tk.Label(cell, image=current_image)
        flip_label.place(relwidth=1, relheight=1)

    # Update player move counts
    update_move_counts()

    def is_game_over():
        return not any(is_valid_move(row, col, current_player) for row in range(8) for col in range(8)) and \
           not any(is_valid_move(row, col, 1 - current_player) for row in range(8) for col in range(8))

    if all(cell is not None for row in board_state for cell in row) or is_game_over():
        declare_winner()
    else:
        # Switch to the next player
        current_player = 1 - current_player

# Background image
bg_image = tk.PhotoImage(file="green-board.png")  # Change to your image file
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Welcome message
welcome_label = tk.Label(root, text="Welcome to Othello!", font=("Arial", 30), bg='light yellow')
welcome_label.place(relx=0.5, rely=0.3, anchor='center')  # Adjusted position higher

# Buttons for first window
tutorial_button = tk.Button(root, text="Tutorial", command=open_tutorial, font=("Arial", 16), bg='light blue')
tutorial_button.place(relx=0.02, rely=0.02, relwidth=0.2, relheight=0.1)

start_button = tk.Button(root, text="Start", command=start_next_window, font=("Arial", 16), bg='light green')
start_button.place(relx=0.4, rely=0.6, relwidth=0.2, relheight=0.1)

exit_button = tk.Button(root, text="Exit", command=exit_program, font=("Arial", 16), bg='light coral')
exit_button.place(relx=0.78, rely=0.85, relwidth=0.2, relheight=0.1)

# Second window
next_window = tk.Toplevel(root)
next_window.title("sound settings")
next_window.geometry("800x600")
next_window.state('zoomed')  # Maximize the second window
next_window.withdraw()  # Hide the second window initially

# Background image for second window
bg_label2 = tk.Label(next_window, image=bg_image)
bg_label2.place(relwidth=1, relheight=1)

# Buttons for second window
song1_button = tk.Button(next_window, text="Play Song 1", command=play_song1, font=("Arial", 30), bg='light blue')
song1_button.place(relx=0.5, rely=0.3, anchor='center')

song2_button = tk.Button(next_window, text="Play Song 2", command=play_song2, font=("Arial", 30), bg='light blue')
song2_button.place(relx=0.5, rely=0.5, anchor='center')

stop_button = tk.Button(next_window, text="no Song", command=stop_song, font=("Arial", 30), bg='light coral')
stop_button.place(relx=0.5, rely=0.7, anchor='center')

back_button = tk.Button(next_window, text="Back", command=go_back, font=("Arial", 16), bg='light coral')
back_button.place(relx=0.02, rely=0.85, relwidth=0.2, relheight=0.1)

start_game_button = tk.Button(next_window, text="Start Game", command=start_third_window, font=("Arial", 16), bg='light green')
start_game_button.place(relx=0.78, rely=0.85, relwidth=0.2, relheight=0.1)

# Third window
third_window = tk.Toplevel(root)
third_window.title("Online Game")
third_window.geometry("800x600")
third_window.state('zoomed')  # Maximize the third window
third_window.withdraw()  # Hide the third window initially

# Player move counts
black_moves_label = tk.Label(third_window, text="Black Moves: 0", font=("Arial", 30), bg='light yellow')
black_moves_label.place(relx=0.05, rely=0.1)

white_moves_label = tk.Label(third_window, text="White Moves: 0", font=("Arial", 30), bg='light yellow')
white_moves_label.place(relx=0.05, rely=0.2)

black_move_count = 0
white_move_count = 0

def update_move_counts():
    global black_move_count, white_move_count
    black_move_count, white_move_count = count_cells()
    black_moves_label.config(text=f"Black Moves: {black_move_count}")
    white_moves_label.config(text=f"White Moves: {white_move_count}")

# Create grid in third window
def create_grid():
    global grid_frame
    grid_frame = tk.Frame(third_window, bg='light yellow')
    grid_frame.place(relx=0.45, rely=0.1, relwidth=0.5, relheight=0.8)
    for row in range(8):
        for col in range(8):
            cell = tk.Frame(grid_frame, bg='green', highlightbackground='black', highlightthickness=1)
            cell.grid(row=row, column=col, sticky='nsew')
            cell.bind("<Button-1>", on_cell_click)  # Bind left-click event to each cell
    for i in range(8):
        grid_frame.grid_columnconfigure(i, weight=1)
        grid_frame.grid_rowconfigure(i, weight=1)

create_grid()  # Call the function to create the grid

# Tutorial window
tutorial_window = tk.Toplevel(root)
tutorial_window.title("Tutorial")
tutorial_window.geometry("800x600")
tutorial_window.state('zoomed')  # Maximize the tutorial window
tutorial_window.withdraw()  # Hide the tutorial window initially

# Add content to the tutorial window
tutorial_text = (
    "1. Black always moves first.\n\n"
    "2. If on your turn you cannot outflank and flip at least one opposing disc, your turn is forfeited and your opponent moves again. However, if a move is available to you, you may not forfeit your turn.\n\n"
    "3. Players may not skip over their own color disc(s) to outflank an opposing disc.\n\n"
    "4. Disc(s) may only be outflanked as a direct result of a move and must fall in the direct line of the disc placed down.\n\n"
    "5. All discs outflanked in any one move must be flipped, even if it is to the player's advantage not to flip them at all.\n\n"
    "6. Once a disc is placed on a square, it can never be moved to another square later in the game.\n\n"
    "7. When it is no longer possible for either player to move, the game is over. Discs are counted and the player with the majority of their color showing is the winner.\n\n"
    "Note: It is possible for a game to end before all 64 squares are filled."
)

tutorial_label = tk.Label(tutorial_window, text=tutorial_text, font=("Arial", 16), bg='light green', justify='left', anchor='nw')
tutorial_label.pack(expand=True, fill='both', padx=20, pady=20)

close_tutorial_button = tk.Button(tutorial_window, text="Close", command=close_tutorial, font=("Arial", 16), bg='light coral')
close_tutorial_button.pack(side="bottom", pady=20)

root.mainloop()


