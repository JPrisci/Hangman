import random

class HangmanGame:
    def __init__(self, word_list, max_attempts=6):
        """
        Initialize the HangmanGame with a list of words and a maximum number of attempts.
        Chooses a random word from the list and sets up the game state with guessed letters and wrong guesses.
        """
        self.word_list = word_list  # List of potential words for the game
        self.max_attempts = max_attempts  # Maximum allowed wrong guesses before game over
        self.word = random.choice(self.word_list).lower()  # Randomly select a word from the list and convert to lowercase
        self.guessed_letters = []  # List to track correctly guessed letters
        self.wrong_guesses = []  # List to track incorrectly guessed letters
        print(f"Initialized game with word: {self.word}")  # Debugging: Output the selected word for verification

    def get_display_word(self):
        """
        Return the current state of the word being guessed.
        Correctly guessed letters are shown, and missing letters are represented by underscores.
        """
        # List comprehension to display guessed letters and underscores for unguessed ones
        return ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.word])

    def guess(self, letter):
        """
        Process a guessed letter.
        Update the game state based on whether the letter is in the word or not.
        Return 'win' if the player has guessed the word, 'lose' if they've run out of attempts,
        'correct' if the guess is right, and 'incorrect' if it's wrong.
        """
        # Ignore the guess if the letter has already been guessed (correct or incorrect)
        if letter in self.guessed_letters or letter in self.wrong_guesses:
            return "continue"  # Continue the game if the letter was already guessed
        
        # Check if the guessed letter is in the word
        if letter in self.word:
            self.guessed_letters.append(letter)  # Add the letter to guessed letters
            # Check if the player has won by guessing all letters in the word
            if all(letter in self.guessed_letters for letter in self.word):
                return "win"
            return "correct"
        else:
            # If the letter is not in the word, add it to wrong guesses
            self.wrong_guesses.append(letter)
            # Check if the player has used all their attempts and lost the game
            if len(self.wrong_guesses) >= self.max_attempts:
                return "lose"
            return "incorrect"

    def get_wrong_guesses(self):
        """
        Return a string of all wrong guesses made by the player, separated by commas.
        """
        return ', '.join(self.wrong_guesses)  # Join wrong guesses into a single string

    def attempts_left(self):
        """
        Return the number of attempts the player has left before they lose.
        This is calculated as the maximum allowed attempts minus the number of wrong guesses made.
        """
        return self.max_attempts - len(self.wrong_guesses)
