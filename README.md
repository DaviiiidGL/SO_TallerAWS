# Taller AWS 2026 – Gestión de archivos en S3 y despliegue de FastAPI en EC2/Lambda
Las capturas se encuentran en `Capturas.md`

Este repositorio contiene el desarrollo del taller de **Sistemas Operativos – AWS 2026**. El proyecto cubre tres partes principales: gestión de archivos en Amazon S3, despliegue de una aplicación FastAPI en Amazon EC2 y desarrollo/despliegue de una API FastAPI contenerizada en AWS Lambda usando Amazon ECR y una Function URL pública.[1]

## Objetivos del taller

El taller solicita implementar operaciones de carga y descarga de archivos en Amazon S3 usando tanto AWS CLI como boto3, desplegar una aplicación FastAPI en una instancia EC2 y construir una segunda aplicación FastAPI que almacene imágenes en S3, registre metadatos en RDS y se despliegue en Lambda mediante una imagen Docker publicada en ECR.[1]

## Contenido esperado del repositorio

De acuerdo con el enunciado, el repositorio debe incluir como mínimo el código fuente, los scripts utilizados, el `Dockerfile`, los archivos de configuración, las instrucciones de ejecución en este `README` y la evidencia o documentación requerida, como capturas de pantalla o entregables equivalentes.[1]

Una estructura sugerida del proyecto es la siguiente:

```text
.
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── s3_service.py
├── scripts/
│   ├── s3_cli_examples.sh
│   └── s3_boto3_examples.py
├── evidence/
│   ├── s3/
│   ├── ec2/
│   └── lambda/
├── requirements.txt
├── Dockerfile
└── README.md
```

## 1. Gestión de archivos en Amazon S3

### 1.1 Creación del bucket

El taller pide crear un bucket con el patrón `user-########-ueia-so`, donde `########` sea un identificador único, por ejemplo un número aleatorio o la cédula.[1]

Ejemplo:

```bash
aws s3 mb s3://user-12345678-ueia-so --region us-east-1
```

### 1.2 Operaciones con AWS CLI

Se debe demostrar la carga de un archivo al bucket, verificar que el archivo quedó almacenado, descargarlo en una carpeta diferente y comprobar que la descarga se realizó correctamente.[1]

Ejemplo de carga:

```bash
aws s3 cp archivo.txt s3://user-12345678-ueia-so/
```

Ejemplo de verificación:

```bash
aws s3 ls s3://user-12345678-ueia-so/
```

Ejemplo de descarga:

```bash
aws s3 cp s3://user-12345678-ueia-so/archivo.txt ./descargas/archivo.txt
```

Cuando se trabaja con múltiples archivos, cambia principalmente la forma de invocar el comando: en lugar de transferir un solo archivo, se puede usar copia recursiva o patrones por carpeta para subir o descargar varios recursos a la vez.[1]

Ejemplo práctico de múltiples archivos:

```bash
aws s3 cp ./carpeta-local s3://user-12345678-ueia-so/carpeta-local --recursive
aws s3 cp s3://user-12345678-ueia-so/carpeta-local ./descargas/carpeta-local --recursive
```

### 1.3 Operaciones con boto3

El enunciado también exige cargar y descargar archivos usando boto3, verificar el resultado y realizar una prueba con tres archivos de texto, explicando las diferencias cuando se manipulan múltiples archivos.[1]

Ejemplo mínimo en Python:

```python
import boto3

s3 = boto3.client("s3")
bucket = "user-12345678-ueia-so"

# Subir archivo
s3.upload_file("archivo1.txt", bucket, "archivo1.txt")

# Descargar archivo
s3.download_file(bucket, "archivo1.txt", "./descargas/archivo1.txt")
```

Para múltiples archivos, normalmente se recorre una lista de nombres o rutas y se ejecuta la operación para cada elemento, manteniendo la misma lógica pero dentro de un ciclo.[1]

## 2. Despliegue de FastAPI en Amazon EC2

El taller pide tomar la aplicación FastAPI compartida en la carpeta `test_docker_fastapi`, subirla a GitHub, crear una instancia EC2, clonar el repositorio en la instancia y realizar todas las configuraciones necesarias para ejecutar correctamente la aplicación.[1]

### 2.1 Requisitos solicitados

Se deben documentar dependencias, entorno, puertos, permisos y demás ajustes necesarios para que la aplicación corra en EC2, además de configurar un daemon o servicio que arranque automáticamente con la instancia.[1]

También se deben hacer los cambios necesarios en la instancia o en el Security Group para permitir acceso mediante la IP pública, y documentar dichas configuraciones con capturas de pantalla.[1]

### 2.2 Flujo sugerido

1. Crear la instancia EC2.
2. Conectarse por SSH.
3. Instalar Python, pip, Git y dependencias del proyecto.
4. Clonar el repositorio desde GitHub.
5. Crear entorno virtual e instalar dependencias.
6. Probar la app localmente.
7. Configurar un servicio `systemd` para arranque automático.
8. Abrir el puerto necesario en el Security Group.[1]

Ejemplo de ejecución manual:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 3. Desarrollo y despliegue de FastAPI con S3, RDS, Docker, ECR y Lambda

### 3.1 Endpoint POST

Se debe implementar un endpoint `POST` que reciba el nombre de un usuario y una imagen en formato PNG o JPG/JPEG, validando que solo se acepten esos formatos y retornando un error HTTP del lado del cliente en caso de formato inválido.[1]

Además, el endpoint debe almacenar la imagen en un bucket S3 organizado por usuario y registrar en Amazon RDS, como mínimo, los campos `id`, `usuario`, `ruta de la imagen en S3` y `fecha de creación`.[1]

### 3.2 Endpoint GET

Se debe implementar un endpoint `GET` que reciba nombre de usuario y nombre de imagen, consulte la ubicación en la base de datos, devuelva un mensaje claro si el usuario o la imagen no existen y retorne una URL de acceso a la imagen, por ejemplo una URL prefirmada, junto con la fecha de almacenamiento registrada en RDS.[1]

### 3.3 Contenerización

El taller exige crear una imagen Docker para ejecutar la aplicación y validar su funcionamiento usando `docker build` y `docker run`.[1]

Ejemplo:

```bash
docker build -t fastapi-aws-taller .
docker run -p 8000:8000 fastapi-aws-taller
```

### 3.4 Publicación en ECR

La imagen debe publicarse en un repositorio de Amazon ECR.[1]

Ejemplo de flujo:

```bash
aws ecr get-login-password --region us-east-1 | \
docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

docker buildx build \
  --platform linux/amd64 \
  --provenance=false \
  -t <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/fastapi-aws-taller:lambda \
  --push .
```

### 3.5 Despliegue en Lambda

La función Lambda debe crearse usando la imagen almacenada en ECR y debe configurarse con una URL pública para invocación, además de realizar todas las configuraciones necesarias para garantizar el funcionamiento correcto de la aplicación.[1]

Esto incluye, como mínimo, revisar variables de entorno, role de ejecución, permisos de acceso a S3, conectividad hacia RDS, timeout, memoria y permisos asociados a la Function URL.[1]

## Variables de entorno sugeridas

El siguiente bloque ilustra variables típicas para una solución de este tipo:

```env
AWS_REGION=us-east-1
S3_BUCKET=user-12345678-ueia-so
DB_HOST=xxxxxxxx.us-east-1.rds.amazonaws.com
DB_PORT=3306
DB_NAME=nombre_bd
DB_USER=admin
DB_PASSWORD=xxxxxxxx
```

En un entorno productivo sobre Lambda, estas variables deben configurarse directamente en AWS Lambda o mediante un servicio de secretos, en lugar de depender exclusivamente de un archivo local `.env`.[1]
