from math import isfinite, log, tan


def function(x):
    if not isfinite(x) or not -5 <= x <= 5:
        raise ValueError("Аргумент должен лежать в интервале [−5; 5].")
    if x <= -2:
        return (-x - 2) / 3
    if x == 0:
        return 0.0
    if x < 2:
        half = x / 2
        # Для наименьших ненулевых float деление на два округляется к нулю.
        return -log(abs(tan(half))) if half else log(2) - log(abs(x))
    return (x - 2) / 3


def main():
    try:
        x = float(input("Введите x: "))
        print(f"f({x:g}) = {function(x):.8g}")
    except (EOFError, ValueError) as error:
        print(f"Ошибка ввода: {error or 'нет аргумента'}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
