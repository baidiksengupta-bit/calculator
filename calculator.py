#!/usr/bin/env python3
"""
Interactive GUI Calculator (Tkinter)
-------------------------------------
A graphical, clickable calculator with basic + operations functions,
keyboard support, and a real-time expression display.
"""

import math
import tkinter as tk
from tkinter import font

# Safe namespace exposed to eval() — no builtins, only whitelisted math helpers
SAFE_FUNCS = {
    "sqrt": math.sqrt,
    "cbrt": lambda x: math.copysign(abs(x) ** (1 / 3), x),
    "log": math.log10,
    "ln": math.log,
    "exp": math.exp,
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "fact": lambda x: math.factorial(int(x)),
    "pi": math.pi,
    "e": math.e,
}


class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.expression = ""
        self.display_font = font.Font(size=26)
        self.button_font = font.Font(size=14)
        self.ops_font = font.Font(size=12)
        
        self.ops_visible = False  # Track visibility state of operations menu

        self._build_display()
        self._build_toggle_button()
        self._build_operations_row()
        self._build_buttons()
        self._bind_keys()
        
        # Apply initial visibility state
        self._toggle_operations(initial=True)

    # ---------- UI construction ----------
    def _build_display(self):
        self.display_var = tk.StringVar(value="0")
        display = tk.Entry(
            self.root,
            textvariable=self.display_var,
            font=self.display_font,
            bd=0,
            justify="right",
            bg="#1e1e2e",
            fg="white",
            insertbackground="white",
            state="readonly",
            readonlybackground="#1e1e2e",
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=(20, 10), ipady=18)

    def _build_toggle_button(self):
        self.toggle_btn = tk.Button(
            self.root,
            text="▼ Show Operations",
            font=self.ops_font,
            bd=0,
            bg="#313244",
            fg="#a6e3a1",
            activebackground="#585b70",
            activeforeground="#a6e3a1",
            command=self._toggle_operations,
        )
        self.toggle_btn.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=5, pady=(0, 5), ipady=5)

    def _build_operations_row(self):
        ops_buttons = [
            ("√", "sqrt("), ("∛", "cbrt("), ("x²", "**2"), ("xʸ", "**"),
            ("log", "log("), ("ln", "ln("), ("eˣ", "exp("),
            ("sin", "sin("), ("cos", "cos("), ("tan", "tan("),
            ("x!", "fact("), ("π", "pi"), ("e", "e"), ("(", "("), (")", ")"),
        ]
        self.ops_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.ops_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=5)

        for i, (label, insert_text) in enumerate(ops_buttons):
            btn = tk.Button(
                self.ops_frame,
                text=label,
                font=self.ops_font,
                bd=0,
                bg="#45475a",
                fg="white",
                activebackground="#585b70",
                command=lambda t=insert_text: self.append(t),
            )
            btn.grid(row=i // 5, column=i % 5, sticky="nsew", padx=3, pady=3, ipady=8)

        for c in range(5):
            self.ops_frame.grid_columnconfigure(c, weight=1)

    def _build_buttons(self):
        # Rows shifted down by 1 to accommodate toggle button and operations frame
        buttons = [
            ("C", 3, 0, "#f38ba8"), ("⌫", 3, 1, "#f38ba8"), ("%", 3, 2, "#f38ba8"), ("/", 3, 3, "#fab387"),
            ("7", 4, 0, "#313244"), ("8", 4, 1, "#313244"), ("9", 4, 2, "#313244"), ("*", 4, 3, "#fab387"),
            ("4", 5, 0, "#313244"), ("5", 5, 1, "#313244"), ("6", 5, 2, "#313244"), ("-", 5, 3, "#fab387"),
            ("1", 6, 0, "#313244"), ("2", 6, 1, "#313244"), ("3", 6, 2, "#313244"), ("+", 6, 3, "#fab387"),
            ("0", 7, 0, "#313244", 2), (".", 7, 2, "#313244"), ("=", 7, 3, "#a6e3a1"),
        ]

        for spec in buttons:
            if len(spec) == 5:
                text, row, col, color, colspan = spec
            else:
                text, row, col, color = spec
                colspan = 1

            btn = tk.Button(
                self.root,
                text=text,
                font=self.button_font,
                bd=0,
                bg=color,
                fg="black" if color in ("#a6e3a1", "#fab387", "#f38ba8") else "white",
                activebackground="#585b70",
                command=lambda t=text: self.on_button_click(t),
            )
            btn.grid(
                row=row, column=col, columnspan=colspan,
                sticky="nsew", padx=5, pady=5, ipady=15,
            )

        # Update row configurations to include the new rows
        for i in range(8):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def _bind_keys(self):
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<Return>", lambda e: self.evaluate())
        self.root.bind("<BackSpace>", lambda e: self.backspace())

    # ---------- Logic ----------
    def _toggle_operations(self, initial=False):
        if not initial:
            self.ops_visible = not self.ops_visible
            
        if self.ops_visible:
            self.ops_frame.grid()
            self.toggle_btn.config(text="▲ Hide Operations")
        else:
            self.ops_frame.grid_remove()  # Removes from view but remembers grid options
            self.toggle_btn.config(text="▼ Show Operations")

    def on_button_click(self, char):
        if char == "C":
            self.clear()
        elif char == "⌫":
            self.backspace()
        elif char == "=":
            self.evaluate()
        else:
            self.append(char)

    def on_key_press(self, event):
        char = event.char
        if char in "0123456789.+-*/%()":
            self.append(char)
        elif event.keysym == "Escape":
            self.clear()

    def append(self, text):
        self.expression += text
        self.update_display(self.expression)

    def clear(self):
        self.expression = ""
        self.update_display("0")

    def backspace(self):
        self.expression = self.expression[:-1]
        self.update_display(self.expression if self.expression else "0")

    def evaluate(self):
        if not self.expression:
            return
        try:
            allowed = set("0123456789.+-*/%() ") | set("".join(SAFE_FUNCS.keys()))
            if not set(self.expression) <= allowed:
                raise ValueError("Invalid characters")
            result = eval(self.expression, {"__builtins__": {}}, SAFE_FUNCS)
            self.update_display(str(result))
            self.expression = str(result)
        except ZeroDivisionError:
            self.update_display("Error: Div by 0")
            self.expression = ""
        except Exception:
            self.update_display("Error")
            self.expression = ""

    def update_display(self, text):
        self.display_var.set(text)


def main():
    root = tk.Tk()
    CalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
    