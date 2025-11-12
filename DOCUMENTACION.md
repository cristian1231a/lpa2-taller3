"""
FLUJO DE CONEXIÓN A LA BASE DE DATOS
====================================

1. CONFIGURACIÓN (config.py)
   - database_url: str = "sqlite:///./database.sqlite"
   
2. CONEXIÓN (database.py)
   - engine = create_engine(settings.database_url)
   - SessionLocal = sessionmaker(bind=engine)
   
3. MODELOS (database.py)
   - Usuario (tabla: usuario)
     * id (PK)
     * nombre
     * email
   
   - Cancion (tabla: cancion)
     * id (PK)
     * titulo
     * artista
     * duracion
   
   - Favorito (tabla: favorito)
     * id (PK)
     * usuario_id (FK -> usuario.id)
     * cancion_id (FK -> cancion.id)

4. ROUTERS (routers/)
   - usuarios.py -> GET/POST/PUT/DELETE /api/usuarios
   - canciones.py -> GET/POST/PUT/DELETE /api/canciones
   - favoritos.py -> GET/POST/PUT/DELETE /api/favoritos

5. APLICACIÓN PRINCIPAL (main.py)
   - Importa los routers
   - Registra los routers en la app
   - Al iniciar: crea_db_and_tables()


ENDPOINTS DISPONIBLES
====================

USUARIOS:
  GET    /api/usuarios             - Obtener todos los usuarios
  GET    /api/usuarios/{id}        - Obtener un usuario por ID
  POST   /api/usuarios             - Crear nuevo usuario
  PUT    /api/usuarios/{id}        - Actualizar usuario
  DELETE /api/usuarios/{id}        - Eliminar usuario

CANCIONES:
  GET    /api/canciones            - Obtener todas las canciones
  GET    /api/canciones/{id}       - Obtener una canción por ID
  POST   /api/canciones            - Crear nueva canción
  PUT    /api/canciones/{id}       - Actualizar canción
  DELETE /api/canciones/{id}       - Eliminar canción

FAVORITOS:
  GET    /api/favoritos            - Obtener todos los favoritos
  GET    /api/favoritos/usuario/{usuario_id} - Favoritos de un usuario
  POST   /api/favoritos            - Añadir canción a favoritos
  DELETE /api/favoritos/{id}       - Eliminar favorito


EJEMPLOS DE USO
===============

1. Crear un usuario:
   POST /api/usuarios
   {
     "nombre": "Juan Pérez",
     "email": "juan@example.com"
   }

2. Crear una canción:
   POST /api/canciones
   {
     "titulo": "Bohemian Rhapsody",
     "artista": "Queen",
     "duracion": 354
   }

3. Añadir canción a favoritos:
   POST /api/favoritos
   {
     "usuario_id": 1,
     "cancion_id": 1
   }

4. Obtener favoritos de un usuario:
   GET /api/favoritos/usuario/1
"""
