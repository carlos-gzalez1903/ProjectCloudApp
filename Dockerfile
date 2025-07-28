# Usa una imagen oficial de Python
FROM python:3.9-slim

# Directorio de trabajo
WORKDIR ./

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de archivos
COPY . .

# Puerto expuesto (Fly usa 8080 por defecto)
EXPOSE 8080

# Comando para ejecutar la app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
