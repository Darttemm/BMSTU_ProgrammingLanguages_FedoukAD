from dataclasses import dataclass

KEYWORDS = set("""программа конец если иначе пока возврат функция истина ложь
печать целое цел вещ вещественное строка""".split())
DOUBLE = set("== != <= >= += -= && || ++".split())
OPERATORS = set("+-*/%=<>!")
SEPARATORS = set("(){}[],;.:")


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    line: int
    col: int
