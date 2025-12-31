from sqlalchemy import Column, Integer, Float, String
from database import Base

class IngestaoAgua(Base):
    __tablename__ = "ingestao_agua"

    id = Column(Integer, primary_key=True, index=True)
    peso = Column(Float, nullable=False)
    idade = Column(Integer, nullable=False)
    atividade = Column(String, nullable=False)
    clima = Column(String, nullable=False)
    quantidade_de_agua = Column(Float, nullable=False)
