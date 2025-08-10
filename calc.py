#CALCULATOR-MINI PROJECT-1
import tkinter as tk

# ----------------- Functions -----------------
def press(num):
    """Append number/operator to expression and update display."""
    global expression  
    expression += str(num)
    equation.set(expression)

def evaluate_expression(expr):
    """    Evaluate a numeric expression string safely. """
   
    # Evaluate and return string result
    # Keep floats trimmed (remove trailing .0)
    result = eval(expr)
    if isinstance(result, float):
        # Avoid long float representations
        result = round(result, 10)
        # Remove trailing zeros and possible trailing dot
        s = ('%f' % result).rstrip('0').rstrip('.')
        return s if s != '' else '0'
    return str(result)

def equalpress():
    """Validate and evaluate the expression, with specific error handling."""
    global expression
    try:
        # Allow only specific characters to reduce risk
        if expression.strip() == "":
            return
        allowed = set("0123456789+-*/(). ")
        if not all(ch in allowed for ch in expression):
            raise ValueError("Invalid character")

        # Prevent expressions that start/end with operators (simple guard)
        expr_stripped = expression.strip()
        if expr_stripped[0] in "+*/" or expr_stripped[-1] in "+-*/":
            raise SyntaxError("Incomplete expression")

        total = evaluate_expression(expression)
        equation.set(total)
        expression = total  # allow chaining
    except ZeroDivisionError:
        equation.set("Cannot divide by 0")
        expression = ""
    except (SyntaxError, ValueError):
        equation.set("Error")
        expression = ""

def clear():
    """Clear the display and reset expression."""
    global expression
    expression = ""
    equation.set("")

def backspace():
    """Remove last character from expression."""
    global expression
    expression = expression[:-1]
    equation.set(expression)

def key_press(event):
    """Map keyboard keys to behavior."""
    key = event.char
    # Numeric and operator characters
    if key in "0123456789+-*/().":
        press(key)
    elif key in ("\r", "\n"):  # Enter
        equalpress()
    elif key == "\x08":  # Backspace
        backspace()
    # allow Escape to clear
    elif event.keysym == "Escape":
        clear()

# ----------------- GUI Setup -----------------
window = tk.Tk()
window.title("Final Calculator")
window.geometry("360x480")
window.minsize(300, 420)
window.configure(bg="#121212")

expression = ""
equation = tk.StringVar()

for i in range(6):          # 0..5 rows (0 = display, 1-4 = buttons, 5 = wide controls)
    window.grid_rowconfigure(i, weight=1, uniform="row")
for j in range(4):          # 4 columns
    window.grid_columnconfigure(j, weight=1, uniform="col")

# Entry (display)
entry = tk.Entry(
    window, textvariable=equation, font=('Segoe UI', 28, 'bold'),
    bd=0, bg="#1e1e1e", fg="#ffffff", justify="right", insertbackground="white"
)
entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

# Buttons layout data
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3)
]

# Create buttons
for (text, row, col) in buttons:
    # Color design: operators in orange, equals in green-ish, others dark
    if text == "=":
        bg_color = "#7c27ae"
        fg_color = "#ffffff"
        cmd = equalpress
    elif text in "+-*/":
        bg_color = "#8212f3"
        fg_color = "#111111"
        cmd = lambda t=text: press(t)
    else:
        bg_color = "#2b2b2b"
        fg_color = "#ffffff"
        cmd = lambda t=text: press(t)

    btn = tk.Button(
        window, text=text, command=cmd,
        font=('Segoe UI', 18, 'bold'),
        bd=0, bg=bg_color, fg=fg_color, activebackground="#3a3a3a"
    )
    btn.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)

# Wide Clear and Backspace buttons in last row
tk.Button(window, text="C", command=clear,
          font=('Segoe UI', 16, 'bold'), bd=0, bg="#e74c3c", fg="white")\
    .grid(row=5, column=0, columnspan=2, sticky="nsew", padx=6, pady=6)

tk.Button(window, text="⌫", command=backspace,
          font=('Segoe UI', 16, 'bold'), bd=0, bg="#2980b9", fg="white")\
    .grid(row=5, column=2, columnspan=2, sticky="nsew", padx=6, pady=6)

# Keyboard bindings
window.bind("<Key>", key_press)

# Start with 0 shown
equation.set("0")
expression = ""

window.mainloop()
