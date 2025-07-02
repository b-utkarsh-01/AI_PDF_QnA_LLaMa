from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# SQLite database URL
DATABASE_URL = "sqlite:///./pdf_docs.db"

# Create the database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session factory for DB operations
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Function to create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)
