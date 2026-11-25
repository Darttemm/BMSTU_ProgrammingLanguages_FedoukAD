import argparse
from decimal import InvalidOperation

from lab_work_07_1 import plot
from lab_work_03_1 import arguments
from lab_work_03_3 import series


def point_set(start="-1", stop="1", step="0.005"):
    x_values = arguments(start, stop, step)
    if len(x_values) < 2 or x_values[0] == x_values[-1]:
        raise ValueError("Для графика нужно не менее двух различных точек.")
    return [(x, series(x, 1e-3)[0]) for x in x_values]


def draw(start="-1", stop="1", step="0.005"):
    points = point_set(start, stop, step)
    y_values = [y for _, y in points]
    low, high = min(y_values), max(y_values)
    if low == high:
        low, high = low - 0.01, high + 0.01
    screen, _, line, _ = plot("Ряд Тейлора для (1 + x)^(1/4)",
                              (points[0][0], points[-1][0], low, high))
    line(points, "#783690", 2)
    screen.update()
    return screen


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description="График функции, вычисленной рядом.")
    cli.add_argument("--start", default="-1")
    cli.add_argument("--stop", default="1")
    cli.add_argument("--step", default="0.005")
    args = cli.parse_args()
    try:
        draw(args.start, args.stop, args.step).mainloop()
    except (InvalidOperation, ValueError) as exc:
        cli.error(str(exc))
