# Build stage
FROM python:3.13 AS builder

WORKDIR /secunda_test

# Установка системных библиотек
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    default-mysql-client \
    libmariadb-dev-compat \
    iputils-ping \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir cryptography

# Копируем приложение
COPY . .

# Runtime stage
FROM python:3.13

WORKDIR /secunda_test

# Установка системных библиотек (чтобы runtime образ тоже мог запускать нужные инструменты)
RUN apt-get update && apt-get install -y \
    libssl-dev \
    libffi-dev \
    default-mysql-client \
    libmariadb-dev-compat \
    iputils-ping \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости из builder
COPY --from=builder /usr/local /usr/local
COPY --from=builder /secunda_test /secunda_test

# Переменные окружения
ENV PATH=/usr/local/bin:$PATH
ENV MYSQL_HOST=mysql
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=12345
ENV MYSQL_DATABASE=secunda
ENV PYTHONPATH=/secunda_test/app

# Копируем скрипт ожидания базы
COPY app/wait-for-db.sh /secunda_test/app/wait-for-db.sh
RUN chmod +x /secunda_test/app/wait-for-db.sh

EXPOSE 8000

# Команда запуска
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
