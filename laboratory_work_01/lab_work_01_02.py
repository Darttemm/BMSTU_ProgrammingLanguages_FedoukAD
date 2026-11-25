from decimal import Decimal, InvalidOperation
from fractions import Fraction


def calculate(a, b, c):
    if not all((a, b, c, b + c, a + b + c, a - b - c)):
        raise ValueError("Один из знаменателей первой формулы равен нулю.")
    left = (1 / a - 1 / (b + c)) / (1 / a + 1 / (b + c))
    middle = 1 + (b * b + c * c - a * a) / (2 * b * c)
    z1 = left * middle / ((a - b - c) / (a * b * c))
    z2 = a * (a - b - c) / 2
    return z1, z2


def read_values(text):
    a, b, c = (Fraction(value) for value in text.split())
    return a, b, c


def result_text(z1, z2):
    values = (Decimal(z.numerator) / Decimal(z.denominator) for z in (z1, z2))
    return "\n".join(f"z{i} = {value}" for i, value in enumerate(values, 1))


def main():
    try:
        print(result_text(*calculate(*read_values(input("Введите a, b, c: ")))))
    except (EOFError, InvalidOperation, ValueError) as error:
        print(f"Ошибка ввода: {error or 'нет данных'}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
