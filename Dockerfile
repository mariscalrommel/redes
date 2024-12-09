# Usar una imagen base de Python
FROM python:3.10-slim
WORKDIR /app
COPY . /app
EXPOSE 25545
CMD ["python", "ConectarWifi_EnvioDeDatos.py"]
