from decimal import Decimal, InvalidOperation
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "laboratory_work_02"))
from lab_work_02_1 import function


def arguments(start, stop, step):
    a, b, h = map(Decimal, (start, stop, step))
    if not all(value.is_finite() for value in (a, b, h)):
        raise ValueError("Границы и шаг должны быть конечными.")
    if a > b or h <= 0:
        raise ValueError("Требуется Xнач ≤ Xкон и dx > 0.")
    if b - a >= 5000 * h:
        raise ValueError("Слишком много точек. Увеличьте шаг.")
    count = int((b - a) // h)
    return [float(a + i * h) for i in range(count + 1)]


def table(start="-5", stop="5", step="0.5"):
    points = arguments(start, stop, step)
    rows = [f"{x:>10.5g} | {function(x):>14.8g}" for x in points]
    return "\n".join(["Таблица значений f(x)", "         x |           f(x)", *rows])


def main():
    try:
        values = input("Введите Xнач, Xкон, dx [−5 5 0.5]: ").split()
        if values and len(values) != 3:
            raise ValueError("Нужно ввести три числа.")
        print(table(*values))
    except (EOFError, InvalidOperation, ValueError) as error:
        print(f"Ошибка ввода: {error or 'некорректные числа'}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
