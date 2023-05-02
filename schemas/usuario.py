from pydantic import BaseModel
from typing import Optional, List

from model.usuario import Usuario
from schemas import RegistroViewSchema, apresenta_lista_registros


class UsuarioSchema(BaseModel):
    id: int = 1
    nome: str = "João da Silva"
    celular: str = "11987654321"
    registros: List[RegistroViewSchema] = []

class ListagemUsuarioSchema(BaseModel):
    usuarios: List[UsuarioSchema]
    
def apresenta_usuario(usuario:Usuario):
    """ Função para apresentar um usuário
    """
    return {
        'id': usuario.id,
        'nome': usuario.nome,
        'celular': usuario.celular,
        'registros': apresenta_lista_registros(usuario.registros) if usuario.registros else [],
    }
    
def apresenta_usuarios(usuarios:List[Usuario]):
    """ Função para apresentar uma lista de usuários
    """
    result = []
    for usuario in usuarios:
        result.append(apresenta_usuario(usuario))
    return {"usuarios": result}