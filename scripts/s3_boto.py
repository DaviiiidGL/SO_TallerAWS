from pathlib import Path
from datetime import datetime
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

BUCKET_NAME = "user-1027741071-ueia-so"
AWS_REGION = "us-east-1"

BASE_DIR = Path(__file__).resolve().parent.parent
ORIGEN_DIR = BASE_DIR / "data" / "origen"
DESTINO_DIR = BASE_DIR / "data" / "destino"

s3 = boto3.client("s3", region_name=AWS_REGION)

# Posibles errores con el bucket
def verificar_bucket(bucket_name: str):
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"[OK] Bucket accesible: {bucket_name}")
    except ClientError as e:
        print(f"[ERROR] No se pudo acceder al bucket: {bucket_name}")
        raise e

# Subir un archivo local a AWS
def subir_archivo(local_path: Path, s3_key: str):
    s3.upload_file(str(local_path), BUCKET_NAME, s3_key)
    print(f"[UPLOAD OK] {local_path.name} -> s3://{BUCKET_NAME}/{s3_key}")

# AWS a local
def descargar_archivo(s3_key: str, local_path: Path):
    local_path.parent.mkdir(parents=True, exist_ok=True)
    s3.download_file(BUCKET_NAME, s3_key, str(local_path))
    print(f"[DOWNLOAD OK] s3://{BUCKET_NAME}/{s3_key} -> {local_path}")

# Ver objetos que hay en:
def listar_objetos(prefijo: str = ""):
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefijo)
    print("\n[LISTADO S3]")
    if "Contents" not in response:
        print("No hay objetos en ese prefijo.")
        return
    for obj in response["Contents"]:
        print(f"- {obj['Key']} ({obj['Size']} bytes)")


def verificar_archivo_local(path: Path):
    if path.exists():
        print(f"[LOCAL OK] Existe: {path}")
        print(f"[CONTENIDO] {path.read_text(encoding='utf-8')}")
    else:
        print(f"[LOCAL ERROR] No existe: {path}")


def main():
    try:
        print("=== DEMO BOTO3 S3 ===")
        print(f"Fecha/hora: {datetime.now()}")
        print(f"Origen: {ORIGEN_DIR}")
        print(f"Destino: {DESTINO_DIR}\n")

        verificar_bucket(BUCKET_NAME)

        # 1. Subir un archivo
        archivo_unico = ORIGEN_DIR / "Prueba.txt"
        key_unica = "boto3-demo/prueba.txt"
        subir_archivo(archivo_unico, key_unica)

        # 2. Verificar
        listar_objetos("boto3-demo/")

        # 3. Descargar a otra carpeta
        destino_unico = DESTINO_DIR / "prueba_descargada.txt"
        descargar_archivo(key_unica, destino_unico)

        # 4. Verificar descarga
        verificar_archivo_local(destino_unico)

        # 5. Subir y descargar 3 archivos de texto
        multiples = ["texto1.txt", "texto2.txt", "texto3.txt"]

        print("\n=== MULTIPLES ARCHIVOS ===")
        for nombre in multiples:
            origen = ORIGEN_DIR / nombre
            key = f"boto3-demo/multiples/{nombre}"
            subir_archivo(origen, key)

        listar_objetos("boto3-demo/multiples/")

        for nombre in multiples:
            key = f"boto3-demo/multiples/{nombre}"
            destino = DESTINO_DIR / nombre
            descargar_archivo(key, destino)

        print("\n=== VERIFICACION LOCAL MULTIPLES ===")
        for nombre in multiples:
            verificar_archivo_local(DESTINO_DIR / nombre)

        print("\n[FIN OK] Proceso completado correctamente.")

    except NoCredentialsError:
        print("[ERROR] No se encontraron credenciales AWS configuradas.")
    except ClientError as e:
        print(f"[ERROR AWS] {e}")
    except Exception as e:
        print(f"[ERROR GENERAL] {e}")


if __name__ == "__main__":
    main()