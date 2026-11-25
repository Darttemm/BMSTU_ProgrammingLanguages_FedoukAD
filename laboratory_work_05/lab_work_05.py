def read_matrix(n, rows):
    if n <= 0:
        raise ValueError("Порядок матрицы должен быть положительным.")
    matrix = [list(map(int, row.split())) for row in rows]
    if len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError(f"Ожидается {n} строк по {n} целых чисел.")
    return matrix


def transpose(matrix):
    n = len(matrix)
    return [[matrix[i][j] for i in range(n)] for j in range(n)]


def frequencies(matrix):
    counts = {}
    for row in matrix:
        for value in row:
            counts[value] = counts.get(value, 0) + 1
    return counts


def format_matrix(matrix):
    width = max(len(str(value)) for row in matrix for value in row)
    return "\n".join(" ".join(f"{value:>{width}}" for value in row) for row in matrix)


def result_text(matrix):
    counts = frequencies(matrix)
    frequencies_text = "\n".join(f"{value:>8} | {counts[value]}" for value in sorted(counts))
    return (f"Исходная матрица\n{format_matrix(matrix)}\n"
            f"Транспонированная матрица\n{format_matrix(transpose(matrix))}\n"
            f"Значение | Количество\n{frequencies_text}")


def main():
    try:
        n = int(input("Порядок матрицы: "))
        print(result_text(read_matrix(n, (input() for _ in range(n)))))
    except (EOFError, ValueError) as error:
        print(f"Ошибка ввода: {error or 'неполная матрица'}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
