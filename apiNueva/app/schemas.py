from pydantic import BaseModel
from datetime import datetime

class ImageResponse(BaseModel):
    id: int
    usuario: str
    nombre_imagen: str
    ruta_s3: str
    fecha_creacion: datetime

    class Config:
        from_attributes = True