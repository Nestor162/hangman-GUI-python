import PySimpleGUI as sg
from string import ascii_uppercase


# This class is used to build the graphical user interface (GUI)
class Canvas:
    def __init__(self, hangman):
        self.hangman = hangman
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

        # Initializes the Hangman game window and stores it in the "window" variable
        self._window = sg.Window(
            title="Hangman",
            layout=self.layout,
            finalize=True,
        )

        # Stores the canvas in the "canvas" variable
        self._canvas = self._window["-CANVAS-"]

    # Methods to build and draw the graphycs
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

    def _draw_scaffold(self):
        lines = [
            ((40, 55), (180, 55), 10),
            ((165, 60), (165, 365), 10),
            ((160, 360), (100, 360), 10),
            ((100, 365), (100, 330), 10),
            ((100, 330), (100, 310), 1),
        ]
        for *points, width in lines:
            self._canvas.DrawLine(*points, color="black", width=width)

    def _draw_hanged_man(self):
        head = (100, 290)
        torso = [((100, 270), (100, 170))]
        left_arm = [
            ((100, 250), (80, 250)),
            ((80, 250), (60, 210)),
            ((60, 210), (60, 190)),
        ]
        right_arm = [
            ((100, 250), (120, 250)),
            ((120, 250), (140, 210)),
            ((140, 210), (140, 190)),
        ]
        left_leg = [
            ((100, 170), (80, 170)),
            ((80, 170), (70, 140)),
            ((70, 140), (70, 80)),
            ((70, 80), (60, 80)),
        ]
        right_leg = [
            ((100, 170), (120, 170)),
            ((120, 170), (130, 140)),
            ((130, 140), (130, 80)),
            ((130, 80), (140, 80)),
        ]
        body = [
            torso,
            left_arm,
            right_arm,
            left_leg,
            right_leg,
        ]
        if self.hangman.game_logic._wrong_guesses == 1:
            self._canvas.DrawCircle(
                head,
                20,
                line_color="red",
                line_width=2,
            )
        elif self.hangman.game_logic._wrong_guesses > 1:
            for part in body[self.hangman.game_logic._wrong_guesses - 2]:
                self._canvas.DrawLine(*part, color="red", width=2)

    def _build_letters_frame(self):
        letter_groups = [
            # Splits the uppercase ASCII letters into groups of 4 for
            # displaying as buttons on the hangman interface.
            ascii_uppercase[i : i + 4]
            for i in range(0, len(ascii_uppercase), 4)
        ]

        letter_buttons = [
            # Uses a nested list comprehension to generate a button for each letter
            # Results in a grid of letter buttons used to make guesses.
            [
                sg.Button(
                    button_text=f" {letter} ",
                    font="Courier 20",
                    border_width=0,
                    button_color=(None, sg.theme_background_color()),
                    key=f"-letter-{letter}-",
                    enable_events=True,
                )
                for letter in letter_group
            ]
            for letter_group in letter_groups
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
