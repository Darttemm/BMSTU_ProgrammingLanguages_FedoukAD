from pathlib import Path
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from parser import LexError, ParseError, parse


def in_program(body):
    return parse("программа demo { " + body + " } конец")["body"][0]


class ParserTests(unittest.TestCase):
    def test_example(self):
        p = Path(__file__).with_name("example")
        actual = parse(p.with_suffix(".src").read_text(encoding="utf-8"))
        expected = json.loads(p.with_suffix(".json").read_text(encoding="utf-8"))
        self.assertEqual(actual, expected)

    def test_statements(self):
        for body, kind in (
            ("x: цел;", "Объявл"), ("x += 1;", "Присв"),
            ("если 1 {} иначе {}", "Если"), ("пока 1 {}", "Пока"),
            ("печать;", "Печать"), ('печать("x", 1);', "Печать"),
            ("возврат;", "Возврат"), ("{ возврат 1; }", "Блок"),
        ):
            with self.subTest(body=body):
                self.assertEqual(in_program(body)["kind"], kind)

    def test_literals(self):
        for source, value in (
            ("3.14", 3.14), ("0x1F", 31), ("0b1010", 10),
            ("1e-5", 1e-5), ("42L", 42), ("3.5f", 3.5),
        ):
            with self.subTest(source=source):
                self.assertEqual(in_program(f"возврат {source};")["expr"]["value"], value)

    def test_precedence(self):
        first = in_program("возврат 1+2*3;")["expr"]
        self.assertEqual((first["op"], first["right"]["op"]), ("+", "*"))
        second = in_program("возврат (1+2)*3;")["expr"]
        self.assertEqual((second["op"], second["left"]["op"]), ("*", "+"))
        third = in_program("возврат 1-2-3;")["expr"]
        self.assertEqual((third["op"], third["left"]["op"]), ("-", "-"))
        fourth = in_program("возврат !a||b&&2<3;")["expr"]
        self.assertEqual((fourth["op"], fourth["right"]["op"]), ("||", "&&"))
        self.assertEqual(fourth["left"]["op"], "!")

    def test_lexical_errors(self):
        for text, col in (("$", 1), ('"a', 1), ('"\\q"', 2)):
            with self.subTest(text=text), self.assertRaises(LexError) as caught:
                parse(text)
            self.assertEqual((caught.exception.line, caught.exception.col), (1, col))

    def test_syntax_errors(self):
        for text, line, col in (
            ("программа x {\nвозврат 1\n} конец", 3, 1),
            ("программа x {\nвозврат 1;", 2, 11),
            ("программа x {} конец лишнее", 1, 22),
        ):
            with self.subTest(text=text), self.assertRaises(ParseError) as caught:
                parse(text)
            self.assertEqual((caught.exception.line, caught.exception.col), (line, col))


if __name__ == "__main__":
    unittest.main()
