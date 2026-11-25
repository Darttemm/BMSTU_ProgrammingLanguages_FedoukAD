import argparse
from math import isfinite, pi

from lab_work_07_1 import plot
from lab_work_03_2 import shots


def experiment(radius, count=10000, seed=None):
    if not 1 <= count <= 10000:
        raise ValueError("Допустимо от 1 до 10000 испытаний.")
    if not isfinite(radius) or radius <= 0 or radius * radius == 0:
        raise ValueError("Выберите положительный R с представимым квадратом.")
    square = radius * radius
    if not isfinite(4 * square):
        raise ValueError("Площадь квадрата выходит за диапазон float.")
    points = list(shots(radius, count, seed))
    fraction = sum(result for _, _, result in points) / count
    real_ratio = 3 - pi / 2
    return points, 4 * fraction * square, real_ratio * square, 100 * abs(4 * fraction / real_ratio - 1)


def draw(radius, count=10000, seed=None):
    points, estimate, exact, error = experiment(radius, count, seed)
    print(f"S ≈ {estimate:.6g}, S точная = {exact:.6g}, ошибка = {error:.3f}%")
    # Масштаб от −1 до 1 нужен только для координат на экране.
    screen, pen, _, label = plot("Мишень и метод Монте-Карло", (-1, 1, -1, 1), equal=True, divisions=4,
                                 xlabel="x/R", ylabel="y/R")
    # Масштаб подписей осей указан в долях R.
    for x, y, result in points:
        pen.goto(x / radius, y / radius)
        pen.dot(2, "#286fa6" if result else "#c8c8c8")
    label(0, -0.83, f"N = {count}, относительная ошибка {error:.2f}%")
    screen.update()
    return screen


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description="Площадь мишени варианта 24.")
    cli.add_argument("--radius", type=float, default=2)
    cli.add_argument("--count", type=int, default=10000)
    cli.add_argument("--seed", type=int)
    cli.add_argument("--text-only", action="store_true")
    args = cli.parse_args()
    try:
        if args.text_only:
            _, estimate, exact, error = experiment(args.radius, args.count, args.seed)
            print(f"S ≈ {estimate:.6g}, S точная = {exact:.6g}, ошибка = {error:.3f}%")
        else:
            draw(args.radius, args.count, args.seed).mainloop()
    except ValueError as exc:
        cli.error(str(exc))
