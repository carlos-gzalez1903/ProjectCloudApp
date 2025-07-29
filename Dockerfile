FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Usa PORT de las variables de entorno o 8080 por defecto
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8080} --access-logfile - --error-logfile - app:app"]