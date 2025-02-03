# Usa una imagen base de Node.js
FROM node:18

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo package.json y package-lock.json (si existe)
COPY package*.json ./

# Instala las dependencias de npm ignorando los conflictos de dependencias
RUN npm install --legacy-peer-deps

# Copia el resto de los archivos del proyecto al contenedor
COPY . .

# Expone el puerto en el que React corre (usualmente 3000)
EXPOSE 3000

# Define el comando para ejecutar la aplicación en modo desarrollo
CMD ["npm", "start"]
