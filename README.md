# docker-lab-5 — розв'язувач квадратних рівнянь у Docker

| Поле | Значення |
|---|---|
| Студент | Чабан Володимир |
| Група | З-41 |
| Номер у списку | 35 |
| Варіант | 5 (35 mod 10 = 5) — розв'язувач квадратних рівнянь |
| Мова | Python 3.12 |
| Базовий образ | `python:3.12-alpine` |

## Що робить програма

Розв'язує рівняння **ax² + bx + c = 0**. Коефіцієнти задаються змінними середовища `A`, `B`, `C`
(дробові можна писати через крапку або кому). Програма виводить:

- дискримінант `D = b² − 4ac` з підставленими числами;
- кількість коренів залежно від знака `D` і самі корені (для `D < 0` — повідомлення, що дійсних коренів немає, і комплексні корені довідково);
- покроковий розв'язок;
- окремо обробляє випадок `a = 0` (лінійне рівняння) і некоректне введення (код виходу 1).

## Файли

```
main.py        # програма
Dockerfile     # опис образу
.dockerignore  # що не потрапляє в контекст збірки
logs/          # вивід команд build / run / ps / logs
screenshots/   # скріншоти терміналу для звіту
```

## Dockerfile

```dockerfile
FROM python:3.12-alpine
WORKDIR /app
COPY main.py .
RUN adduser -D appuser
USER appuser
ENV A=1 B=-3 C=2 PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
```

## Збірка і запуск

```bash
docker build -t quadratic-solver .
docker run --name quad-default quadratic-solver                         # x² - 3x + 2 = 0
docker run --name quad-two -e A=2 -e B=-7 -e C=3 quadratic-solver       # два корені
docker run --name quad-one -e A=1 -e B=2 -e C=1 quadratic-solver        # D = 0
docker run --name quad-none -e A=1 -e B=0 -e C=4 quadratic-solver       # D < 0
docker run --name quad-linear -e A=0 -e B=2 -e C=-4 quadratic-solver    # a = 0
docker logs quad-two
```

## Перевірені випадки

| A, B, C | D | Результат |
|---|---|---|
| 1, −3, 2 | 1 | x₁ = 2, x₂ = 1 |
| 2, −7, 3 | 25 | x₁ = 3, x₂ = 0.5 |
| 1, 2, 1 | 0 | x = −1 |
| 1, 0, 4 | −16 | дійсних коренів немає (0 ± 2i) |
| 0, 2, −4 | — | лінійне, x = 2 |
| A=abc | — | «Помилка: A='abc' не є числом», код виходу 1 |

## Прибирання

```bash
docker rm quad-default quad-two quad-one quad-none quad-linear quad-bad
docker rmi quadratic-solver
```
