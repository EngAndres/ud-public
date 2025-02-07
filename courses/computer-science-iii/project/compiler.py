"""This module contains the Compiler class.

Author: Carlos Andres Sierra <cavirguezs@uditrital.edu.co>
"""

import os
import tkinter as tk

from lexical import LexicalAnalyzer
from sintactic import SintacticAnalyzer
from semantic import SemanticAnalyzer


class Compiler:
    """This class represents the behavior of a complete compiler."""

    def compile(self, code: str):
        """This method compiles the code."""
        tokens_ = LexicalAnalyzer.lex(code)
        sintactic_analyzer = SintacticAnalyzer(tokens_)
        sintactic_analyzer.parse()
        semantic_analyzer_ = SemanticAnalyzer(tokens_)
        notes = semantic_analyzer_.analyze()
        self.draw_pentagram(notes)

    def draw_pentagram(self, notes: list):
        """This method draws the notes on a pentagram.

        Args:
            notes (list): A list of tuples with notes and durations.
        """
        root = tk.Tk()
        root.title("Pentagram Line Compiler")
        canvas = tk.Canvas(root, width=1200, height=300, bg="white")
        canvas.pack()

        # Draw the G clef image
        current_dir = os.getcwd()
        g_clef_image_path = os.path.join(current_dir, "img/g_clef.png")
        g_clef_image = tk.PhotoImage(file=g_clef_image_path)
        canvas.create_image(10, 75, anchor=tk.NW, image=g_clef_image)

        x = 150
        
        # Draw the pentagram lines
        for i in range(5):
            canvas.create_line(
                50, 100 + i * 20, 1000, 100 + i * 20, width=2, fill="light gray"
            )

        # draw segment lines
        for i in range(5):
            canvas.create_line(
                (x - 25) + (i * 256), 100, (x - 25) + (i * 256), 180, width=2, fill="light gray"
            )

        # Draw the notes
        note_positions = {
            "C": 195,
            "D": 185,
            "E": 175,  # E on the bottom line
            "F": 165,
            "G": 155,  # G on the second line from the bottom
            "A": 145,
            "B": 135,  # B on the third line from the bottom
        }

        for note, duration in notes:
            note_name = note[0]
            note_alteration = note[1]
            octave = int(note[-1])
            y = note_positions[note_name] - (octave - 4) * 70

            # Add sharp (#) or flat (b) symbol if applicable
            if note_alteration in ["s", "b"]:
                delta_alteration = 5
                if note_alteration == "s":
                    canvas.create_text(
                        x - delta_alteration, y, text="#", font=("Arial", 11)
                    )
                elif note_alteration == "b":
                    canvas.create_text(
                        x - delta_alteration, y, text="b", font=("Arial", 11)
                    )

            # Draw the note stem and flags based on duration
            stem_height = 35
            delta = 1
            circle_size = 12
            x_delta = 10
            y_delta = 5
            if duration == "1":
                canvas.create_oval(x - 4, y - 3, x + 22, y + 16, fill="white", width=2)
            elif duration == "1/2":  # Half note (stem only)
                canvas.create_oval(
                    x - delta,
                    y - delta,
                    x + circle_size,
                    y + circle_size,
                    fill="white",
                    width=2,
                )
                canvas.create_line(x + 12, y + 5, x + 12, y - stem_height, width=2)
            elif duration == "1/4":  # Quarter note (stem only)
                canvas.create_oval(
                    x - delta, y - delta, x + circle_size, y + circle_size, fill="black"
                )
                canvas.create_line(x + 10, y + 5, x + 10, y - stem_height, width=2)
            elif duration == "1/8":
                # Eighth note (stem and one flag)
                canvas.create_oval(
                    x - delta, y - delta, x + circle_size, y + circle_size, fill="black"
                )
                canvas.create_line(x + 10, y + 5, x + 10, y - stem_height, width=2)
                canvas.create_line(
                    x + 10, y - stem_height, x + 18, y - stem_height + 5, width=2
                )
            elif duration == "1/16":
                # Sixteenth note (stem and two flags)
                canvas.create_oval(
                    x - delta, y - delta, x + circle_size, y + circle_size, fill="black"
                )
                canvas.create_line(
                    x + x_delta, y + y_delta, x + x_delta, y - stem_height, width=2
                )
                canvas.create_line(
                    x + x_delta,
                    y - stem_height,
                    x + x_delta * 1.8,
                    y - stem_height + y_delta,
                    width=2,
                )
                canvas.create_line(
                    x + x_delta,
                    y - stem_height + y_delta,
                    x + x_delta * 1.8,
                    y - stem_height + y_delta * 2,
                    width=2,
                )

            x += int(256 * self.__convert_to_num(duration))

        root.mainloop()

    def __convert_to_num(self, duration: str) -> float:
        """This method converts a duration to a number.

        Args:
            duration (str): The duration to convert.

        Returns:
            float: The duration as a number.
        """
        components = duration.split("/")
        upper = int(duration.split("/")[0])
        lower = 1
        if len(components) > 1:
            lower = int(duration.split("/")[1])
        return upper / lower
