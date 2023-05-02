from sqlalchemy import Column, Integer, extract, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from typing import Union

from model.base import Base

class Registro(Base):
    __tablename__ = "registro"
    
    id = Column("pk_registro", Integer, primary_key=True)    
    data_entrada = Column(DateTime)
    data_saida = Column(DateTime)   
    ubs_id = Column(Integer, ForeignKey("ubs.pk_ubs"), nullable=False)
    ubs = relationship("UBS", back_populates="registros")
    usuario_id = Column(Integer, ForeignKey("usuario.pk_usuario"), nullable=False)
    usuario = relationship("Usuario", back_populates="registros")    
   
    def __init__(self, usuario_id: int, ubs_id: int, data_entrada:Union[DateTime, None] = None, data_saida:Union[DateTime, None] = None):
        """
        Cria um histórico de registro de entrada ou saída da Unidade de Saída

        Arguments:
            data_registro: data de entrada e saída da fila à base
        """    
        self.ubs_id = ubs_id
        self.usuario_id = usuario_id
        if data_entrada:
            self.data_entrada = data_entrada
            
        if data_saida:
            self.data_saida = data_saida
   