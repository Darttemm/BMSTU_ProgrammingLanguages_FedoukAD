import re

TEXT = "Today is 23.10.2026 and we are teaching the regular expression. 14:58 14.58"

DATE = r"(?:0[1-9]|[12][0-9]|3[01])\.(?:0[1-9]|1[0-2])\.(?:[0-9]{4}|[0-9]{2})"
TIME = r"(?:[01][0-9]|2[0-3])[.:][0-5][0-9]"
INTEGER = r"[+-]?[0-9]+"
REAL = r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)"

PATTERNS = (
    ("Дата", rf"(?<![\w.]){DATE}(?!\w|\.[0-9])"),
    ("Время", rf"(?<![\w.:]){TIME}(?!\w|[.:][0-9])"),
    ("Целое", rf"(?<![\w.+-]){INTEGER}(?!\w|\.[0-9])"),
    ("Вещественное", rf"(?<![\w.+-]){REAL}(?!\w|\.[0-9])"),
    ("Натуральные числа", r"(?<![0-9-])0*[1-9][0-9]*(?![0-9])"),
    ("Фрагменты капсом", r"[A-ZА-ЯЁ]+"),
    ("Русская буква перед цифрой", r"\b\w*[А-Яа-яЁё]\w*[0-9]\w*\b"),
    ("Слова с заглавной", r"\b[A-ZА-ЯЁ]\w*\b"),
    ("Слова с гласной", r"\b[AEIOUYaeiouyАЕЁИОУЫЭЮЯаеёиоуыэюя]\w*\b"),
)


def analyze(text):
    # Дата и время остаются отдельными объектами при поиске числовых токенов.
    masked = text
    for _, pattern in PATTERNS[:2]:
        masked = re.sub(pattern, lambda match: " " * len(match[0]), masked)
    return [re.findall(pattern, masked if 2 <= i <= 3 else text)
            for i, (_, pattern) in enumerate(PATTERNS)]


def main():
    try:
        text = input("Текст (пустая строка — пример): ") or TEXT
    except EOFError:
        text = TEXT
    print(text)
    for (label, _), matches in zip(PATTERNS, analyze(text)):
        print(f"{label}: {', '.join(matches) or '—'}")


if __name__ == "__main__":
    main()
