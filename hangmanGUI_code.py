import string
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from hangman_code import HangmanGame  # Import the HangmanGame class

# Step 1: Set up the word list and initialize the game
word_list = ['python', 'hangman', 'challenge', 'computer', 'programming']
game = HangmanGame(word_list, max_attempts=6)  # Create a new Hangman game instance with a list of words and max attempts

def reset_game():
    """Reset the game state to start a new game."""
    global game
    game = HangmanGame(word_list, max_attempts=6)  # Reinitialize the game with a new word
    display_word.set(game.get_display_word())  # Update the display with the new word
    wrong_guesses_label.config(text="Wrong guesses: ")  # Clear the wrong guesses display
    hangman_label.config(text=f"Attempts left: {game.attempts_left()}")  # Reset the attempts left display
    update_hangman_image()  # Reset the hangman image to the initial state
    # Re-enable all the letter buttons for the new game
    for button in letter_buttons:
        button.config(state=tk.NORMAL)

def ask_replay():
    """Ask the player if they want to replay the game."""
    answer = messagebox.askyesno("Hangman", "Do you want to play again?")  # Display a message box asking if the player wants to play again
    if answer:
        reset_game()  # Restart the game if the player chooses 'Yes'
    else:
        window.quit()  # Close the game if the player chooses 'No'

def guess_letter(letter, button):
    """Process a guessed letter and update the game state."""
    result = game.guess(letter)  # Make a guess and get the result
    button.config(state=tk.DISABLED)  # Disable the button after it has been pressed

    # Update the display for the word and wrong guesses
    display_word.set(game.get_display_word())
    wrong_guesses_label.config(text="Wrong guesses: " + game.get_wrong_guesses())
    hangman_label.config(text=f"Attempts left: {game.attempts_left()}")  # Update the number of remaining attempts
    
    # Update the hangman image based on the number of wrong guesses
    update_hangman_image()

    # Check if the game is won or lost and prompt for replay
    if result == "win":
        messagebox.showinfo("Hangman", f"Congratulations! You guessed the word '{game.word}'!")  # Inform the player of their win
        ask_replay()  # Ask if the player wants to replay
    elif result == "lose":
        messagebox.showinfo("Hangman", f"Game over! The word was '{game.word}'.")  # Inform the player of their loss
        ask_replay()  # Ask if the player wants to replay

def update_hangman_image():
    """Update the hangman image based on the number of wrong guesses."""
    wrong_guesses_count = len(game.wrong_guesses)  # Get the number of wrong guesses
    max_images = 7  # Total number of hangman images

    # Determine the path of the image to display
    if wrong_guesses_count <= max_images:
        img_path = f"Images/P{wrong_guesses_count + 1}.jpg"  # Path to the current hangman image
    else:
        img_path = f"Images/P{max_images + 1}.jpg"  # Path to the final image if max attempts are exceeded

    try:
        # Load and resize the image
        img = Image.open(img_path)
        img = img.resize((150, 150), Image.LANCZOS)  # Resize the image to fit the label
        hangman_img = ImageTk.PhotoImage(img)
        hangman_image_label.config(image=hangman_img)  # Update the label with the new image
        hangman_image_label.image = hangman_img  # Keep a reference to avoid garbage collection
    except FileNotFoundError:
        print(f"Image file not found: {img_path}")  # Print an error message if the image file is missing

# Step 4: Initialize the GUI
def initialize_gui():
    global window, display_word, hangman_image_label, wrong_guesses_label, hangman_label, letter_buttons

    # Create the main window
    window = tk.Tk()  # Initialize the main Tkinter window
    window.title("Hangman Game")  # Set the window title

    # Create a label to display the word progress
    display_word = tk.StringVar()
    display_word.set(game.get_display_word())
    word_label = tk.Label(window, textvariable=display_word, font=("Helvetica", 20))
    word_label.pack(pady=10)  # Pack the label with some padding

    # Create a label to display the hangman image
    hangman_image_label = tk.Label(window)
    hangman_image_label.pack(pady=10)
    update_hangman_image()  # Display the initial hangman image

    # Create a label to display the remaining attempts
    hangman_label = tk.Label(window, text=f"Attempts left: {game.attempts_left()}", font=("Helvetica", 14))
    hangman_label.pack(pady=10)

    # Create a label to display wrong guesses
    wrong_guesses_label = tk.Label(window, text="Wrong guesses: ", font=("Helvetica", 14))
    wrong_guesses_label.pack(pady=10)

    # Create the buttons for each letter in the alphabet
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    letter_buttons = []  # List to store letter buttons
    for letter in string.ascii_lowercase:
        button = tk.Button(button_frame, text=letter.upper(), width=4, height=2, bg="#89CFF0", fg="white")
        button.config(command=lambda l=letter, b=button: guess_letter(l, b))  # Set the button command
        button.grid(row=(ord(letter) - 97) // 9, column=(ord(letter) - 97) % 9, padx=5, pady=5)  # Arrange buttons in grid
        letter_buttons.append(button)  # Add button to the list for later access

    window.mainloop()  # Start the Tkinter event loop

# Step 5: Set up the game and start the GUI
if __name__ == "__main__":
    initialize_gui()  # Initialize the GUI and start the application
