import tkinter as tk
import random
import math

WIDTH, HEIGHT = 500, 500
CELL = 20
DELAY = 130

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg="#1a3a1a", highlightthickness=0)
        self.canvas.pack(padx=10, pady=(10, 0))

        info_frame = tk.Frame(root, bg="#1a1a2e")
        info_frame.pack(fill="x", padx=10, pady=5)

        self.score_label = tk.Label(info_frame, text="Score: 0",
                                    font=("Arial", 13, "bold"),
                                    bg="#1a1a2e", fg="#a8ff78")
        self.score_label.pack(side="left", padx=8)

        self.high_label = tk.Label(info_frame, text="Best: 0",
                                   font=("Arial", 13, "bold"),
                                   bg="#1a1a2e", fg="#f7971e")
        self.high_label.pack(side="right", padx=8)

        btn_frame = tk.Frame(root, bg="#1a1a2e")
        btn_frame.pack(pady=(0, 10))

        tk.Button(btn_frame, text="Restart", command=self.start_game,
                  font=("Arial", 11, "bold"), bg="#2d6a2d", fg="white",
                  relief="flat", padx=15, pady=4).pack()

        self.root.bind("<KeyPress>", self.change_direction)
        self.high_score = 0
        self.draw_background()
        self.start_game()

    def draw_background(self):
        # Sky gradient using layered rects
        colors = ["#0d1b0d", "#0f2310", "#122b12", "#153215", "#183a18"]
        for i, c in enumerate(colors):
            self.canvas.create_rectangle(0, i * 40, WIDTH, (i + 1) * 40, fill=c, outline="")

        # Remaining area
        self.canvas.create_rectangle(0, 200, WIDTH, HEIGHT, fill="#1a3a1a", outline="")

        # Stars
        random.seed(42)
        for _ in range(60):
            x = random.randint(0, WIDTH)
            y = random.randint(0, 180)
            r = random.choice([1, 1, 1, 2])
            brightness = random.choice(["#ffffff", "#ddffdd", "#aaffaa"])
            self.canvas.create_oval(x, y, x+r, y+r, fill=brightness, outline="")

        # Moon
        self.canvas.create_oval(390, 20, 430, 60, fill="#e8f5d0", outline="#c5e8a0", width=1)
        self.canvas.create_oval(400, 22, 435, 57, fill="#183a18", outline="")

        # Ground base
        self.canvas.create_rectangle(0, 430, WIDTH, HEIGHT, fill="#0f2010", outline="")

        # Grass patches
        for gx in range(0, WIDTH, 15):
            h = random.randint(5, 18)
            shade = random.choice(["#1a5c1a", "#1e6b1e", "#154d15", "#237823"])
            self.canvas.create_line(gx, 432, gx + random.randint(-4, 4),
                                    432 - h, fill=shade, width=2)

        # Trees
        self._draw_tree(30, 400, 80)
        self._draw_tree(80, 410, 60)
        self._draw_tree(420, 395, 90)
        self._draw_tree(465, 408, 65)
        self._draw_tree(10, 420, 50)
        self._draw_tree(490, 415, 55)

        # Bushes
        for bx in range(0, WIDTH, 45):
            bw = random.randint(25, 45)
            bh = random.randint(12, 22)
            shade = random.choice(["#1a5c1a", "#196019", "#145514"])
            self.canvas.create_oval(bx, 430 - bh, bx + bw, 435, fill=shade, outline="")

        # Fireflies
        random.seed(99)
        for _ in range(12):
            fx = random.randint(20, 480)
            fy = random.randint(200, 430)
            self.canvas.create_oval(fx, fy, fx+3, fy+3, fill="#ccff66", outline="")
            self.canvas.create_oval(fx-2, fy-2, fx+5, fy+5,
                                    fill="", outline="#99ff33", width=1)

        # Subtle grid
        for x in range(0, WIDTH, CELL):
            self.canvas.create_line(x, 0, x, HEIGHT, fill="#1e4a1e", width=1)
        for y in range(0, HEIGHT, CELL):
            self.canvas.create_line(0, y, WIDTH, y, fill="#1e4a1e", width=1)

    def _draw_tree(self, x, y, height):
        trunk_w = max(5, height // 10)
        self.canvas.create_rectangle(x - trunk_w//2, y - height//3,
                                     x + trunk_w//2, y,
                                     fill="#4a2e0a", outline="")
        layers = 3
        shade_list = ["#1b5e1b", "#1e6b1e", "#227822"]
        for i in range(layers):
            ly = y - height//3 - (i * height // (layers + 1))
            lw = int((height // 2) * (1 - i * 0.2))
            shade = shade_list[i % 3]
            self.canvas.create_polygon(
                x - lw, ly,
                x + lw, ly,
                x, ly - height // (layers + 1) - 10,
                fill=shade, outline="#0d3d0d", width=1
            )

    def start_game(self):
        self.snake = [(240, 200), (220, 200), (200, 200), (180, 200)]
        self.direction = "Right"
        self.next_direction = "Right"
        self.score = 0
        self.running = True
        self.food = None
        self.spawn_food()
        self.update_score()
        self.run()

    def spawn_food(self):
        while True:
            x = random.randint(2, (WIDTH // CELL) - 3) * CELL
            y = random.randint(2, (HEIGHT // CELL) - 3) * CELL
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def change_direction(self, event):
        opposites = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
        key_map = {"Left": "Left", "Right": "Right", "Up": "Up", "Down": "Down",
                   "a": "Left", "d": "Right", "w": "Up", "s": "Down"}
        new_dir = key_map.get(event.keysym)
        if new_dir and new_dir != opposites.get(self.direction):
            self.next_direction = new_dir

    def run(self):
        if not self.running:
            return
        self.direction = self.next_direction
        hx, hy = self.snake[0]
        moves = {"Left": (-CELL, 0), "Right": (CELL, 0),
                 "Up": (0, -CELL), "Down": (0, CELL)}
        dx, dy = moves[self.direction]
        new_head = (hx + dx, hy + dy)

        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in self.snake):
            self.game_over()
            return

        self.snake.insert(0, new_head)
        ate = new_head == self.food
        if ate:
            self.score += 10
            self.update_score()
            self.spawn_food()
        else:
            self.snake.pop()

        self.draw()
        self.root.after(DELAY, self.run)

    def draw(self):
        self.canvas.delete("snake_layer")
        self.draw_food()
        self.draw_snake()

    def draw_food(self):
        fx, fy = self.food
        cx, cy = fx + CELL//2, fy + CELL//2
        self.canvas.create_oval(fx+2, fy+3, fx+CELL-2, fy+CELL-1,
                                fill="#cc2200", outline="#ff4422", width=1, tags="snake_layer")
        self.canvas.create_oval(fx+5, fy+5, fx+9, fy+9,
                                fill="#ff6655", outline="", tags="snake_layer")
        self.canvas.create_line(cx, fy+3, cx+3, fy-2,
                                fill="#5a3a00", width=2, tags="snake_layer")
        self.canvas.create_oval(cx+2, fy-4, cx+8, fy+1,
                                fill="#33aa33", outline="", tags="snake_layer")

    def draw_snake(self):
        n = len(self.snake)
        for i in range(n - 1, -1, -1):
            x, y = self.snake[i]
            t = i / max(n - 1, 1)

            if i == 0:
                self.draw_head(x, y)
            else:
                r = int(30 + (1 - t) * 60)
                g = int(160 + (1 - t) * 60)
                b = int(20 + (1 - t) * 20)
                body_col = f"#{r:02x}{g:02x}{b:02x}"
                shade_col = f"#{max(0,r-20):02x}{max(0,g-40):02x}{max(0,b-10):02x}"

                is_tail = (i == n - 1)

                if is_tail:
                    nx, ny = self.snake[i - 1]
                    dx = nx - x
                    dy = ny - y
                    if dx != 0:
                        if dx > 0:
                            pts = [x+2, y+CELL//2-3, x+CELL-1, y+4,
                                   x+CELL-1, y+CELL-4, x+2, y+CELL//2+3]
                        else:
                            pts = [x+CELL-2, y+CELL//2-3, x+1, y+4,
                                   x+1, y+CELL-4, x+CELL-2, y+CELL//2+3]
                    else:
                        if dy > 0:
                            pts = [x+CELL//2-3, y+2, x+4, y+CELL-1,
                                   x+CELL-4, y+CELL-1, x+CELL//2+3, y+2]
                        else:
                            pts = [x+CELL//2-3, y+CELL-2, x+4, y+1,
                                   x+CELL-4, y+1, x+CELL//2+3, y+CELL-2]
                    self.canvas.create_polygon(pts, fill=body_col, outline=shade_col,
                                              width=1, smooth=True, tags="snake_layer")
                else:
                    pad = 2
                    self.canvas.create_rectangle(x+pad, y+pad, x+CELL-pad, y+CELL-pad,
                                                fill=body_col, outline=shade_col,
                                                width=1, tags="snake_layer")
                    if i % 3 == 0:
                        mx, my = x + CELL//2, y + CELL//2
                        self.canvas.create_oval(mx-4, my-3, mx+4, my+3,
                                               fill=shade_col, outline="", tags="snake_layer")

    def draw_head(self, x, y):
        d = self.direction
        col = "#22cc22"
        dark = "#118811"

        self.canvas.create_rectangle(x+1, y+1, x+CELL-1, y+CELL-1,
                                    fill=col, outline=dark, width=1,
                                    tags="snake_layer")

        if d == "Right":
            ex1, ey1 = x+12, y+5
            ex2, ey2 = x+12, y+13
            tx, ty = x+18, y+CELL//2
        elif d == "Left":
            ex1, ey1 = x+6, y+5
            ex2, ey2 = x+6, y+13
            tx, ty = x+1, y+CELL//2
        elif d == "Up":
            ex1, ey1 = x+5, y+6
            ex2, ey2 = x+13, y+6
            tx, ty = x+CELL//2, y+1
        else:
            ex1, ey1 = x+5, y+12
            ex2, ey2 = x+13, y+12
            tx, ty = x+CELL//2, y+CELL-1

        for ex, ey in [(ex1, ey1), (ex2, ey2)]:
            self.canvas.create_oval(ex-3, ey-3, ex+3, ey+3,
                                   fill="white", outline=dark, width=1, tags="snake_layer")
            self.canvas.create_oval(ex-1, ey-1, ex+1, ey+1,
                                   fill="black", outline="", tags="snake_layer")

        if d == "Right":
            self.canvas.create_line(x+CELL-1, y+CELL//2, tx+5, ty,
                                   fill="#ff3333", width=1, tags="snake_layer")
            self.canvas.create_line(tx+5, ty, tx+9, ty-3, fill="#ff3333", width=1, tags="snake_layer")
            self.canvas.create_line(tx+5, ty, tx+9, ty+3, fill="#ff3333", width=1, tags="snake_layer")
        elif d == "Left":
            self.canvas.create_line(x+1, y+CELL//2, tx-5, ty,
                                   fill="#ff3333", width=1, tags="snake_layer")
            self.canvas.create_line(tx-5, ty, tx-9, ty-3, fill="#ff3333", width=1, tags="snake_layer")
            self.canvas.create_line(tx-5, ty, tx-9, ty+3, fill="#ff3333", width=1, tags="snake_layer")
        elif d == "Up":
            self.canvas.create_line(x+CELL//2, y+1, tx, ty-5,
                                   fill="#ff3333", width=1, tags="snake_layer")
            self.canvas.create_line(tx, ty-5, tx-3, ty-9, fill="#ff3333", width=1, tags="snake_layer")
            self.canvas.create_line(tx, ty-5, tx+3, ty-9, fill="#ff3333", width=1, tags="snake_layer")
        else:
            self.canvas.create_line(x+CELL//2, y+CELL-1, tx, ty+5,
                                   fill="#ff3333", width=1, tags="snake_layer")
            self.canvas.create_line(tx, ty+5, tx-3, ty+9, fill="#ff3333", width=1, tags="snake_layer")
            self.canvas.create_line(tx, ty+5, tx+3, ty+9, fill="#ff3333", width=1, tags="snake_layer")

    def update_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.score_label.config(text=f"Score: {self.score}")
        self.high_label.config(text=f"Best: {self.high_score}")

    def game_over(self):
        self.running = False
        self.canvas.create_rectangle(100, 170, 400, 320,
                                    fill="#0a1a0a", outline="#33aa33",
                                    width=2, tags="snake_layer")
        self.canvas.create_text(WIDTH//2, 210, text="GAME OVER",
                               fill="#ff4444", font=("Arial", 26, "bold"),
                               tags="snake_layer")
        self.canvas.create_text(WIDTH//2, 255, text=f"Score: {self.score}",
                               fill="#a8ff78", font=("Arial", 16),
                               tags="snake_layer")
        self.canvas.create_text(WIDTH//2, 290, text="Press Restart to play again",
                               fill="#77bb77", font=("Arial", 11),
                               tags="snake_layer")

root = tk.Tk()
root.configure(bg="#1a1a2e")
game = SnakeGame(root)
root.mainloop()