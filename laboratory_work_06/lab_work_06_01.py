import argparse
from pathlib import Path
import sys
from tempfile import NamedTemporaryFile


def solve(task, text):
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / f"laboratory_work_{task:02d}"))
    if task == 1:
        from lab_work_01_02 import calculate, read_values, result_text
        return result_text(*calculate(*read_values(text)))
    rows = text.splitlines()
    if not rows:
        raise ValueError("Файл пуст.")
    n = int(rows[0])
    if task == 4:
        from lab_work_04 import calculate, result_text
        numbers = list(map(float, " ".join(rows[1:]).split()))
        if n < 1 or len(numbers) != n + 1:
            raise ValueError("После n укажите n элементов массива и число для вставки.")
        return result_text(calculate(numbers[:-1], numbers[-1]))
    from lab_work_05 import read_matrix, result_text
    return result_text(read_matrix(n, rows[1:]))


def save_result(path, text):
    with NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                            delete=False) as stream:
        temp = Path(stream.name)
        try:
            stream.write(text + "\n")
            stream.close()
            temp.replace(path)
        finally:
            temp.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Файловый ввод и вывод для работ 1, 4 и 5.")
    parser.add_argument("task", type=int, choices=(1, 4, 5))
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        if args.input.resolve() == args.output.resolve() or (
            args.output.exists() and args.input.samefile(args.output)
        ):
            raise ValueError("Входной и выходной файлы должны различаться.")
        result = solve(args.task, args.input.read_text(encoding="utf-8"))
        save_result(args.output, result)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Ошибка: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
