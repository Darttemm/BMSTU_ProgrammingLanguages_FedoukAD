from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lexer import LexError, tokenize


GOOD = (
    ("42L", [("LONG", "42L", 1, 1)]),
    ("3.5f", [("FLOAT_F", "3.5f", 1, 1)]),
    ("7f", [("FLOAT_F", "7f", 1, 1)]),
    ("42Layer", [("INT", "42", 1, 1), ("ID", "Layer", 1, 3)]),
    ("0x1fL", [("LONG", "0x1fL", 1, 1)]),
    ("0b101", [("INT", "0b101", 1, 1)]),
    ("1e-5", [("FLOAT", "1e-5", 1, 1)]),
    ("если\n\tсчёт", [("KW", "если", 1, 1), ("ID", "счёт", 2, 5)]),
    ("a<=b;", [("ID", "a", 1, 1), ("OP", "<=", 1, 2),
              ("ID", "b", 1, 4), ("SEP", ";", 1, 5)]),
    ('/*x*/ "а\\n"', [("STR", "а\n", 1, 7)]),
)
BAD = (
    ("42LL", 1, 3, "суффикс"),
    ("3.5g", 1, 4, "суффикс"),
    ("42L9", 1, 3, "суффикс"),
    ("5i", 1, 2, "суффикс"),
    ("1e+", 1, 4, "экспоненты"),
)


class LexerTests(unittest.TestCase):
    def test_accepted(self):
        for source, expected in GOOD:
            with self.subTest(source=source):
                tokens = tokenize(source)
                self.assertEqual(tokens[-1].kind, "EOF")
                self.assertEqual(
                    [(t.kind, t.value, t.line, t.col) for t in tokens[:-1]],
                    expected,
                )

    def test_rejected(self):
        for source, line, col, reason in BAD:
            with self.subTest(source=source):
                with self.assertRaisesRegex(LexError, reason) as caught:
                    tokenize(source)
                self.assertEqual((caught.exception.line, caught.exception.col), (line, col))


if __name__ == "__main__":
    unittest.main()
