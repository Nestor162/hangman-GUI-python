import PySimpleGUI as sg
from string import ascii_uppercase
from random import choice


MAX_WRONG_GUESSES = 6


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

        self._window = sg.Window(
            title="Hangman",
            layout=self.layout,
            finalize=True,
        )

        self._canvas = self._window["-CANVAS-"]

        self._new_game()

        self.quit = False

    def read_event(self):
        event = self._window.read()
        event_id = event[0] if event is not None else None
        return event_id

    def process_event(self, event):
        if event[:8] == "-letter-":
            self._play(letter=event[8])
        elif event == "-RESTART-":
            self._restart_game()
        elif event == "-NEW-":
            self._new_game()

    def close_window(self):
        self._window.close()

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
        if self._wrong_guesses == 1:
            self._canvas.DrawCircle(
                head,
                20,
                line_color="red",
                line_width=2,
            )
        elif self._wrong_guesses > 1:
            for part in body[self._wrong_guesses - 2]:
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

    # Methods that define the game logic
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
        self._window[f"-letter-{letter}-"].update(disabled=True)
        self._window["-DISPLAY-WORD-"].update(self._guessed_word)
        self._draw_hanged_man()

    def _select_word(self):
        # Selects a random word from the word list file to use as the target word.
        with open("words.txt", mode="r", encoding="utf-8") as words:
            word_list = words.readlines()
        return choice(word_list).strip().upper()

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
        self._canvas.erase()
        self._draw_scaffold()
        for letter in ascii_uppercase:
            self._window[f"-letter-{letter}-"].update(disabled=False)
        self._window["-DISPLAY-WORD-"].update(self._guessed_word)

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

    def check_winner(self):
        if self._wrong_guesses < MAX_WRONG_GUESSES:
            answer = sg.PopupYesNo(
                "You've won! Congratulations!\n" "Another round?",
                title="Winner!",
            )
        else:
            answer = sg.PopupYesNo(
                f"You've lost! The word was '{self._target_word}'.\n" "Another round?",
                title="Sorry!",
            )
        self.quit = answer == "No"
        if not self.quit:
            self._new_game()


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
        while not game.is_over():
            event_id = game.read_event()
            if event_id in {sg.WIN_CLOSED, "-QUIT-"}:
                game.quit = True
                break
            game.process_event(event_id)

        # If the game is over, check if the player won or lost
        if not game.quit:
            game.check_winner()

    game.close_window()
