FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias primero (para cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto
COPY . .

# Puerto para Fly.io
EXPOSE 8080

# Comando de inicio (¡usa el nombre correcto de tu módulo!)
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]