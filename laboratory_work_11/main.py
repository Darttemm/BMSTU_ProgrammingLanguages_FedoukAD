from pathlib import Path
import argparse
import json

from parser import LexError, ParseError, parse


def main():
    cli = argparse.ArgumentParser(description="Синтаксический анализатор языка «Бауманец».")
    cli.add_argument("source", type=Path, nargs="?",
                     default=Path(__file__).with_name("tests") / "example.src")
    args = cli.parse_args()
    try:
        tree = parse(args.source.read_text(encoding="utf-8"))
    except (OSError, ValueError, LexError, ParseError) as error:
        cli.exit(1, f"{error}\n")
    print(json.dumps(tree, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
