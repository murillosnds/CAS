from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api.routes import router

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Cálculo de Hidratação",
    description="API para calcular a quantidade ideal de água diária",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(router, prefix="/api/v1", tags=["hydration"])

@app.get("/")
async def root():
    return {
        "message": "API de Cálculo de Hidratação",
        "docs": "/docs",
        "version": "1.0.0"
    }