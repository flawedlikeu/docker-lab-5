# Практична №5, варіант 5 — Володимир ЧАБАН, З-41
FROM python:3.12-alpine

WORKDIR /app
COPY main.py .

# не запускати програму від root
RUN adduser -D appuser
USER appuser

# значення за замовчуванням: x² - 3x + 2 = 0
ENV A=1 B=-3 C=2 PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
