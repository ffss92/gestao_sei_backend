from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .utils.database import Base
from .v1 import api
from .core import settings

# Metadados do banco de dados
metadata = Base.metadata

# Instância / Metadados do Serviço
app = FastAPI(
  title=settings.SERVICE_NAME,
  version=settings.SERVICE_VERSION,
)

# Configuração de CORS
app.add_middleware(
  CORSMiddleware, 
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Rotas
app.include_router(api.router, prefix="/api/v1")