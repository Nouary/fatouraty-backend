from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env
load_dotenv('.env.local')  # Load .env.local for local overrides

# Use DATABASE_URL from environment
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL not configured in environment")

print(f"Database URL: {SQLALCHEMY_DATABASE_URL[:50]}..." if len(SQLALCHEMY_DATABASE_URL) > 50 else f"Database URL: {SQLALCHEMY_DATABASE_URL}")

# Configure engine based on database type
if SQLALCHEMY_DATABASE_URL.startswith("postgresql"):
    # PostgreSQL configuration for Neon
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        connect_args={"sslmode": "require"} if "sslmode=require" not in SQLALCHEMY_DATABASE_URL else {},
        echo=False,
    )
else:
    # Fallback for other databases (though we expect PostgreSQL)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()