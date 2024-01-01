import PySimpleGUI as sg
from canvas import Canvas
from game import Game as GameLogic


# This is the main class, which will be used to run the game and handle the events
class Hangman:
    def __init__(self):
        self.canvas = Canvas(self)
        self.game_logic = GameLogic(self.canvas, self)
        self.quit = False

    def read_event(self):
        event = self.canvas._window.read()
        event_id = event[0] if event is not None else None
        return event_id

    def process_event(self, event):
        if event[:8] == "-letter-":
            self.game_logic._play(letter=event[8])
        elif event == "-RESTART-":
            self.game_logic._restart_game()
        elif event == "-NEW-":
            self.game_logic._new_game()

    def close_window(self):
        self.canvas._window.close()


"""
This (if name == "main") is known as the "name-main idiom" in Python
The code inside this block will only run when file is executed directly, 
but not when imported as a module.
Useful to put initialization code that should run on start
"""

if __name__ == "__main__":
    # Main entry point for running the Hangman game.
    # The main loop repeatedly reads events from the user ( clicks, keypresses, etc) and breaks when the window is closed.
    game = Hangman()

    # The main loop
    # If the quit variable is True, exit the main loop and closes the window
    while not game.quit:
        # Executes this loop until the is_over method returns True
        while not game.game_logic.is_over():
            event_id = game.read_event()
            if event_id in {sg.WIN_CLOSED, "-QUIT-"}:
                game.quit = True
                break
            game.process_event(event_id)

        # If the game is over, check if the player won or lost
        if not game.quit:
            game.game_logic.check_winner()

    game.close_window()
