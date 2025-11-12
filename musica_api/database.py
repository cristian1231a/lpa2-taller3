from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from musica_api.config import get_settings

# Obtener la configuración desde settings.py
settings = get_settings()

# Crear el motor de conexión a la base de datos SQLite
# (el archivo debe estar en el mismo directorio del proyecto)
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # Requerido por SQLite
)

# Crear una sesión local (para ejecutar consultas)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 4️⃣ Declarar la clase base para los modelos
Base = declarative_base()


# ============================================
# DEFINICIÓN DE MODELOS (TABLAS)
# ============================================

class Usuario(Base):
    """Modelo para la tabla de usuarios."""
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    
    # Relaciones
    favoritos = relationship("Favorito", back_populates="usuario")


class Cancion(Base):
    """Modelo para la tabla de canciones."""
    __tablename__ = "cancion"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    artista = Column(String(100), nullable=False)
    duracion = Column(Integer)  # en segundos
    
    # Relaciones
    favoritos = relationship("Favorito", back_populates="cancion")


class Favorito(Base):
    """Modelo para la tabla de favoritos (relación muchos a muchos entre usuarios y canciones)."""
    __tablename__ = "favorito"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    cancion_id = Column(Integer, ForeignKey("cancion.id"), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="favoritos")
    cancion = relationship("Cancion", back_populates="favoritos")


# Función para crear todas las tablas
def create_db_and_tables():
    """
    Crea todas las tablas en la base de datos si no existen.
    Se debe ejecutar al iniciar la aplicación.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente")


# Función para probar la conexión
def test_connection():
    """Prueba la conexión a la base de datos."""
    try:
        with engine.connect() as conn:
            print("✅ Conexión exitosa a la base de datos:", settings.database_url)
    except Exception as e:
        print("❌ Error al conectar a la base de datos:", e)
