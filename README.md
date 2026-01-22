# TAI - Educational Coding Platform

An educational platform where teachers create coding exercises and students solve them with integrated code editing, testing, and progressive. User configuration is not implemented, every user can create, perform, and update exercises.

## Features

- **Multi-language support**: C, Java, and Python
- **Exercise creation**: Teachers can create exercises with multiple files, test cases, and progressive hints
- **Automated testing**: Student code is compiled and tested against predefined test cases

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│    Frontend     │────▶│     Backend      │───▶│   PostgreSQL    │
│   (Angular 20)  │◀────│    (FastAPI)     │◀───│    Database     │
│   Port 4200     │     │    Port 8000     │     │   Port 5432     │
└─────────────────┘     └────────┬─────────┘     └─────────────────┘
                                 │
                        ┌────────▼─────────┐
                        │  Code Compiler   │
                        │  gcc/javac/py    │
                        └──────────────────┘
```

## Quick Start with Docker

### Prerequisites
- Docker
- Docker Compose

### Start the application

1. **Clone the repository** 

2. **Run docker-compose**:
   ```bash
   docker-compose up 
   ```

3. **Access the application**:
   - Frontend: http://localhost:4200
   - Backend : http://localhost:8000
   - Backend API docs: http://localhost:8000/docs

### Stop the application

```bash
docker-compose down
```

### Reset the database

The database is automatically initialized with sample data from `init.sql`. To reset:
```bash
docker-compose down
docker-compose up 
```

> **Note**: By default, data is not persisted between restarts. To enable persistence, uncomment the volume configuration in `docker-compose.yml`.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | Angular 20, TypeScript, TailwindCSS |
| Backend | FastAPI, Python 3.11, SQLAlchemy |
| Database | PostgreSQL 15 |
| Compilers | GCC, OpenJDK 17, Python 3 |

## Project Structure

```
tai2/
├── frontend/          # Angular frontend application
├── backend/           # FastAPI backend API
├── init.sql           # Database schema and seed data
├── docker-compose.yml 
└── README.md          
```

## Development (without Docker)

See individual README files:
- [Frontend README](frontend/README.md)
- [Backend README](backend/README.md)
