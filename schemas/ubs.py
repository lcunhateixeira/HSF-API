import calendar
from pydantic import BaseModel
from datetime import datetime

from typing import Optional, List
from model.ubs import UBS
from schemas.registro import RegistroSchema


class UBSSchema(BaseModel):
    """ Define como uma nova UBS deve ser representada
    """
    id: int = 1
    nome_fantasia: str = "Centro de Saúde Tapera"
    endereco: str = "Rua Tapera, 123"
    cidade: str = "São Paulo"
    latitude: str = "-23.123456"
    longitude: str = "-45.123456"
    telefone: str = "11987654321"
    cnes: str = "1234567"
    fila: int = 0
    registros: List[RegistroSchema] = []
        
class UBSViewSchema(BaseModel):
    """ Define como uma nova UBS deve ser representada
    """
    id: int = 1
    nome_fantasia: str = "Centro de Saúde Tapera"
    endereco: str = "Rua Tapera, 123"
    cidade: str = "São Paulo"
    latitude: str = "-23.123456"
    longitude: str = "-45.123456"
    telefone: str = "11987654321"
    cnes: str = "1234567"
    fila: int = 0
    movimentacao_mes: str = "10"
    media_movimentacao_diaria: str = "0.33"
    
class BuscaUBSSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca de uma Unidade Básica de Saúde 
        Que será realizada pelo cnes (Código Nacional de Estabelecimento de Saúde)  ou pelo nome fantasia
    """
    nome_fantasia: Optional[str] = "Centro de Saúde Tapera"
    cnes: Optional[str] = "1234567"
    

def apresenta_ubs(ubs:UBS) -> UBSViewSchema:
    """ Retorna uma representação da UBS seguindo o schema definido em
        UBSViewSchema.
    """
    ano_atual = datetime.now().year
    mes_atual = datetime.now().month
    dias_no_mes = calendar.monthrange(ano_atual, mes_atual)[1]
    #Calculando a quantidade de movimentações no mês
    movimentacoes_mes = 0
    for registro in ubs.registros:
        if registro.data_saida and registro.data_saida.month == mes_atual:
            movimentacoes_mes += 1

    #calculando média de movimentação diária
    media_movimentacao_diaria = movimentacoes_mes / dias_no_mes
    
    return {
        'id': ubs.id,
        'nome_fantasia': ubs.nome_fantasia,
        'endereco': ubs.endereco,
        'cidade' : ubs.cidade,
        'latitude': ubs.latitude,
        'longitude': ubs.longitude,
        'telefone': ubs.telefone,  
        'cnes': ubs.cnes,
        'fila': ubs.fila,
        'movimentacao_mes': movimentacoes_mes,
        'media_movimentacao_diaria': media_movimentacao_diaria,
    }

class ListagemUBSSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a listagem de UBS
    """
    ubses: List[UBSViewSchema]

def apresenta_ubses(ubses: List[UBS]):
    """ Função que recebe uma lista de UBS e retorna uma ListagemUBSSchema
    """
    result = []
    for ubs in ubses:
        result.append(apresenta_ubs(ubs))
    return {"ubses": result}

class DeleteUBSSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a exclusão de uma Unidade Básica de Saúde 
        Que será realizada pelo cnes (Código Nacional de Estabelecimento de Saúde)
    """
    message: str = "Unidade Básica de Saúde excluída com sucesso"
    nome_fantasia: str = "Centro de Saúde Tapera"
