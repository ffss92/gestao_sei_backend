# API - Gestão do SEI
## 1. Setup
Para iniciar o servidor, serão necessários alguns pré requisitos.
- [Python](https://www.python.org/) 3.6.8^
- [MySQL](https://www.mysql.com/)
- [Redis](https://redis.io/)
- [RabbitMQ](https://rabbitmq.com/)

### 1.1 Variáveis de ambiente
O projeto depende de várias variáveis de ambiente. Para defini-las, crie um arquivo `.env` com base nas configurações do modelo `.env.conf` 
e configure as informações.

### 1.2 Dependências
Para o ambiente de desenvolvimento, crie um ambiente virtual do Python usando o comando `python -m venv <venv>` na raiz do projeto. 
- Windows: Para ativar o ambiente virtual no Windows, digite `C:\> <venv>\Scripts\activate.bat`.
- Linux: Para ativar o ambiente virtual no Linux, digite `$ source <venv>/bin/activate`.<br/>

Para sair do ambiente virtual, digite `deactivate`. Referência para criação de ambientes virtuais no Python pode ser encontrada [aqui](https://docs.python.org/3/library/venv.html). <br/>

As dependências do projeto estão contidas no arquivo `requirements.txt`. Para instalá-las, vá até a raiz do projeto e digite `pip install -r requirements.txt`

### 1.3 Migrações no Banco de Dados
Após instaladas as dependências e configuração das variáveis de ambiente, é necessário aplicar as migrações ao banco de dados. O projeto usa o pacote [alembic](https://alembic.sqlalchemy.org/en/latest/) para gerenciar as migrações de mudanças no banco de dados.<br/>
Para executar as migrações, digite o comando `alembic upgrade head`.

### 1.4 Pré-inicilização
Para executar algum código antes de iniciar o servidor, modifique o script `pre_start.py`. Atualmente, o script cria um usuário administrador com base nas variáveis de ambientes `ADMIN_EMAIL` e `ADMIN_PASSWORD` declaradas no arquivo `.env`. 

### 1.5 Iniciando o servidor
Para inciar o servidor, digite o comando `uvicorn api.main:app` na raiz do projeto. 
Por padrão, a porta 8000 é utilizada. 
Para mais informações sobre as configuração veja a [documentação](https://www.uvicorn.org/) do uvicorn.

## 2. Documentação
O framework utilizado no projeto, [FastAPI](https://fastapi.tiangolo.com/), gera automaticamente a documentação OpenAPI do serviço com base nos schemas e rotas declaradas. 
Por padrão, a documentação pode ser acessada no link http://localhost:8000/docs. A documentação apresenta todos os endpoints da API e permite fazer requisições a cada um deles.