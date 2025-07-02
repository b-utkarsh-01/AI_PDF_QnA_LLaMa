from sqlalchemy import Column, Integer, String, DateTime, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Declare base
Base = declarative_base()

# Document model
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)
    text = Column(Text, nullable=True)

# SQLite DB path
DATABASE_URL = "sqlite:///./pdf_docs.db"

# Create engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Create tables if not exist
def create_tables():
    Base.metadata.create_all(bind=engine)