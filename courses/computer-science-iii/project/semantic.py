import tkinter as tk
from lexical import lex
from sintactic import Parser

class SemanticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.notes = []

    def analyze(self):
        for token in self.tokens:
            if token.type == 'NOTE':
                self.notes.append((token.value, None))
            elif token.type == 'DURATION':
                if self.notes:
                    self.notes[-1] = (self.notes[-1][0], token.value)
        return self.notes

def draw_pentagram(notes):
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

# Example usage
input_text = """
START
C4 4 D4 4 E4 4 F4 4 G4 4 A4 4 B4 4 C4 4
END
"""

tokens = lex(input_text)
parser = Parser(tokens)
parser.parse()
semantic_analyzer = SemanticAnalyzer(tokens)
notes = semantic_analyzer.analyze()
draw_pentagram(notes)