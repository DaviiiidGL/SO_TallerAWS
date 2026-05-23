from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from .database import Base

class ImageRecord(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(100), nullable=False)
    nombre_imagen = Column(String(255), nullable=False)
    ruta_s3 = Column(String(500), nullable=False)
    fecha_creacion = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))