"""This module contains the Compiler class.

Author: Carlos Andres Sierra <cavirguezs@uditrital.edu.co>
"""

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
        root.title("Pentagram Line")
        canvas = tk.Canvas(root, width=800, height=400, bg='white')
        canvas.pack()

        # Draw the pentagram lines
        for i in range(5):
            canvas.create_line(50, 50 + i * 20, 750, 50 + i * 20, width=2)

        # Draw the notes
        note_positions = {
            'C': 130, 'D': 120, 'E': 110, 'F': 100, 'G': 90, 'A': 80, 'B': 70
        }
        x = 100
        for note, duration in notes:
            note_name = note[0]
            octave = int(note[1])
            y = note_positions[note_name] - (octave - 4) * 35
            canvas.create_oval(x, y, x + 10, y + 10, fill='black')
            if duration:
                canvas.create_text(x + 5, y + 20, text=duration, font=('Arial', 12))
            x += 40

        root.mainloop()
