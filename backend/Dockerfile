# Usa una imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . .

# Instala las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que Flask corre (usualmente 5000)
EXPOSE 5000

# Define el comando para ejecutar tu aplicación con `run.py`
CMD ["python", "run.py"]
