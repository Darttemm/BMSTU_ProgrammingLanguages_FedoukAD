from tokens import DOUBLE, KEYWORDS, OPERATORS, SEPARATORS, Token


class LexError(Exception):
    def __init__(self, msg, line, col):
        self.line, self.col = line, col
        super().__init__(msg)

    def __str__(self):
        return f"LexError [{self.line}:{self.col}]: {super().__str__()}"


class Lexer:
    def __init__(self, source):
        self.src = source.replace("\r\n", "\n").replace("\r", "\n")
        self.pos, self.line, self.col = 0, 1, 1

    def peek(self, offset=0):
        return self.src[self.pos + offset:self.pos + offset + 1]

    def advance(self):
        ch = self.src[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 4 if ch == "\t" else 1
        return ch

    def take_while(self, test):
        start = self.pos
        while self.peek() and test(self.peek()):
            self.advance()
        return self.src[start:self.pos]

    def tokenize(self):
        out = []
        while ch := self.peek():
            line, col = self.line, self.col
            pair = ch + self.peek(1)
            if ch.isspace():
                self.advance()
            elif ch == "#" or pair == "//":
                self.take_while(lambda c: c != "\n")
            elif pair == "/*":
                end = self.src.find("*/", self.pos + 2)
                if end < 0:
                    raise LexError("незакрытый комментарий", line, col)
                while self.pos < end + 2:
                    self.advance()
            else:
                if digit(ch) or (ch == "." and digit(self.peek(1))):
                    kind, value = self.number()
                elif ch.isalpha() or ch == "_":
                    value = self.take_while(word_char)
                    kind = "KW" if value in KEYWORDS else "ID"
                elif ch == '"':
                    kind, value = "STR", self.string()
                elif pair in DOUBLE:
                    kind, value = "OP", self.advance() + self.advance()
                elif ch in OPERATORS or ch in SEPARATORS:
                    kind = "OP" if ch in OPERATORS else "SEP"
                    value = self.advance()
                else:
                    raise LexError(f"недопустимый символ {ch!r}", line, col)
                out.append(Token(kind, value, line, col))
        return out + [Token("EOF", "", self.line, self.col)]

    def number(self):
        start = self.pos
        kind, based = "INT", False
        prefix = self.src[start:start + 2].lower()
        if prefix in ("0x", "0b"):
            based = True
            self.advance()
            self.advance()
            alphabet = "0123456789abcdef" if prefix == "0x" else "01"
            if not self.take_while(lambda c: c.lower() in alphabet):
                raise LexError("ожидались цифры", self.line, self.col)
            if digit(self.peek()):
                raise LexError("цифра вне основания", self.line, self.col)
        else:
            self.take_while(digit)
            if self.peek() == "." and digit(self.peek(1)):
                kind = "FLOAT"
                self.advance()
                self.take_while(digit)
            if self.peek() in ("e", "E"):
                kind = "FLOAT"
                self.advance()
                if self.peek() in ("+", "-"):
                    self.advance()
                if not self.take_while(digit):
                    raise LexError("ожидались цифры экспоненты", self.line, self.col)
        suffix = self.peek()
        if suffix and (suffix.isalpha() or suffix == "_"):
            end = self.pos + 1
            while end < len(self.src) and word_char(self.src[end]):
                end += 1
            word = self.src[self.pos:end]
            if len(word) == 1 and ((suffix == "L" and kind == "INT") or (suffix == "f" and not based)):
                kind = "LONG" if suffix == "L" else "FLOAT_F"
                self.advance()
            elif (len(word) == 1 or suffix == "_"
                  or (suffix in ("L", "f") and
                      (digit(word[1]) or all(c in "Lf" for c in word)))):
                raise LexError(f"недопустимый суффикс {word!r}", self.line, self.col)
            # Например, 42Layer состоит из числа 42 и имени Layer.
        return kind, self.src[start:self.pos]

    def string(self):
        line, col = self.line, self.col
        self.advance()
        parts = []
        escapes = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}
        while self.peek() not in ("", "\n", '"'):
            ch = self.advance()
            if ch == "\\":
                esc = self.peek()
                if esc not in escapes:
                    raise LexError("неизвестная escape-последовательность", self.line, self.col - 1)
                ch = escapes[self.advance()]
            parts.append(ch)
        if self.peek() != '"':
            raise LexError("незакрытая строка", line, col)
        self.advance()
        return "".join(parts)


def digit(ch):
    return bool(ch) and "0" <= ch <= "9"


def word_char(ch):
    return ch.isalnum() or ch == "_"


def tokenize(source):
    return Lexer(source).tokenize()
