# Sistema de Votaciones — API RESTful

API para gestionar un sistema de votaciones: registro de votantes y candidatos, emisión de un único voto por votante, y estadísticas de resultados.

**Stack:** Python 3.11+, FastAPI, SQLAlchemy, PostgreSQL, JWT (autenticación).

## Requisitos previos

- Python 3.10+
- PostgreSQL corriendo localmente (o accesible por red)

## Instalación y ejecución local

1. Clonar el repositorio y entrar a la carpeta del proyecto.

2. Crear un entorno virtual e instalar dependencias:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # En Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Crear la base de datos en PostgreSQL:

   ```sql
   CREATE DATABASE voting_db;
   ```

4. Copiar el archivo de variables de entorno y ajustarlo con tus credenciales:

   ```bash
   cp .env.example .env
   ```

   Variables disponibles en `.env`:

   | Variable | Descripción | Valor por defecto |
   |---|---|---|
   | `DATABASE_URL` | Cadena de conexión a PostgreSQL | `postgresql+psycopg2://postgres:postgres@localhost:5432/voting_db` |
   | `JWT_SECRET_KEY` | Clave secreta para firmar los tokens JWT | — (cámbiala) |
   | `JWT_ALGORITHM` | Algoritmo de firma | `HS256` |
   | `JWT_EXPIRE_MINUTES` | Minutos de validez del token | `60` |
   | `ADMIN_USERNAME` / `ADMIN_PASSWORD` | Credenciales del usuario administrador para obtener el token | `admin` / `admin123` |

5. Levantar el servidor (las tablas se crean automáticamente al iniciar):

   ```bash
   uvicorn app.main:app --reload
   ```

   La API queda disponible en `http://localhost:8000`.

6. Documentación interactiva (Swagger UI): `http://localhost:8000/docs`

## Autenticación

Todos los endpoints (excepto `/auth/login`) requieren un token JWT.

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Respuesta:

```json
{ "access_token": "eyJhbGciOi...", "token_type": "bearer" }
```

Usa ese token en cada request siguiente:

```bash
-H "Authorization: Bearer <access_token>"
```

## Endpoints

### Votantes

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/voters` | Registrar un votante |
| GET | `/voters` | Listar votantes |
| GET | `/voters/{id}` | Obtener un votante |
| DELETE | `/voters/{id}` | Eliminar un votante |

```bash
curl -X POST http://localhost:8000/voters \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "Ana Gomez", "email": "ana@example.com"}'

curl http://localhost:8000/voters -H "Authorization: Bearer $TOKEN"

curl http://localhost:8000/voters/1 -H "Authorization: Bearer $TOKEN"

curl -X DELETE http://localhost:8000/voters/1 -H "Authorization: Bearer $TOKEN"
```

### Candidatos

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/candidates` | Registrar un candidato |
| GET | `/candidates` | Listar candidatos |
| GET | `/candidates/{id}` | Obtener un candidato |
| DELETE | `/candidates/{id}` | Eliminar un candidato |

```bash
curl -X POST http://localhost:8000/candidates \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "Carlos Ruiz", "party": "Partido A", "email": "carlos@example.com"}'
```

> `email` en candidatos es opcional y se usa junto con el nombre para verificar que la misma persona no esté registrada como votante y candidato a la vez.

### Votos

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/votes` | Emitir un voto |
| GET | `/votes` | Listar todos los votos |
| GET | `/votes/statistics` | Estadísticas de la votación |

```bash
curl -X POST http://localhost:8000/votes \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d '{"voter_id": 1, "candidate_id": 1}'

curl http://localhost:8000/votes/statistics -H "Authorization: Bearer $TOKEN"
```

Respuesta de ejemplo de `/votes/statistics`:

```json
{
  "total_votes": 2,
  "total_voters_voted": 2,
  "results": [
    { "candidate_id": 1, "name": "Carlos Ruiz", "votes": 1, "percentage": 50.0 },
    { "candidate_id": 2, "name": "Maria Lopez", "votes": 1, "percentage": 50.0 }
  ]
}
```

## Reglas de negocio y validaciones

- Email único por votante; email único por candidato (cuando se provee).
- Una misma persona no puede registrarse a la vez como votante y como candidato (se valida por nombre y, si se provee, por email).
- Un votante solo puede votar una vez (`has_voted`); intentar votar de nuevo devuelve `409`.
- `voter_id` / `candidate_id` inexistentes devuelven `404` al votar, consultar o eliminar.
- Al emitir un voto: se crea el registro de voto, se marca `has_voted = true` en el votante y se incrementa `votes` en el candidato, en una sola transacción.
- Errores de validación de formato (campos faltantes, email inválido, etc.) devuelven `422` automáticamente.

## Estructura del proyecto

```
app/
  main.py          # Punto de entrada, registro de routers
  config.py        # Configuración desde variables de entorno
  database.py      # Conexión y sesión de SQLAlchemy
  models.py        # Modelos ORM: Voter, Candidate, Vote
  schemas.py       # Esquemas Pydantic de entrada/salida
  security.py      # Emisión y verificación de JWT
  crud.py          # Lógica de negocio y acceso a datos
  routers/
    auth.py
    voters.py
    candidates.py
    votes.py
```

## Capturas de las estadísticas
<img width="1317" height="491" alt="image" src="https://github.com/user-attachments/assets/8038897b-677e-410d-9954-89522aa09ea8" />

