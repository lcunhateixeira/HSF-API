from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.registro import Registro

class RegistroSchema(BaseModel):
    """ Define como um novo registro de entrada e saída deve ser representado
    """
    data_entrada: Optional[datetime] = None
    data_saida: Optional[datetime] = None
    ubs_id: int = None
    usuario_id: int = None
    
class RegistroViewSchema(BaseModel):
    """ Define a apresentação de um registro de entrada e saída 
    """
    usuario_id: int = 1
    usuario_nome: str = "João da Silva"
    usb_nome_fantasia: str = "Casa de Saúde São José"
    data_entrada: Optional[datetime] = "2021-08-01 12:00:00"
    data_saida: Optional[datetime] = "2021-08-01 12:00:00"
    
def apresenta_registro(registro:Registro):
    """ Função para apresentar um registro de entrada e saída
    """
    return {
     'usuario_id': registro.usuario.id,
     'usuario_nome': registro.usuario.nome,
     'ubs_nome_fantasia': registro.ubs.nome_fantasia,
     'data_entrada': registro.data_entrada,
     'data_saida': registro.data_saida,
    }
    
def apresenta_lista_registros(registros:List[Registro]):
    """ Função para apresentar uma lista de registros de entrada e saída
    """
    return [apresenta_registro(registro) for registro in registros]