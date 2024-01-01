import PySimpleGUI as sg
from random import choice
from string import ascii_uppercase

# The maximum number of wrong guesses allowed (number of parts of the hangman)
MAX_WRONG_GUESSES = 6


# This class contains the game logic
class Game:
    def __init__(self, canvas, hangman):
        self.canvas = canvas
        self.hangman = hangman
        self._new_game()
        self._played_games = 0
        self._won_games = 0

    def _select_word(self):
        # Selects a random word from the word list file to use as the target word.
        with open("words.txt", mode="r", encoding="utf-8") as words:
            word_list = words.readlines()
            return choice(word_list).strip().upper()

    def _build_guessed_word(self):
        # Builds the guessed word string to display.
        # For each letter in the target word,
        # Check if it is in the guessed letters.
        # If so, add the letter, otherwise add an underscore.
        # Join the list of letters/underscores into a space separated string.
        current_letters = []
        for letter in self._target_word:
            if letter in self._guessed_letters:
                current_letters.append(letter)
            else:
                current_letters.append("_")
        return " ".join(current_letters)

    def is_over(self):
        # Checks if the game is over by returning True if either:
        # - The number of wrong guesses equals the max allowed wrong guesses
        # - All letters of the target word have been guessed
        return any(
            [
                self._wrong_guesses == MAX_WRONG_GUESSES,
                set(self._target_word).issubset(self._guessed_letters),
            ]
        )

    def _play(self, letter):
        # Checks if the guessed letter is in the target word.
        # If the letter IS NOT in the word,
        # it increments the wrong guess count

        if letter not in self._target_word:
            self._wrong_guesses += 1

        # Otherwise, if the letter  IS in the target word,
        # it adds the letter to the guessed letters and
        # updates the guessed word.
        self._guessed_letters.add(letter)
        self._guessed_word = self._build_guessed_word()

        # Update GUI
        self.canvas._window[f"-letter-{letter}-"].update(disabled=True)
        self.canvas._window["-DISPLAY-WORD-"].update(self._guessed_word)
        self.canvas._draw_hanged_man()

    def _new_game(self):
        # Selects a new random word as the target word for the game
        # and resets the game state to start a new game
        self._target_word = self._select_word()
        self._restart_game()

    def _restart_game(self):
        # Restarts the game by resetting the game guessed letters, the mistakes and clearing the screen. The current word stays the same
        self._guessed_letters = set()
        self._wrong_guesses = 0
        self._guessed_word = self._build_guessed_word()

        # Redraw the GUI
        self.canvas._canvas.erase()
        self.canvas._draw_scaffold()
        for letter in ascii_uppercase:
            self.canvas._window[f"-letter-{letter}-"].update(disabled=False)
        self.canvas._window["-DISPLAY-WORD-"].update(self._guessed_word)

    def check_winner(self):
        self._played_games += 1
        if self._wrong_guesses < MAX_WRONG_GUESSES:
            self._won_games += 1
            answer = sg.PopupYesNo(
                "You've won! Congratulations!\n"
                f"That's {self._won_games} out of {self._played_games}!\n"
                "Another round?",
                title="Winner!",
            )
        else:
            answer = sg.PopupYesNo(
                f"You've lost! The word was '{self._target_word}'.\n"
                f"That's {self._won_games} out of {self._played_games}!\n"
                "Another round?",
                title="Sorry!",
            )
        self.hangman.quit = answer == "No"
        if not self.hangman.quit:
            self._new_game()
