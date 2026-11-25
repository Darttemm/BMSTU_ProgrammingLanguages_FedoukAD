from pathlib import Path
import sys
import turtle

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "laboratory_work_03"))
from lab_work_03_1 import function


def point_sets():
    left = [(x / 100, function(x / 100)) for x in range(-500, -199)]
    inner_right = [(x / 100, function(x / 100)) for x in range(1, 200)]
    inner_left = [(-x, y) for x, y in reversed(inner_right)]
    right = [(x / 100, function(x / 100)) for x in range(200, 501)]
    return left, inner_left, inner_right, right


def plot(title, bounds, equal=False, divisions=8, xlabel="x", ylabel="y"):
    screen = turtle.Screen()
    screen.setup(width=0.85, height=0.82)
    screen.title(title)
    screen.tracer(0)
    x0, x1, y0, y1 = bounds
    dx, dy = x1 - x0, y1 - y0
    if equal:
        aspect = screen.window_width() / screen.window_height()
        dx, dy = max(dx, dy * aspect), max(dy, dx / aspect)
    padx = (dx * 1.24 - (x1 - x0)) / 2
    pady = (dy * 1.30 - (y1 - y0)) / 2
    screen.setworldcoordinates(x0 - padx, y0 - pady, x1 + padx, y1 + pady)
    pen = turtle.Turtle(visible=False)
    pen.penup()
    pen.speed(0)

    def line(points, color="#222222", width=1):
        pen.pencolor(color)
        pen.pensize(width)
        pen.goto(*points[0])
        pen.pendown()
        for point in points[1:]:
            pen.goto(*point)
        pen.penup()

    def label(x, y, text, size=10):
        pen.pencolor("#222222")
        pen.goto(x, y)
        pen.write(text, align="center", font=("Arial", size, "normal"))

    label((x0 + x1) / 2, y1 + 0.06 * dy, title, 16)
    line([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)])
    if x0 <= 0 <= x1:
        line([(0, y0), (0, y1)], "#989898")
    if y0 <= 0 <= y1:
        line([(x0, 0), (x1, 0)], "#989898")
    for i in range(divisions + 1):
        x = x0 + (x1 - x0) * i / divisions
        y = y0 + (y1 - y0) * i / divisions
        line([(x, y0), (x, y0 + 0.012 * dy)])
        line([(x0, y), (x0 + 0.009 * dx, y)])
        label(x, y0 - 0.058 * dy, f"{x:.3g}")
        label(x0 - 0.046 * dx, y - 0.011 * dy, f"{y:.3g}")
    label(x1 + 0.04 * dx, y0 - 0.03 * dy, xlabel, 12)
    label(x0 - 0.046 * dx, y1 + 0.035 * dy, ylabel, 12)
    return screen, pen, line, label


def draw():
    tracks = point_sets()
    top = max(y for track in tracks for _, y in track)
    screen, pen, line, label = plot("Кусочная функция", (-5, 5, -1, top), divisions=10)
    for track in tracks:
        line(track, "#1e5e9b", 2)
    pen.goto(0, 0)
    pen.dot(6, "#1e5e9b")
    label(0, top - 0.18, "В разрыве ветви не соединяются")
    screen.update()
    return screen


if __name__ == "__main__":
    draw().mainloop()
