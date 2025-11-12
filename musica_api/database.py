from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

# Función para probar la conexión
def test_connection():
    try:
        with engine.connect() as conn:
            print("✅ Conexión exitosa a la base de datos:", settings.database_url)
    except Exception as e:
        print("❌ Error al conectar a la base de datos:", e)
