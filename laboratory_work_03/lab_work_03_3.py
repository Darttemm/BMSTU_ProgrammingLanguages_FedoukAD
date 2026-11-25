from decimal import InvalidOperation
from math import frexp, isfinite
from lab_work_03_1 import arguments


def series(x, eps):
    if not -1 <= x <= 1 or not isfinite(eps) or not 1e-12 <= eps < 1:
        raise ValueError("Требуется |x| ≤ 1 и 1e−12 ≤ ε < 1.")
    if x == -1:
        return 0.0, 0
    if abs(x) > 0.75:
        # 1 + x = m * 2**e, поэтому ряд можно суммировать в точке m - 1.
        m, e = frexp(1 + x)
        base = m - 1
        factor = 2 ** (e / 4)
    else:
        base, factor = x, 1.0
    total, term, n = 1.0, 1.0, 0
    while True:
        next_term = term * base * (0.25 - n) / (n + 1)
        tail = abs(next_term)
        if base < 0:
            tail /= 1 - abs(base)
        if factor * tail <= eps:
            return factor * total, n + 1
        total += next_term
        term = next_term
        n += 1


def main():
    try:
        a, b, h, eps = input("Введите Xнач, Xкон, dx, ε: ").split()
        points = arguments(a, b, h)
        print("         x |         y(x) | Членов")
        for x in points:
            y, n = series(x, float(eps))
            print(f"{x:10.6g} | {y:12.9g} | {n:6d}")
    except (EOFError, InvalidOperation, ValueError) as error:
        print(f"Ошибка ввода: {error or 'некорректные числа'}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
