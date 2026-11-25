from pathlib import Path
import argparse

from lexer import LexError, tokenize


def main():
    cli = argparse.ArgumentParser(description="Лексический анализатор языка «Бауманец».")
    cli.add_argument("source", type=Path, nargs="?", default=Path(__file__).with_name("programm.bmstu"))
    args = cli.parse_args()
    try:
        tokens = tokenize(args.source.read_text(encoding="utf-8"))
    except (OSError, ValueError, LexError) as error:
        cli.exit(1, f"{error}\n")
    print(f"{'Тип':<8} {'Лексема':<24} {'Строка':>6} {'Столбец':>7}")
    for token in tokens:
        print(f"{token.kind:<8} {token.value!r:<24} {token.line:>6} {token.col:>7}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
