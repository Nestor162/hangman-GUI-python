import PySimpleGUI as sg


class Hangman:
    # Initializes the Hangman game window and stores it in the "window" variable
    def __init__(self):
        self.window = sg.Window(
            title="Hangman",
            layout=[[]],
            finalize=True,
            margins=(100, 100),
        )

    def read_event(self):
        event = self.window.read()
        event_id = event[0] if event is not None else None
        return event_id

    def close_window(self):
        self.window.close()


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
    while True:
        event_id = game.read_event()
        if event_id in {sg.WIN_CLOSED}:
            break
    game.close_window()
