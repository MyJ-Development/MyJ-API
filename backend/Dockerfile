# Comenzamos con una imagen base de Python
FROM python:3.8-buster

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crear directorio para la aplicación
RUN mkdir /app
WORKDIR /app

# Instalar dependencias
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copiar el proyecto
COPY . /app/

# Exponer el puerto donde la app va a ser servida
EXPOSE 3011

# Comando para iniciar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:3011"]
