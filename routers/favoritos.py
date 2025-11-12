from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from musica_api.database import SessionLocal, Favorito, Usuario, Cancion

router = APIRouter()


# ============================================
# MODELOS PYDANTIC (para validación)
# ============================================

class FavoritoBase(BaseModel):
    usuario_id: int
    cancion_id: int


class FavoritoCreate(FavoritoBase):
    pass


class FavoritoResponse(FavoritoBase):
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

@router.get("/", response_model=List[FavoritoResponse], tags=["Favoritos"])
async def obtener_favoritos(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los favoritos.
    """
    favoritos = db.query(Favorito).all()
    return favoritos


@router.get("/usuario/{usuario_id}", response_model=List[FavoritoResponse], tags=["Favoritos"])
async def obtener_favoritos_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los favoritos de un usuario específico.
    """
    # Verificar que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    favoritos = db.query(Favorito).filter(Favorito.usuario_id == usuario_id).all()
    return favoritos


@router.post("/", response_model=FavoritoResponse, tags=["Favoritos"])
async def crear_favorito(favorito: FavoritoCreate, db: Session = Depends(get_db)):
    """
    Añade una canción a los favoritos de un usuario.
    """
    # Verificar que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id == favorito.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar que la canción existe
    cancion = db.query(Cancion).filter(Cancion.id == favorito.cancion_id).first()
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    
    # Verificar que no se repita
    favorito_existente = db.query(Favorito).filter(
        Favorito.usuario_id == favorito.usuario_id,
        Favorito.cancion_id == favorito.cancion_id
    ).first()
    if favorito_existente:
        raise HTTPException(status_code=400, detail="Esta canción ya está en favoritos")
    
    nuevo_favorito = Favorito(usuario_id=favorito.usuario_id, cancion_id=favorito.cancion_id)
    db.add(nuevo_favorito)
    db.commit()
    db.refresh(nuevo_favorito)
    return nuevo_favorito


@router.delete("/{favorito_id}", tags=["Favoritos"])
async def eliminar_favorito(favorito_id: int, db: Session = Depends(get_db)):
    """
    Elimina una canción de los favoritos.
    """
    favorito = db.query(Favorito).filter(Favorito.id == favorito_id).first()
    if not favorito:
        raise HTTPException(status_code=404, detail="Favorito no encontrado")
    
    db.delete(favorito)
    db.commit()
    return {"mensaje": "Favorito eliminado correctamente"}
