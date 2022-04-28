import os
from typing import List, Union
from pydantic import BaseSettings
from datetime import datetime, timedelta
from dotenv import load_dotenv


# Carrega as variáveis do arquivo .env
load_dotenv()

class Settings(BaseSettings):
  """
  Configurações Básicas do Serviço \n
  TODO: Validar configurações usando [BaseSettings](https://pydantic-docs.helpmanual.io/usage/settings/).
  """

  # SERVICE
  SERVICE_NAME: str = os.environ.get("SERVICE_NAME", "Api")
  SERVICE_VERSION: str = os.environ.get("SERVICE_VERSION", "0.1.0")
  ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")

  # DATABASE
  DB_USER: str = os.environ.get("DB_USER")
  DB_PASSWORD: str = os.environ.get("DB_PASSWORD")
  DB_DB: str = os.environ.get("DB_DB")
  DB_HOST: str = os.environ.get("DB_HOST")
  DB_PORT: str = os.environ.get("DB_PORT")

  # REDIS
  REDIS_HOST: str = os.environ.get("REDIS_HOST", "localhost")
  REDIS_PORT: int = os.environ.get("REDIS_PORT", 6379)
  REDIS_PASSWORD: str = os.environ.get("REDIS_PASSWORD")

  # RABBITMQ
  # Variáveis do RabbitMQ
  RABBITMQ_ENABLED: bool = bool(os.environ.get("RABBITMQ_ENABLED", False))
  RABBITMQ_HOST: str = os.environ.get("RABBITMQ_HOST")
  RABBITMQ_PORT: str = os.environ.get("RABBITMQ_PORT")
  RABBITMQ_USER: str = os.environ.get("RABBITMQ_USER")
  RABBITMQ_PASSWORD: str = os.environ.get("RABBITMQ_PASSWORD")

  #CORS ORIGINS 
  CORS_ORIGINS: Union[List[str], str, None] = ["*"]

  # JWT
  SECRET_KEY: str = os.environ.get("SECRET_KEY")
  ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")
  TOKEN_EXPIRATION: timedelta = timedelta(minutes=(60 * 2)) # Duas horas

  # PW RESET EXPIRES
  PW_RESET_TOKEN_EXPIRES: datetime = datetime.utcnow() + timedelta(hours=4)

  # ADMIN
  ADMIN_EMAIL: str = os.environ.get("ADMIN_EMAIL")
  ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD") 

settings = Settings()