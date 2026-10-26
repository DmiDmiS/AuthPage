# === Этап 1: Сборка зависимостей ===
FROM python:3.11-slim AS builder

WORKDIR /app

# Запрещаем Python писать файлы .pyc на диск и настраиваем буферизацию логов для контейнеров
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем базовые инструменты для сборки пакетов
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

# Собираем колеса (wheels) пакетов в отдельную папку
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# === Этап 2: Финальный минимальный образ ===
FROM python:3.11-slim

WORKDIR /app

# Создаем системную группу и пользователя, под которым будет работать приложение (Security Best Practice)
RUN groupadd -r sreuser && useradd -r -g sreuser sreuser

# Копируем собранные пакеты из первого этапа и устанавливаем их
COPY --from=builder /app/wheels /images/wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /images/wheels/*

# Копируем код нашего приложения
COPY . .

# Меняем владельца папки на созданного пользователя
RUN chown -R sreuser:sreuser /app

# Переключаемся на безопасного пользователя (теперь приложение работает не из-под root)
USER sreuser

# Открываем порт для Django наружу
EXPOSE 8000

# Запускаем сервер разработки Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
