# TAI - Educational Coding Platform Backend

A FastAPI backend for an educational coding exercise platform. It enables "teachers" to create coding exercises and "students" to solve them with integrated code editing, testing, and progressive hints. 


## Technology Stack

- **Framework:** FastAPI (Python 3.10)
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Validation:** Pydantic v2
- **Migrations:** Alembic



## Installation

I recommend using the docker-compose file located at the root of this repository. However, if you want to start only the backend:

### Prerequisites

- Python 3.10
- PostgreSQL 13+
- Compilers: gcc, javac, python3

### Steps

**Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

**Configure environment variables** - Create a `.env` file:
   ```env
   DB_URL='postgresql+psycopg2://username:password@localhost:5432/tai_db'
   ```

**Create and feel the database**:
   ```bash
   createdb tai_db
   ```

   **Option A** - Using init.sql (includes sample data):
   ```bash
   psql -U username -d tai_db -f ../init.sql
   ```

   **Option B** - Using Alembic migrations (schema only, no sample data):
   ```bash
   alembic upgrade head
   ```

## Running the Server

```bash
fastapi dev app/main.py
```


## Project Structure

```
app/
├── main.py                 # FastAPI app + all route definitions
├── core/
│   ├── config.py           # Pydantic settings (loads .env)
│   └── enums.py            
├── db/
│   ├── database.py         # SQLAlchemy engine + session dependency
│   └── models.py           # 11 ORM models (SQLAlchemy)
├── schemas/
│   └── schemas.py          # Pydantic request/response models
├── services/               
│   ├── create_exercise.py  # Exercise CRU operations
│   ├── compiler.py         # Code compilation (gcc, javac, python3)
│   ├── exercise_run.py     # Student submission handling & grading
│   ├── unit_update.py      # Unit/Course CUD operations
│   └── info_navigation.py  # Navigation queries (dashboard)
└── utils/
    ├── synthax_code.py     # Syntax 
    └── parsing.py          # Marker extraction from code
```



## Supported Languages:

| Language | Extension | Compiler | Comment Style |
|----------|-----------|----------|---------------|
| C        | `.c`      | gcc      | `// comment`  |
| Java     | `.java`   | javac    | `// comment`  |
| Python   | `.py`     | python3  | `# comment`   |



