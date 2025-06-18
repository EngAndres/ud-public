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

    def __init__(self):
        self.x_start = 150
        self.x_offset = 50

        # Draw the notes
        self.note_positions = {
            "C": 195,
            "D": 185,
            "E": 175,  # E on the bottom line
            "F": 165,
            "G": 155,  # G on the second line from the bottom
            "A": 145,
            "B": 135,  # B on the third line from the bottom
        }

        self._g_clef_image = None

    def compile(self, code: str):
        """This method compiles the code."""
        tokens_ = LexicalAnalyzer.lex(code)
        sintactic_analyzer = SintacticAnalyzer(tokens_)
        sintactic_analyzer.parse()
        semantic_analyzer_ = SemanticAnalyzer(tokens_)
        notes, time_signature = semantic_analyzer_.analyze()
        self.draw_pentagram(notes, time_signature)

    def _convert_to_num(self, duration: str) -> float:
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

    def _draw_lines(self, canvas: tk.Canvas):
        """Draws the five lines of the pentagram.

        Args:
            canvas (tk.Canvas): The canvas to draw the lines on.
        """
        for i in range(5):
            canvas.create_line(
                50, 100 + i * 20, 1175, 100 + i * 20, width=2, fill="light gray"
            )

    def _create_canvas_window(self, title: str, width: int, height: int):
        """Creates and returns a Tkinter root and canvas widget.

        Args:
            title (str): The title of the window.
            width (int): The width of the window.
            height (int): The height of the window.

        Returns:
            A tuple containing the root and canvas widgets.
        """
        root = tk.Tk()
        root.title(title)
        canvas = tk.Canvas(root, width=width, height=height, bg="white")
        canvas.pack()
        return root, canvas

    def _draw_clef(self, canvas: tk.Canvas):
        """Draws the G clef image on the canvas.

        Args:
            canvas (tk.Canvas): The canvas to draw the G clef on.
        """
        current_dir = os.getcwd()
        g_clef_image_path = os.path.join(current_dir, "img/g_clef.png")
        g_clef_image = tk.PhotoImage(file=g_clef_image_path)
        # Keep a reference so the image isn't garbage-collected.
        self._g_clef_image = g_clef_image
        canvas.create_image(10, 75, anchor=tk.NW, image=self._g_clef_image)

    def _draw_segment_lines(self, canvas: tk.Canvas, time_signature: str):
        """Draws the segment lines on the pentagram.

        Args:
            canvas (tk.Canvas): The canvas to draw the segment lines on.
        """

        distance = 256 * self._convert_to_num(time_signature)
        x = self.x_start
        for i in range(5):
            canvas.create_line(
                (x - 25) + (i * distance),
                100,
                (x - 25) + (i * distance),
                180,
                width=2,
                fill="light gray",
            )

    def _draw_time_signature(self, canvas: tk.Canvas, time_signature: str):
        """Draws the given time signature next to the clef."""
        # Position the time signature just to the right of the clef.
        # Adjust these x,y values as needed.
        clef_end_x = 100
        clef_y = 65
        canvas.create_text(
            clef_end_x, clef_y, text=time_signature, font=("Arial", 20, "bold")
        )

    def _draw_notes(self, canvas: tk.Canvas, notes: list):
        """Draws all notes with their accidentals and flags.

        Args:
            canvas (tk.Canvas): The canvas to draw the notes on.
            notes (list): The notes to draw.
        """
        x = self.x_start
        for note, duration in notes:
            note_name = note[0]
            note_alteration = note[1]
            octave = int(note[-1])
            y = self.note_positions[note_name] - (octave - 4) * 70

            # Draw accidental if needed.
            self._draw_accidental(canvas, x, y, note_alteration)

            # Draw note head, stem, and flags based on duration.
            self._draw_note_symbol(canvas, x, y, duration)
            x += int(256 * self._convert_to_num(duration))

    def _draw_accidental(self, canvas: tk.Canvas, x: int, y: int, alteration: str):
        """Draws sharp or flat symbol if required.

        Args:
            canvas (tk.Canvas): The canvas to draw the accidental on.
            x (int): The x-coordinate of the accidental.
            y (int): The y-coordinate of the accidental.
            alteration (str): The alteration to draw.
        """
        if alteration in ["s", "b"]:
            delta_alteration = 5
            symbol = "#" if alteration == "s" else "b"
            canvas.create_text(x - delta_alteration, y, text=symbol, font=("Arial", 11))

    def _draw_note_symbol(self, canvas: tk.Canvas, x: int, y: int, duration: str):
        """Draws the note head, stem and flags depending on the note's duration.

        Args:
            canvas (tk.Canvas): The canvas to draw the note symbol on.
            x (int): The x-coordinate of the note symbol.
            y (int): The y-coordinate of the note symbol.
            duration (str): The duration of the note
        """

        # Common parameters
        stem_height = 35
        delta = 1
        circle_size = 12
        x_delta = 10
        y_delta = 5
        line_vertical = 12

        if duration == "1":
            canvas.create_oval(x - 4, y - 3, x + 22, y + 16, fill="white", width=2)
        elif duration == "1/2":  # Half note: note head and stem only
            canvas.create_oval(
                x - delta,
                y - delta,
                x + circle_size,
                y + circle_size,
                fill="white",
                width=2,
            )
            canvas.create_line(
                x + line_vertical,
                y + y_delta,
                x + line_vertical,
                y - stem_height,
                width=2,
            )
        elif duration == "1/4":  # Quarter note: filled note head and stem only
            canvas.create_oval(
                x - delta, y - delta, x + circle_size, y + circle_size, fill="black"
            )
            canvas.create_line(x + 10, y + y_delta, x + 10, y - stem_height, width=2)
        elif duration == "1/8":  # Eighth note: filled head, stem and one flag.
            canvas.create_oval(
                x - delta, y - delta, x + circle_size, y + circle_size, fill="black"
            )
            canvas.create_line(x + 10, y + 5, x + 10, y - stem_height, width=2)
            canvas.create_line(
                x + 10, y - stem_height, x + 18, y - stem_height + 5, width=2
            )
        elif duration == "1/16":  # Sixteenth note: filled head, stem and two flags.
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

    def draw_pentagram(self, notes: list, time_signature: str):
        """Draws notes on a pentagram."""
        root, canvas = self._create_canvas_window("Pentagram Line Compiler", 1200, 300)
        self._draw_clef(canvas)
        self._draw_time_signature(canvas, time_signature)
        self._draw_lines(canvas)
        self._draw_segment_lines(canvas, time_signature)
        self._draw_notes(canvas, notes)
        root.mainloop()