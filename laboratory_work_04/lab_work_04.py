from math import isfinite


def extremes(values):
    if not values or not all(map(isfinite, values)):
        raise ValueError("Нужен непустой массив конечных чисел.")
    lowest = highest = 0
    for i in range(1, len(values)):
        if values[i] < values[lowest]:
            lowest = i
        if values[i] > values[highest]:
            highest = i
    return lowest, highest


def calculate(values, value):
    lo, hi = extremes(values)
    if not values[lo] <= value <= values[hi]:
        raise ValueError("Новое число должно лежать в диапазоне [Min; Max].")
    middle = (lo + hi) // 2
    changed = values.copy()
    for i in range(len(changed) - 1, middle, -1):
        changed[i] = changed[i - 1]
    changed[middle] = value
    ordered = changed.copy()
    distances = [abs(item - value) for item in ordered]
    if not all(map(isfinite, distances)):
        raise ValueError("Разность с новым значением выходит за диапазон float.")
    for i in range(1, len(ordered)):
        item, key = ordered[i], distances[i]
        j = i
        while j > 0 and distances[j - 1] > key:
            ordered[j] = ordered[j - 1]
            distances[j] = distances[j - 1]
            j -= 1
        ordered[j] = item
        distances[j] = key
    return values[lo], values[hi], middle + 1, changed, ordered


def result_text(result):
    lo, hi, position, changed, ordered = result
    return (f"Min = {lo:g}, Max = {hi:g}\n"
            f"Позиция вставки: {position}\n"
            f"После вставки: {changed}\nПосле сортировки: {ordered}")


def main():
    try:
        n = int(input("Количество элементов: "))
        values = list(map(float, input("Элементы массива: ").split()))
        if n != len(values):
            raise ValueError("Количество элементов не совпадает с n.")
        lo, hi = extremes(values)
        print(f"Допустимый диапазон вставки: [{values[lo]:g}; {values[hi]:g}]")
        value = float(input("Новое значение: "))
        print(result_text(calculate(values, value)))
    except (EOFError, ValueError) as error:
        print(f"Ошибка ввода: {error or 'нет данных'}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
