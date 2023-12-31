import PySimpleGUI as sg
from string import ascii_uppercase


class Hangman:
    # Initializes the Hangman game window and stores it in the "window" variable
    def __init__(self):
        # Define the window layout
        self.layout = [
            [
                self._build_cavas_frame(),
                self._build_letters_frame(),
            ],
            [
                self._build_word_frame(),
            ],
            [
                self._build_action_buttons_frame(),
            ],
        ]
        self.window = sg.Window(
            title="Hangman",
            layout=self.layout,
            finalize=True,
        )

    def read_event(self):
        event = self.window.read()
        event_id = event[0] if event is not None else None
        return event_id

    def close_window(self):
        self.window.close()

    def _build_cavas_frame(self):
        """
        Builds the canvas frame that will display the hangman graphics.

        The Graph is given the key "-CANVAS-" so it can be updated dynamically.
        It is sized at 200x400 pixels and covers the area from (0,0) to (200, 400).
        """
        return sg.Frame(
            "Hangman",
            [
                [
                    sg.Graph(
                        key="-CANVAS-",
                        canvas_size=(200, 400),
                        graph_bottom_left=(0, 0),
                        graph_top_right=(200, 400),
                    )
                ]
            ],
            font="Any 20",
        )

    def _build_letters_frame(self):
        letter_groups = [
            ascii_uppercase[i : i + 4] for i in range(0, len(ascii_uppercase), 4)
        ]
        letter_buttons = [
            [
                sg.Button(
                    button_text=f"{letter} ",
                    font="Courier 20",
                    border_width=0,
                    button_color=(None, sg.theme_background_color()),
                    key=f"-letter-{letter}",
                    enable_events=True,
                )
                for letter in letter_groups
            ]
        ]

        return sg.Column(
            [
                [
                    sg.Frame(
                        "Letters",
                        letter_buttons,
                        font="Any 20",
                    ),
                    sg.Sizer(),
                ]
            ]
        )

    def _build_word_frame(self):
        # Builds the frame to display the word being guessed.
        return sg.Frame(
            "",
            [
                [
                    sg.Text(
                        key="-DISPLAY-WORD-",
                        font="Courier 20",
                    )
                ]
            ],
            element_justification="center",
        )

    def _build_action_buttons_frame(self):
        return sg.Frame(
            "",
            [
                [
                    sg.Sizer(h_pixels=90),
                    sg.Button(
                        button_text="New",
                        key="-NEW-",
                        font="Any 20",
                    ),
                    sg.Sizer(h_pixels=60),
                    sg.Button(
                        button_text="Restart",
                        key="-RESTART-",
                        font="Any 20",
                    ),
                    sg.Sizer(h_pixels=60),
                    sg.Button(
                        button_text="Quit",
                        key="-QUIT-",
                        font="Any 20",
                    ),
                    sg.Sizer(h_pixels=90),
                ]
            ],
        )


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
