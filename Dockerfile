# Utiliza la imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala las dependencias necesarias
RUN pip install --no-cache-dir flask python-dotenv openai flask-cors

# Copia el código fuente al contenedor
COPY . .

# Ejecuta el comando para iniciar tu programa Python
CMD [ "python3", "main.py" ]