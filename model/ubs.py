from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from model.base import Base
from model.registro import Registro

class UBS(Base):
    """
    A classe UBS representa Unidade Básica de Saúde
    """
    __tablename__ = "ubs"
    
    id = Column("pk_ubs", Integer, primary_key=True)
    nome_fantasia = Column(String(100))
    endereco = Column(String(200))
    cidade = Column(String(100))
    latitude = Column(String(20))
    longitude = Column(String(20))
    telefone = Column(String(20))
    cnes = Column(String(20), unique=True)
    fila = Column(Integer)
    registros = relationship("Registro")

        
    def __init__(self, nome_fantasia:str, cidade: str, endereco:str, latitude:str, longitude:str, telefone: str, cnes:str, fila:int):
        """
        Cria uma Unidade Básica de Saúde

        Arguments:
            nome_fantasia: Nome fantasia da Unidade de Saúde
            endereco: Endereço da Unidade de Saúde
            latitude: Latitude da Unidade de Saúde
            longitude: Longitude da Unidade de Saúde
            cnes: CNES da Unidade de Saúde
            fila: Fila da Unidade de Saúde
        """
        self.nome_fantasia = nome_fantasia
        self.endereco = endereco
        self.cidade = cidade
        self.latitude = latitude
        self.longitude = longitude
        self.telefone = telefone
        self.cnes = cnes
        self.fila = fila


    def aumenta_fila(self):
        """Função para adicionar entrada a fila da Unidade de Saúde
        """
        self.fila = 1 if self.fila == 0 or self.fila == None else self.fila + 1 

    def diminui_fila(self):
        """Função para diminuir a fila da Unidade de Saúde
        """
        self.fila = 0 if self.fila == 0 or self.fila == None else self.fila - 1
    
    def adiciona_registro(self, registro: Registro):
        """Função para adicionar um registro de entrada ou saída da fila da Unidade de Saúde
        """
        self.registros.append(registro)
    
