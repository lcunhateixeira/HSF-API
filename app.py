import calendar
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from sqlalchemy import and_, or_

from model import Session, UBS, Registro, Usuario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API - Hospital Sem Fila", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
ubs_tag = Tag(name="UBS", description="Adição e listagem de Unidades Básicas de Saúde")
registro_tag = Tag(name="Registro", description="Registro de entrada e saída de usuários nas Unidades Básicas de Saúdes")
usuario_tag = Tag(name="Usuário", description="Adição e listagem de Usuários")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/usuario', tags=[usuario_tag],
        responses={"200": UsuarioSchema, "409": ErrorSchema, "400": ErrorSchema})
def adiciona_usuario(form: UsuarioSchema):
    
    usuario = Usuario(
        nome = form.nome,
        celular = form.celular,
    )
    
    try:
        session = Session()
        session.add(usuario)
        session.commit()
        return apresenta_usuario(usuario), 200
    
    except IntegrityError as e:
        logger.error(f"Erro ao adicionar usuário: {e}")
        return {"message": "Usuário já existe"}, 409

@app.get('/usuarios', tags=[usuario_tag],
        responses={"200": ListagemUsuarioSchema, "400": ErrorSchema})
def get_usuarios():
    """Retorna uma lista de usuários.
    """
    try:
        session = Session()
        usuarios = session.query(Usuario).all()
        if usuarios:
            return apresenta_usuarios(usuarios), 200
        else:
            return {"usuarios": []}, 200
        
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {e}")
        return {"message": "Erro ao listar usuários"}, 400


@app.post('/ubs', tags=[ubs_tag],
        responses={"200": UBSViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_ubs(form: UBSSchema):
    """Adiciona uma nova UBS à base de dados

    Retorna uma representação da UBS.
    """
    ubs = UBS(
        nome_fantasia = form.nome_fantasia,
        cidade = form.cidade,
        endereco = form.endereco,
        latitude = form.latitude,
        longitude = form.longitude,
        telefone = form.telefone,
        cnes = form.cnes,
        fila = form.fila
    )
    logger.debug(f"Adicionando Unidade Básica de Saúde de nome: '{ubs.nome_fantasia}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando UBS
        session.add(ubs)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado UBS de nome: '{ubs.nome_fantasia}'")
        usb_schema = UBSSchema(
            nome_fantasia = ubs.nome_fantasia,
            endereco = ubs.endereco,
            latitude = ubs.latitude,
            longitude = ubs.longitude,
            telefone = ubs.telefone,
            cnes = ubs.cnes,
            fila = ubs.fila,
        )
        
        return apresenta_ubs(usb_schema), 200

    except IntegrityError as e:
        # A duplicidade do cnes é a provável razão do IntegrityError
        error_msg = "UBS de mesmo cnes já salva na base :/"
        logger.warning(f"Erro ao adicionar UBS '{ubs.nome_fantasia}', {error_msg}")
        return {"mesage": error_msg}, 409
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível salvar a nova UBS, exception '{e}' :/"
        logger.warning(f"Erro ao adicionar Unidade Básica de Saúde '{ubs.nome_fantasia}', {error_msg}")
        return {"mesage": error_msg}, 400


# @app.get('/ubs', tags=[ubs_tag],
#         responses={"200": UBSSchema, "404": ErrorSchema, "400": ErrorSchema})
# def get_ubs(query: UBSSchema):
#     """ Retorna uma representação da UBS com o cnes passado como parâmetro.
#     """
#     cnes = query.cnes
#     logger.debug(f"Buscando UBS com cnes: '{cnes}'")
#     try:
#         # criando conexão com a base
#         session = Session()
#         # buscando UBS
#         ubs = session.query(UBS).filter(UBS.cnes == cnes).first()        
#         if ubs:
#             return apresenta_ubs(ubs), 200
#         else:
#             error_msg = f"UBS com cnes '{cnes}' não encontrada :/"
#             logger.warning(f"Erro ao buscar UBS com cnes: '{cnes}', {error_msg}")
#             return {"mesage": error_msg}, 404
#     except Exception as e:
#         # caso um erro fora do previsto
#         error_msg = f"Não foi possível buscar a UBS com cnes '{cnes}', exception '{e}' :/"
#         logger.warning(f"Erro ao buscar UBS com cnes: '{cnes}', {error_msg}")
#         return {"mesage": error_msg}, 400


@app.get('/ubses', tags=[ubs_tag],
            responses={"200": ListagemUBSSchema, "400": ErrorSchema})
def get_ubses():
    """ Retorna uma lista com todas as Unidades Básicas de Saúde cadastradas na base de dados
        Retorna uma representação da UBS.
    """
    logger.debug(f"Listando todas as UBSes")
    try:
        # criando conexão com a base
        session = Session()
        # buscando todos as Uniades Básicas de Saúde
        logger.debug(f"Buscando todas as UBSes")
        ubses = session.query(UBS).order_by(UBS.fila.asc()).all()
        logger.debug(f"Listando todas as UBSes")
        if not ubses:
            # se não há unidades básicas de saude cadastradas
            return {"ubses": []}, 200
        else:
            logger.debug(f"%d UBSs econtradas" % len(ubses))
            # retorna a representação de produto
            return apresenta_ubses(ubses), 200
        
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível listar as UBSes :/"
        logger.warning(f"Erro ao listar UBSes, {error_msg}")
        return {"mesage": error_msg}, 400

@app.post('/registro', tags=[registro_tag], 
          responses={"200": RegistroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def registra_entrada_saida(form: RegistroSchema):
    """Inclui um registro de entrada ou saída de um usuário na UBS

    Args:
        form (RegistroViewSchema): _description_
    """
    logger.debug(f"Registrando entrada ou saída de usuário na UBS")
    try:        
        # criando conexão com a base
        logger.debug("Criando conexão com a base")
        novo_registro = None
        session = Session()
        #verificar se usuário já está na fila
        registro = session.query(Registro).filter(
                            and_(
                                    Registro.usuario_id == form.usuario_id,
                                    Registro.data_saida == None                               
                                )
                            ).first()
        #Se já está na fila, atualiza data de saída ou data de entrada
        if registro and registro.ubs_id == form.ubs_id:            
            #registra saída e retira da fila da ubs
            registro.data_saida = datetime.now()
            registro.ubs.diminui_fila()
            novo_registro = registro
            session.add(registro) 
        else:
            #Se o usuário tinha registro de entrada em outra ubs, dimimui a fila da ubs e atualiza data de saída do registro 
            if registro:
                registro.ubs.diminui_fila()
                registro.data_saida = datetime.now()
                session.add(registro)
            #Cria novo registro de entrada
            novo_registro  = Registro(
                data_entrada = datetime.now(),
                data_saida = None,
                ubs_id = form.ubs_id,
                usuario_id = form.usuario_id,
            )
            #adiciona novo registro
            session.add(novo_registro)
            #Aumenta a fila da ubs 
            ubs  = session.get(UBS, form.ubs_id)
            ubs.aumenta_fila()
            session.add(ubs)
            
        # efetivando o comando de adição do novo registro na tabela
        logger.debug("Efetivando o comando de adição do novo registro na tabela")
        session.commit()
        logger.debug("apresentando registro de entrada ou saída")
        return apresenta_registro(novo_registro), 200
        
    except IntegrityError as e:
        error_msg = "Erro de integridade ao adicionar registro de entrada ou saída :/"
        logger.warning(f"Erro ao adicionar registro ubs_id: '{form.ubs_id}', user_id: '{form.usuario_id}', {error_msg}")
        return {"mesage": error_msg}, 409
    except Exception as e:
        error_msg = f"Não foi possível salvar o novo registro de entrada ou saída '{e}':/"
        logger.warning(f"Erro ao adicionar registro ubs_id: '{form.ubs_id}', user_id: '{form.usuario_id}', {error_msg}")
        return {"mesage": error_msg}, 400
