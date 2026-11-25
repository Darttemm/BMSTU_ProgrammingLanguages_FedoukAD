from math import hypot, isfinite


def hit(x, y, radius):
    if not all(map(isfinite, (x, y, radius))) or radius <= 0:
        raise ValueError("Координаты конечны, R > 0.")
    if abs(x) > radius or abs(y) > radius:
        return False
    # После деления на R квадрат мишени имеет стороны от −1 до 1.
    u, v = x / radius, y / radius
    if (u >= 0 and v >= 0) or (u <= 0 and v <= 0):
        return abs(u) + abs(v) >= 1
    return hypot(u, v) >= 1


def main():
    try:
        x, y, r = map(float, input("Введите x, y, R: ").split())
        print("Попадание" if hit(x, y, r) else "Промах")
    except (EOFError, ValueError) as error:
        print(f"Ошибка ввода: {error or 'нет координат и радиуса'}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
