from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base, Token
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_token_to_db(access_token:str, db:Session):
    token = Token(access_token=access_token)
    db.add(token)
    db.commit()
    db.refresh(token)

    print(f"Token saved to database: {token.id}")

    return token

def get_latest_token(db:Session):
    token = db.query(Token).filter(Token.expires_at > datetime.utcnow()).order_by(Token.created_at.desc()).first()