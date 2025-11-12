from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from musica_api.database import SessionLocal, Cancion

router = APIRouter()


# ============================================
# MODELOS PYDANTIC (para validación)
# ============================================

class CancionBase(BaseModel):
    titulo: str
    artista: str
    duracion: int  # en segundos


class CancionCreate(CancionBase):
    pass


class CancionResponse(CancionBase):
    id: int
    
    class Config:
        from_attributes = True


# ============================================
# DEPENDENCIAS
# ============================================

def get_db():
    """Obtiene la sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================
# ENDPOINTS
# ============================================

@router.get("/", response_model=List[CancionResponse], tags=["Canciones"])
async def obtener_canciones(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todas las canciones.
    """
    canciones = db.query(Cancion).all()
    return canciones


@router.get("/{cancion_id}", response_model=CancionResponse, tags=["Canciones"])
async def obtener_cancion(cancion_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una canción específica por su ID.
    """
    cancion = db.query(Cancion).filter(Cancion.id == cancion_id).first()
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return cancion


@router.post("/", response_model=CancionResponse, tags=["Canciones"])
async def crear_cancion(cancion: CancionCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva canción.
    """
    nueva_cancion = Cancion(
        titulo=cancion.titulo,
        artista=cancion.artista,
        duracion=cancion.duracion
    )
    db.add(nueva_cancion)
    db.commit()
    db.refresh(nueva_cancion)
    return nueva_cancion


@router.put("/{cancion_id}", response_model=CancionResponse, tags=["Canciones"])
async def actualizar_cancion(cancion_id: int, cancion: CancionCreate, db: Session = Depends(get_db)):
    """
    Actualiza una canción existente.
    """
    cancion_db = db.query(Cancion).filter(Cancion.id == cancion_id).first()
    if not cancion_db:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    
    cancion_db.titulo = cancion.titulo
    cancion_db.artista = cancion.artista
    cancion_db.duracion = cancion.duracion
    db.commit()
    db.refresh(cancion_db)
    return cancion_db


@router.delete("/{cancion_id}", tags=["Canciones"])
async def eliminar_cancion(cancion_id: int, db: Session = Depends(get_db)):
    """
    Elimina una canción.
    """
    cancion = db.query(Cancion).filter(Cancion.id == cancion_id).first()
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    
    db.delete(cancion)
    db.commit()
    return {"mensaje": "Canción eliminada correctamente"}
