from decimal import Decimal, InvalidOperation
from math import atan, fsum, isfinite, pi
import tkinter as tk
from tkinter import messagebox, ttk


def arctan_series(x, eps):
    if not isfinite(x) or x <= 1 or not 1e-10 <= eps < 1:
        raise ValueError("Требуется x > 1 и 1e−10 ≤ ε < 1.")
    u = 1 / x
    whole, n = 0.0, 0
    if u > 0.5:
        # arctg(u) = pi/4 + arctg((u - 1)/(u + 1)).
        whole, u = pi / 4, (u - 1) / (u + 1)
    terms = []
    term = u
    while abs(term) > eps:
        terms.append(term)
        n += 1
        term *= -u * u * (2 * n - 1) / (2 * n + 1)
    return pi / 2 - (whole + fsum(terms))


def graph_data(start, stop, step, eps, shift):
    a, b, h = map(Decimal, (start, stop, step))
    delta, offset = float(eps), float(shift)
    if (not all(x.is_finite() for x in (a, b, h))
            or not 1 < a < b or h <= 0
            or not all(isfinite(float(x)) for x in (a, b, h))
            or not isfinite(offset)):
        raise ValueError("Требуется 1 < Xнач < Xкон, dx > 0 и конечное b.")
    if b - a >= 5000 * h:
        raise ValueError("Нужно не более 5000 точек. Увеличьте шаг.")
    count = int((b - a) // h) + 1
    if count < 2 or float(a + h) == float(a):
        raise ValueError("Шаг должен давать хотя бы две различимые точки.")
    points = [float(a + i * h) for i in range(count)]
    return points, [arctan_series(x, delta) for x in points], [atan(x) + offset for x in points]


class GraphWindow:
    def __init__(self, root):
        self.root = root
        root.title("Лабораторная работа № 8. Два графика")
        root.geometry(f"{int(root.winfo_screenwidth() * .85)}x"
                      f"{int(root.winfo_screenheight() * .78)}")
        controls = ttk.Frame(root, padding=8)
        controls.pack(fill="x")
        self.entries = []
        for name, default in zip(("Xнач", "Xкон", "dx", "ε", "b"), ("1.05", "7", ".025", ".000001", ".15")):
            ttk.Label(controls, text=name).pack(side="left", padx=(8, 2))
            field = ttk.Entry(controls, width=8)
            field.insert(0, default)
            field.pack(side="left")
            self.entries.append(field)
        ttk.Button(controls, text="Построить", command=self.build).pack(side="left", padx=10)
        self.canvas = tk.Canvas(root, background="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.data = None
        self.canvas.bind("<Configure>", lambda _event: self.redraw())
        root.bind("<Return>", lambda _event: self.build())
        self.build()

    def build(self):
        try:
            self.data = graph_data(*(field.get() for field in self.entries))
        except (InvalidOperation, ValueError) as error:
            messagebox.showerror("Ошибка ввода", str(error), parent=self.root)
            return
        self.redraw()

    def redraw(self):
        c = self.canvas
        c.delete("all")
        if self.data is None:
            return
        xs, ys, zs = self.data
        w, h = c.winfo_width(), c.winfo_height()
        if w < 240 or h < 160:
            return
        l, t, r, b = 70, 58, w - 28, h - 50
        x0, x1 = xs[0], xs[-1]
        y0, y1 = min(*ys, *zs), max(*ys, *zs)
        # Масштабируем до деления, чтобы при больших b не переполнился размах.
        scale = max(abs(y0), abs(y1), 1)
        p, q = y0 / scale, y1 / scale
        margin = max((q - p) * 0.05, 1e-15)
        p, q = max(-1.0, p - margin), min(1.0, q + margin)
        c.create_text(w / 2, 17, text="Графики функций варианта 4", font=("Arial", 16, "bold"))
        c.create_text(w / 2, 40, text="Синий — ряд для y(x)      Красный — arctg(x) + b")
        for i in range(7):
            f = i / 6
            x, y = l + f * (r - l), b - f * (b - t)
            c.create_line(x, t, x, b, fill="#d8dce2")
            c.create_line(l, y, r, y, fill="#d8dce2")
            c.create_text(x, b + 14, text=f"{x0 + f * (x1 - x0):.5g}")
            c.create_text(l - 7, y, text=f"{(p + f * (q - p)) * scale:.4g}", anchor="e")
        c.create_rectangle(l, t, r, b, outline="#28333f")
        c.create_text(r, b + 32, text="x")
        c.create_text(l - 48, t - 12, text="y, z")
        for values, color in ((ys, "#1858aa"), (zs, "#bd291d")):
            coords = []
            for x, y in zip(xs, values):
                coords.extend((l + (r - l) * ((x - x0) / (x1 - x0)),
                               b - (b - t) * ((y / scale - p) / (q - p))))
            c.create_line(coords, fill=color, width=2)


if __name__ == "__main__":
    window = tk.Tk()
    GraphWindow(window)
    window.mainloop()
