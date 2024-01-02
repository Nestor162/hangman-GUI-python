# Hangman Game with Python and PySimpleGUI

This project implements a graphical version of the classic hangman game in Python using the PySimpleGUI library.

## Game Rules

- A random word is selected by the computer as the hidden target word
- The player guesses letters trying to reveal the target word
- If the player guesses a letter correctly, it is revealed in the word
- If the guess is incorrect, a body part is added to the hanging man
- The player has 6 incorrect guesses before the full hangman is drawn and the game ends
- If the player reveals the full word before 6 mistakes, they win

## Project Overview

### Gameplay demo

gameplay.gif

This project implements a hangman game in Python with a graphical interface using PySimpleGUI.

The code is organized into the following modules:

- **[hangman.py](https://github.com/Nestor162/hangman-GUI-python/blob/main/hangman.py)**: Main game class that handles game loop, GUI events and overall control flow
- **[game.py](https://github.com/Nestor162/hangman-GUI-python/blob/main/game.py)**: Contains Game class with game logic like selecting word, checking guesses, game state
- **[canvas.py](https://github.com/Nestor162/hangman-GUI-python/blob/main/canvas.py)**: Renders hangman figure and handles GUI display using PySimpleGUI

**Key features:**

- Graphical display of hangman figure, wrong guesses and revealed word
- Random word selection from a predefined list
- New game, restart and quit game options
- Keeping track of the player’s score through multiple rounds
- Modular design with separate classes for game logic and UI

## Getting Started

### Requirements

- Python 3.x
- PySimpleGUI

### Running the Game

1.  Clone the repository:
    `git clone https://github.com/your-username/hangman-game.git`
2.  Install the required dependencies:
    `pip install PySimpleGUI`
3.  Run the Hangman game:
    `python main.py`

## What I've Learned

- I've created a Graphical User Interface (GUI) using PySimpleGUI library
- I've implemented the Hangman Game Logic (word selection, input and results handling)
- I've connected the game logic to the GUI

## Future Improvements

Some potential enhancements for the future:

- **Specialized Word Lists:**
  - Add word lists of different categories
- **Difficulty Levels:**
  - Implement a system for classifying target words based on difficulty, considering factors like word length and popularity.
- **Multilingual Support:**
  - Introduce word lists in various languages, providing players with the opportunity to enhance language skills.
- **Sound Effects:**
  - Enhance user experience by integrating custom sound effects, emphasizing key actions within the game. Explore available Python options for playing sounds.
- **Keyboard Input:**
  - Enable keyboard input for a more interactive and intuitive gaming experience, allowing players to make guesses directly from the keyboard.
