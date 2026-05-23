import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import ImageRecord
from .s3_service import upload_file_to_s3, generate_presigned_url

app = FastAPI(title="Taller AWS FastAPI")

ALLOWED_CONTENT_TYPES = ["image/png", "image/jpeg"]
ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg"]

@app.post("/upload")
async def upload_image(
    usuario: str = Form(...),
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    extension = os.path.splitext(imagen.filename)[1].lower()

    if imagen.content_type not in ALLOWED_CONTENT_TYPES or extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail="Formato inválido. Solo se permiten PNG y JPG/JPEG."
        )

    s3_key = f"{usuario}/{imagen.filename}"
    upload_file_to_s3(imagen.file, s3_key, imagen.content_type)

    record = ImageRecord(
        usuario=usuario,
        nombre_imagen=imagen.filename,
        ruta_s3=s3_key
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "mensaje": "Imagen cargada correctamente",
        "id": record.id,
        "usuario": record.usuario,
        "ruta_s3": record.ruta_s3,
        "fecha_creacion": record.fecha_creacion
    }

@app.get("/image")
def get_image(usuario: str, nombre_imagen: str, db: Session = Depends(get_db)):
    record = db.query(ImageRecord).filter(
        ImageRecord.usuario == usuario,
        ImageRecord.nombre_imagen == nombre_imagen
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el usuario o la imagen solicitada."
        )

    url = generate_presigned_url(record.ruta_s3)

    if not url:
        raise HTTPException(
            status_code=500,
            detail="No se pudo generar la URL prefirmada."
        )

    return {
        "usuario": record.usuario,
        "nombre_imagen": record.nombre_imagen,
        "fecha_creacion": record.fecha_creacion,
        "url": url
    }