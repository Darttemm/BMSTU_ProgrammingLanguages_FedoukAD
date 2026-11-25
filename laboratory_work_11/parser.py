from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "laboratory_work_10"))
from lexer import LexError, tokenize

TYPES = {"целое", "цел", "вещ", "вещественное", "строка"}
PRECEDENCE = (
    {"||"}, {"&&"}, {"==", "!=", "<", ">", "<=", ">="}, {"+", "-"}, {"*", "/", "%"},
)


class ParseError(Exception):
    def __init__(self, message, token):
        self.line, self.col = token.line, token.col
        super().__init__(f"ParseError [{token.line}:{token.col}]: {message}")


def node(kind, **attrs):
    return {"kind": kind, **attrs}


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i]

    def take(self):
        tok = self.peek()
        if tok.kind != "EOF":
            self.i += 1
        return tok

    def match(self, kind, value=None):
        tok = self.peek()
        if tok.kind == kind and (value is None or tok.value == value):
            return self.take()
        return None

    def expect(self, kind, value=None):
        tok = self.match(kind, value)
        if tok is None:
            got = self.peek()
            raise ParseError(f"ожидалось {value or kind}, получено {got.value!r}", got)
        return tok

    def program(self):
        self.expect("KW", "программа")
        name = self.expect("ID").value
        body = self.block()
        end = self.peek()
        if end.value != "конец" or end.kind not in ("ID", "KW"):
            raise ParseError("ожидалось 'конец'", end)
        self.take()
        self.expect("EOF")
        return node("Программа", name=name, body=body)

    def block(self):
        self.expect("SEP", "{")
        body = []
        while self.peek().kind != "EOF" and self.peek().value != "}":
            body.append(self.statement())
        self.expect("SEP", "}")
        return body

    def statement(self):
        if self.match("KW", "если"):
            cond = self.expr()
            then = self.block()
            other = self.block() if self.match("KW", "иначе") else None
            return node("Если", cond=cond, then=then, els=other)
        if self.match("KW", "пока"):
            cond = self.expr()
            return node("Пока", cond=cond, body=self.block())
        if self.match("KW", "печать"):
            args = []
            if self.match("SEP", "("):
                args.append(self.expr())
                while self.match("SEP", ","):
                    args.append(self.expr())
                self.expect("SEP", ")")
            self.expect("SEP", ";")
            return node("Печать", args=args)
        if self.match("KW", "возврат"):
            if self.match("SEP", ";"):
                return node("Возврат", expr=None)
            expr = self.expr()
            self.expect("SEP", ";")
            return node("Возврат", expr=expr)
        if self.peek().kind == "SEP" and self.peek().value == "{":
            return node("Блок", body=self.block())
        return self.named_statement()

    def named_statement(self):
        name = self.expect("ID").value
        if self.match("SEP", ":"):
            typ = self.expect("KW")
            if typ.value not in TYPES:
                raise ParseError("ожидалось название типа", typ)
            value = self.expr() if self.match("OP", "=") else None
            self.expect("SEP", ";")
            return node("Объявл", name=name, typ=typ.value, init=value)
        op = self.peek()
        if op.kind != "OP" or op.value not in ("=", "+=", "-="):
            raise ParseError("ожидалось присваивание", op)
        self.take()
        value = self.expr()
        self.expect("SEP", ";")
        return node("Присв", name=name, op=op.value, expr=value)

    def expr(self, level=0):
        if level == len(PRECEDENCE):
            return self.unary()
        left = self.expr(level + 1)
        while self.peek().kind == "OP" and self.peek().value in PRECEDENCE[level]:
            op = self.take().value
            left = node("БинОп", op=op, left=left, right=self.expr(level + 1))
        return left

    def unary(self):
        tok = self.peek()
        if tok.kind == "OP" and tok.value in ("!", "-", "+"):
            self.take()
            return node("УнОп", op=tok.value, expr=self.unary())
        if self.match("SEP", "("):
            value = self.expr()
            self.expect("SEP", ")")
            return value
        if tok.kind in ("INT", "LONG", "FLOAT", "FLOAT_F"):
            self.take()
            value = tok.value[:-1] if tok.kind in ("LONG", "FLOAT_F") else tok.value
            try:
                if tok.kind in ("FLOAT", "FLOAT_F"):
                    number = float(value)
                    if abs(number) == float("inf"):
                        raise ValueError
                else:
                    base = 0 if value.lower().startswith(("0x", "0b")) else 10
                    number = int(value, base)
            except ValueError:
                raise ParseError("числовой литерал вне диапазона", tok) from None
            return node("Число", value=number)
        if tok.kind in ("STR", "ID"):
            self.take()
            return node("Строка" if tok.kind == "STR" else "Имя", value=tok.value)
        raise ParseError(f"ожидалось выражение, получено {tok.value!r}", tok)


def parse(source):
    return Parser(tokenize(source)).program()
