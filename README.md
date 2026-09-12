# Interactive GUI Calculator

A sleek, modern graphical calculator built using Python and Tkinter. It features a standard numeric keypad alongside a collapsible "Operations" menu for advanced mathematical functions, complete with full keyboard support and a dark-themed UI.

## Features

* **Standard Arithmetic:** Addition, subtraction, multiplication, division, and modulo.
* **Collapsible Operations Menu:** Toggle a drawer to access advanced functions without cluttering the main UI:
  * Trigonometry: `sin`, `cos`, `tan`
  * Logarithms: `log` (base 10), `ln` (natural log)
  * Exponents & Roots: `x²`, `xʸ`, `√`, `∛`, `eˣ`
  * Constants & Extras: `π`, `e`, factorials (`x!`)
* **Keyboard Integration:** 
  * Type numbers and operators directly.
  * Press `Enter` to evaluate.
  * Press `Backspace` to delete the last character.
  * Press `Escape` to clear the display.
* **Safe Evaluation:** Uses a strictly whitelisted namespace for the `eval()` function, preventing arbitrary code execution while allowing complex mathematical expressions.
* **Modern UI:** Features a custom dark color palette inspired by modern developer themes (like Catppuccin).

## Prerequisites

* **Python 3.x**
* **Tkinter** (This is usually included with standard Python installations by default)

## Installation & Usage

1. Clone this repository or download the source code file.
   ```bash
   git clone [https://github.com/yourusername/interactive-gui-calculator.git](https://github.com/baidiksengupta-bit/calculator.git)](https://github.com/yourusername/interactive-gui-calculator.git)
   cd interactive-gui-calculator
