import numpy as np
import tkinter as tk
from PIL import Image  # додано для збереження BMP

# --- Ініціалізація ---
matrix_size = int(input("Введіть розмір матриці(200x200, 500x500, 800х800 ....): "))
matrix = np.zeros((matrix_size, matrix_size), dtype=np.uint8)

if matrix_size >= 1000:
    cell_size = 1
elif matrix_size == 500:
    cell_size = 2
else:
    cell_size = 4

rules_variants = {
    1: ("labyrinth", {
        ("A", 0): (1, -1, "A"),
        ("A", 1): (2, -1, "A"),
        ("A", 2): (3, -1, "A"),
        ("A", 3): (4, -1, "A"),
        ("A", 4): (5, -1, "A"),
        ("A", 5): (6, 1, "B"),
        ("B", 0): (1, 1, "A"),
        ("B", 5): (6, -1, "B"),
        ("B", 6): (7, -1, "B"),
        ("B", 7): (8, -1, "B"),
        ("B", 8): (9, -1, "B"),
        ("B", 9): (10, -1, "B"),
        ("B", 10): (11, -1, "B"),
        ("B", 11): (12, -1, "B"),
        ("B", 12): (13, -1, "B"),
        ("B", 13): (14, -1, "B"),
        ("B", 14): (15, -1, "B"),
        ("B", 15): (0, -1, "B")
    }),
    2: ("island of failure", {
        ("A", 0): (1, -1, "B"),
        ("A", 1): (2, -1, "B"),
        ("A", 2): (3, -1, "B"),
        ("A", 3): (4, -1, "B"),
        ("A", 4): (5, 1, "B"),
        ("A", 5): (6, 1, "B"),
        ("A", 6): (7, 1, "B"),
        ("A", 7): (8, 1, "B"),
        ("A", 8): (9, -1, "B"),
        ("A", 9): (10, -1, "B"),
        ("A", 10): (11, -1, "B"),
        ("A", 11): (12, -1, "B"),
        ("A", 12): (13, 1, "B"),
        ("A", 13): (14, 1, "B"),
        ("A", 14): (15, 1, "B"),
        ("A", 15): (0, 1, "A"),
        ("B", 0): (1, 1, "B"),
        ("B", 1): (2, 1, "A"),
        ("B", 2): (3, 1, "A"),
        ("B", 3): (4, 1, "A"),
        ("B", 4): (5, -1, "A"),
        ("B", 5): (6, -1, "A"),
        ("B", 6): (7, -1, "A"),
        ("B", 7): (8, -1, "A"),
        ("B", 8): (9, 1, "A"),
        ("B", 9): (10, 1, "A"),
        ("B", 10): (11, 1, "A"),
        ("B", 11): (12, 1, "A"),
        ("B", 12): (13, -1, "A"),
        ("B", 13): (14, -1, "A"),
        ("B", 14): (15, -1, "A"),
        ("B", 15): (0, -1, "A")
    }),
    3: ("vane", {
        ("A", 0): (2, 0, "C"),
        ("A", 2): (0, 0, "B"),
        ("B", 2): (2, 1, "A"),
        ("B", 15): (2, 1, "A"),
        ("C", 2): (0, -1, "A"),
        ("C", 0): (15, -1, "A"),
        ("C", 15): (2, -1, "A")
    }),
    4: ("yellow square", {
        ("A", 0): (14, 0, "B"),
        ("B", 0): (14, 0, "C"),
        ("C", 0): (14, 0, "E"),
        ("E", 0): (14, 0, "F"),
        ("F", 0): (14, 0, "J"),
        ("J", 0): (13, -1, "A"),
        ("A", 14): (13, 0, "A"),
        ("A", 13): (14, 0, "A"),
        ("J", 14): (13, 0, "A"),
        ("J", 13): (14, 1, "A")
    })
}

rule = int(input("Введіть номер правила(1: 'лабіринт', 2: 'острів невдачі', 3: 'вертушка', 4: 'жовтий квадрат'):"))
rule_name, rules = rules_variants[rule]

# палітри
palettes = {
    1: {0: (255, 255, 255), 1: (0, 0, 0),
        2: (255, 0, 0), 3: (0, 255, 0), 4: (0, 0, 255),
        5: (255, 255, 0), 6: (255, 0, 255), 7: (0, 255, 255),
        8: (255, 128, 0), 9: (128, 0, 255), 10: (0, 128, 255),
        11: (128, 255, 0), 12: (255, 0, 128), 13: (0, 255, 128),
        14: (128, 128, 255), 15: (255, 128, 128)},
    2: {0: (255, 255, 255), 1: (0, 0, 0),
        2: (57, 255, 20), 3: (0, 255, 255), 4: (255, 20, 147),
        5: (255, 140, 0), 6: (0, 191, 255), 7: (255, 0, 255),
        8: (173, 255, 47), 9: (0, 255, 127), 10: (255, 105, 180),
        11: (255, 69, 0), 12: (30, 144, 255), 13: (199, 21, 133),
        14: (124, 252, 0), 15: (255, 215, 0)},
    3: {0: (255, 255, 255), 1: (0, 0, 0),
         2: (32, 32, 32), 3: (64, 64, 64), 4: (96, 96, 96),
         5: (128, 128, 128), 6: (160, 160, 160), 7: (192, 192, 192),
         8: (224, 224, 224), 9: (255, 0, 0), 10: (0, 255, 0),
         11: (0, 0, 255), 12: (255, 255, 0), 13: (0, 255, 255),
         14: (255, 0, 255), 15: (255, 128, 0)}
}

print("Виберіть палітру кольорів(1:Контрастні, 2:Неонові, 3:Монохром)")
palette_choice = int(input("Введіть номер палітри (1-3): "))
color_map = palettes.get(palette_choice, palettes[1])


# --- Клас Turmite ---
class Turmite:
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    def __init__(self, x, y, direction, state):
        self.x = x
        self.y = y
        self.direction = direction
        self.state = state
        self.history = []

    def step(self, matrix, rules):
        current_color = matrix[self.y, self.x]
        key = (self.state, current_color)
        if key in rules:
            self.history.append((self.x, self.y, self.direction, self.state, current_color))
            new_color, turn, new_state = rules[key]
            matrix[self.y, self.x] = new_color
            self.state = new_state
            self.direction = (self.direction + turn) % 4
            dx, dy = self.directions[self.direction]
            self.x = (self.x + dx) % matrix.shape[1]
            self.y = (self.y + dy) % matrix.shape[0]

    def undo(self, matrix):
        if self.history:
            x, y, old_direction, old_state, old_color = self.history.pop()
            matrix[y, x] = old_color
            self.x, self.y = x, y
            self.direction, self.state = old_direction, old_state


# --- GUI ---
turmite = Turmite(matrix_size // 2, matrix_size // 2, 0, "A")

root = tk.Tk()
root.title(f"Turmite Simulation ({rule_name})")

canvas = tk.Canvas(root, width=matrix_size*cell_size, height=matrix_size*cell_size)
canvas.pack()
frame = tk.Frame(root)
frame.pack()

# створюємо зображення з урахуванням масштабу
img = tk.PhotoImage(width=matrix_size*cell_size, height=matrix_size*cell_size)
canvas.create_image((0, 0), image=img, anchor="nw")

running = False

def draw_matrix():
    pixels = []
    for y in range(matrix_size):
        row = []
        for x in range(matrix_size):
            r, g, b = color_map[matrix[y, x]]
            row.append(f"#{r:02x}{g:02x}{b:02x}")
        row = sum([[c] * cell_size for c in row], [])
        line = " ".join(row)
        for _ in range(cell_size):
            pixels.append("{" + line + "}")
    img.put(" ".join(pixels))

def draw_cell(x, y, color_id):
    r, g, b = color_map[color_id]
    color = f"#{r:02x}{g:02x}{b:02x}"
    for dy in range(cell_size):
        for dx in range(cell_size):
            img.put(color, (x * cell_size + dx, y * cell_size + dy))

def run_steps():
    if running:
        old_x, old_y = turmite.x, turmite.y
        turmite.step(matrix, rules)
        draw_cell(old_x, old_y, matrix[old_y, old_x])
        label_count.config(text=str(len(turmite.history)))
        root.after(1, run_steps)

def run_limited_steps(steps_left):
    if steps_left > 0:
        old_x, old_y = turmite.x, turmite.y
        turmite.step(matrix, rules)
        draw_cell(old_x, old_y, matrix[old_y, old_x])
        label_count.config(text=str(len(turmite.history)))
        root.after(1, lambda: run_limited_steps(steps_left - 1))
    else:
        global running
        running = False

def start_simulation():
    global running
    running = True
    steps_input = entry_ops.get().strip()
    if steps_input:
        try:
            steps = int(steps_input)
            if steps > 0:
                run_limited_steps(steps)
            else:
                running = False
        except ValueError:
            running = False
    else:
        run_steps()

def stop_simulation():
    global running
    running = False

def step_once():
    old_x, old_y = turmite.x, turmite.y
    turmite.step(matrix, rules)
    draw_cell(old_x, old_y, matrix[old_y, old_x])
    label_count.config(text=str(len(turmite.history)))

def undo_step():
    if turmite.history:
        x, y, _, _, old_color = turmite.history[-1]
        turmite.undo(matrix)
        draw_cell(x, y, old_color)
        label_count.config(text=str(len(turmite.history)))

def save_bmp():
    img_pil = Image.new("RGB", (matrix_size, matrix_size))
    for y in range(matrix_size):
        for x in range(matrix_size):
            img_pil.putpixel((x, y), color_map[matrix[y, x]])
    img_pil = img_pil.resize((matrix_size*cell_size, matrix_size*cell_size), Image.NEAREST)
    img_pil.save("turmite.bmp")
    print("Saved as turmite.bmp")


# --- Кнопки ---
start_button = tk.Button(frame, text="Start", command=start_simulation)
start_button.pack(side="left")
stop_button = tk.Button(frame, text="Stop", command=stop_simulation)
stop_button.pack(side="left")
step_button = tk.Button(frame, text="→", command=step_once)
step_button.pack(side="left")
undo_button = tk.Button(frame, text="←", command=undo_step)
undo_button.pack(side="left")
save_button = tk.Button(frame, text="Save BMP", command=save_bmp)
save_button.pack(side="left")
entry_ops = tk.Entry(frame, width=5)
entry_ops.pack(side="left")
label_count = tk.Label(frame, text="0")
label_count.pack(side="left")

draw_matrix()
root.mainloop()
