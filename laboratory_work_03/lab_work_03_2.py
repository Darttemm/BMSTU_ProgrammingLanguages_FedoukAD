from pathlib import Path
from random import Random
from math import isfinite
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "laboratory_work_02"))
from lab_work_02_2 import hit


def shots(radius, count=10, seed=None):
    if not isfinite(radius) or radius <= 0:
        raise ValueError("R должен быть конечным и положительным.")
    rng = Random(seed)
    for _ in range(count):
        x, y = (rng.uniform(-1, 1) * radius for _ in range(2))
        yield x, y, hit(x, y, radius)


def main():
    try:
        values = input("Радиус и, при необходимости, seed: ").split()
        if not 1 <= len(values) <= 2:
            raise ValueError("Введите радиус и, при необходимости, seed.")
        seed = int(values[1]) if len(values) == 2 else None
        print(" № |          x |          y | Результат")
        for i, (x, y, result) in enumerate(shots(float(values[0]), seed=seed), 1):
            label = "попадание" if result else "промах"
            print(f"{i:2d} | {x:10.5g} | {y:10.5g} | {label}")
    except (EOFError, ValueError) as error:
        print(f"Ошибка ввода: {error or 'нет радиуса'}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
