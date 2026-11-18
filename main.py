"""Практична №5, варіант 5 — розв'язувач квадратних рівнянь ax² + bx + c = 0.

Автор: Володимир ЧАБАН, група З-41, журнал № 35 (35 mod 10 = 5).
Коефіцієнти передаються через змінні середовища A, B, C.
"""

import math
import os
import sys


def read_coef(name):
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        raise ValueError(f"не задано змінну середовища {name}")
    try:
        return float(raw.replace(",", "."))
    except ValueError:
        raise ValueError(f"{name}={raw!r} не є числом") from None


def fmt(x):
    """Число без зайвих нулів: 2.0 -> 2, 0.3333333 -> 0.3333."""
    if x == 0:
        x = 0.0  # прибрати -0
    return f"{x:.4f}".rstrip("0").rstrip(".")


def equation(a, b, c):
    parts = [f"{fmt(a)}x²"]
    parts.append(f"{'-' if b < 0 else '+'} {fmt(abs(b))}x")
    parts.append(f"{'-' if c < 0 else '+'} {fmt(abs(c))}")
    return " ".join(parts) + " = 0"


def solve(a, b, c):
    """Повертає (D, корені). Для лінійного випадку D = None."""
    if a == 0:
        if b == 0:
            return None, ("all" if c == 0 else "none")
        return None, (-c / b,)
    d = b * b - 4 * a * c
    if d > 0:
        s = math.sqrt(d)
        return d, ((-b + s) / (2 * a), (-b - s) / (2 * a))
    if d == 0:
        return d, (-b / (2 * a),)
    return d, ()


def report(a, b, c):
    line = "=" * 52
    out = [line, " РОЗВ'ЯЗУВАЧ КВАДРАТНИХ РІВНЯНЬ  (варіант 5)", line,
           f" Коефіцієнти: a = {fmt(a)}, b = {fmt(b)}, c = {fmt(c)}",
           f" Рівняння:    {equation(a, b, c)}", "-" * 52]
    d, roots = solve(a, b, c)

    if a == 0:
        out.append(" Крок 1. a = 0, тому рівняння не квадратне, а лінійне:")
        out.append(f"         {fmt(b)}x + ({fmt(c)}) = 0")
        if roots == "all":
            out.append(" Відповідь: 0 = 0 — будь-яке x є розв'язком.")
        elif roots == "none":
            out.append(f" Відповідь: {fmt(c)} = 0 — розв'язків немає.")
        else:
            out.append(f" Крок 2. x = -c / b = -({fmt(c)}) / {fmt(b)} = {fmt(roots[0])}")
            out.append(f" Відповідь: x = {fmt(roots[0])}")
        out.append(line)
        return "\n".join(out)

    out.append(" Крок 1. Дискримінант D = b² - 4ac")
    out.append(f"         D = ({fmt(b)})² - 4·{fmt(a)}·({fmt(c)})"
               f" = {fmt(b*b)} - ({fmt(4*a*c)}) = {fmt(d)}")
    if d > 0:
        s = math.sqrt(d)
        out.append(f" Крок 2. D = {fmt(d)} > 0 — два різні дійсні корені.")
        out.append(f"         √D = {fmt(s)}")
        out.append(" Крок 3. x = (-b ± √D) / (2a)")
        out.append(f"         x₁ = ({fmt(-b)} + {fmt(s)}) / {fmt(2*a)} = {fmt(roots[0])}")
        out.append(f"         x₂ = ({fmt(-b)} - {fmt(s)}) / {fmt(2*a)} = {fmt(roots[1])}")
        out.append(f" Відповідь: x₁ = {fmt(roots[0])}, x₂ = {fmt(roots[1])}")
    elif d == 0:
        out.append(" Крок 2. D = 0 — один (подвійний) корінь.")
        out.append(f" Крок 3. x = -b / (2a) = {fmt(-b)} / {fmt(2*a)} = {fmt(roots[0])}")
        out.append(f" Відповідь: x = {fmt(roots[0])}")
    else:
        re, im = -b / (2 * a), math.sqrt(-d) / (2 * abs(a))
        out.append(f" Крок 2. D = {fmt(d)} < 0 — дійсних коренів немає.")
        out.append(f"         (комплексні: x = {fmt(re)} ± {fmt(im)}i)")
        out.append(" Відповідь: дійсних коренів немає.")
    out.append(line)
    return "\n".join(out)


def main():
    try:
        a, b, c = read_coef("A"), read_coef("B"), read_coef("C")
    except ValueError as e:
        print(f"Помилка: {e}", file=sys.stderr)
        print("Приклад: docker run -e A=1 -e B=-3 -e C=2 quadratic-solver", file=sys.stderr)
        return 1
    print(report(a, b, c))
    return 0


if __name__ == "__main__":
    sys.exit(main())
