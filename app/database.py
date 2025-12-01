from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings


# Create the engine sqlAlchemy to communicate with postgresql
engine = create_engine(settings.DATABASE_URL)

# Each API requets will have it's own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Parent classe which all my models (tables) will inherit.
# Allow sqlAlchemy to know which classes correspond to SQL tables
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()