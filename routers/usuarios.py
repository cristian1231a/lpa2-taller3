from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from musica_api.database import SessionLocal, Usuario

router = APIRouter()


# ============================================
# MODELOS PYDANTIC (para validación)
# ============================================

class UsuarioBase(BaseModel):
    nombre: str
    email: str


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioResponse(UsuarioBase):
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

@router.get("/", response_model=List[UsuarioResponse], tags=["Usuarios"])
async def obtener_usuarios(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los usuarios.
    """
    usuarios = db.query(Usuario).all()
    return usuarios


@router.get("/{usuario_id}", response_model=UsuarioResponse, tags=["Usuarios"])
async def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un usuario específico por su ID.
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("/", response_model=UsuarioResponse, tags=["Usuarios"])
async def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario.
    """
    # Verificar si el email ya existe
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    nuevo_usuario = Usuario(nombre=usuario.nombre, email=usuario.email)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse, tags=["Usuarios"])
async def actualizar_usuario(usuario_id: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Actualiza un usuario existente.
    """
    usuario_db = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario_db.nombre = usuario.nombre
    usuario_db.email = usuario.email
    db.commit()
    db.refresh(usuario_db)
    return usuario_db


@router.delete("/{usuario_id}", tags=["Usuarios"])
async def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Elimina un usuario.
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado correctamente"}
