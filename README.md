# HSP-API
Códigos API MVP 01 Pós-Graduação em Desenvolvimento Full Stack PUC-Rio.
Este pequeno projeto faz parte do primeiro MVP (Minimum Viable Product) do curso de **Pós-Graduação em Desenvolvimento Full Stack PUC-Rio** e tem como objetivo o desenvolvimento de uma API colocando em prática o conteúdo estudado nesta primeira fase do curso.

## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenpython -m venv .v.pypa.io/en/latest/).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```
Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

Para facilitar os testes faça a carga de dados das Unidades Básicas da cidade de Araranguá-SC através dos seguintes passos:
Instale o sqlite3
```
(env)$ sudo apt install sqlite
```
Após ter executado a API é criada uma base de dados dentro da pasta 'database', após ter executado a API 
execute os comandos abaixo para para carregar as Unidades Basicas de Saúde
```
(env)$ sqlite3 db.sqlite3 < carrega-UBS-Ararangua.sql
```



