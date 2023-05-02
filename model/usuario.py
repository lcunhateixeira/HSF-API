from model.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id: int = Column("pk_usuario", Integer, primary_key=True)
    nome: str = Column(String)
    celular: str = Column(String, unique=True)
    
    def __init__(self, nome: str, celular: str):
        self.nome = nome
        self.celular = celular
        
    registros = relationship("Registro", back_populates="usuario")