# Proyecto 0 de Nivelación ISIS4426

Este proyecto es parte del curso ISIS4426 y consiste en una aplicación web que incluye un **backend en Flask** y un **frontend en React**. Para ejecutar el proyecto en tu máquina local, sigue los pasos a continuación.

Video: https://youtu.be/UySf26TFezY

## Requisitos Previos

Antes de empezar, asegúrate de tener instalados los siguientes programas en tu máquina:

- [**Docker**](https://www.docker.com/get-started)  
- [**Docker Compose**](https://docs.docker.com/compose/install/)

## Instrucciones para Ejecutar el Proyecto

Sigue estos pasos para poner en marcha el proyecto:

### 1. Clonar el Repositorio

Clona el repositorio en tu máquina local utilizando el siguiente comando:

```
git clone https://github.com/tu-usuario/Proyecto0-ISIS4426.git
```

### 2. Verificar Instalación de docker

Asegúrate de que Docker y Docker Compose estén correctamente instalados en tu máquina. Puedes verificarlo ejecutando los siguientes comandos:

```
docker --version
docker-compose --version
```

### 3. Navegar al Directorio del Proyecto

Dirígete al directorio raíz del proyecto, donde se encuentra el archivo docker-compose.yml:

```
cd /ruta/a/Proyecto0-ISIS4426
```

### 4. Construir y Levantar los Contenedores

Para construir las imágenes Docker y levantar los contenedores, ejecuta el siguiente comando:

```
docker-compose up --build
```

### 5. Acceder a la Aplicación
Una vez que los contenedores estén en funcionamiento, podrás acceder a los siguientes servicios desde tu navegador:

- Frontend (React): http://localhost:3000
- Backend (Flask): http://localhost:5000
