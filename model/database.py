from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from fastapi import Depends
import os


# .env dosyasını yükle (local çalışırken)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy Engine oluştur
engine = create_engine(DATABASE_URL)

# SessionLocal, her istek için yeni bir oturum (session) sağlar
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI'de dependency olarak kullanılacak oturum alma fonksiyonu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
