import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

USUARIO = os.getenv("DB_USER", "postgres")
SENHA_RAW = os.getenv("DB_PASSWORD")

if not SENHA_RAW:
    raise RuntimeError("DB_PASSWORD não definida")

SENHA = quote_plus(SENHA_RAW)

HOST = os.getenv("DB_HOST", "localhost")
PORTA = os.getenv("DB_PORT", "5432")
BANCO = os.getenv("DB_NAME", "ingestao_agua")

DATABASE_URL = f"postgresql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
