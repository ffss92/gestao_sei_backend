from redis import Redis
from datetime import timedelta
from pydantic import BaseModel
from typing import Optional, Type, TypeVar, Generic
from api.core import settings


SchemaType = TypeVar("SchemaType", bound=BaseModel)

client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

class Cache(Generic[SchemaType]):
  """Classe para gerenciar o cache"""
  def __init__(
      self, 
      group: str,
      schema: Type[SchemaType],
      client: Redis = client, 
      expires: timedelta = timedelta(days=1)
    ) -> None:
    self.client = client
    self.group = group
    self.expires = expires
    self.schema = schema

  def _update_key(self, key: str):
    """Adequa a `key` para o grupo do cache"""
    return f"{self.group}:{key}"

  def set(self, key: str, obj: SchemaType) -> bool:
    """Adiciona o objeto ao cache"""
    return self.client.setex(self._update_key(key), self.expires, obj.json())

  def get(self, key: str) -> Optional[SchemaType]:
    """Retorna o objeto do cache"""
    value = self.client.get(self._update_key(key))
    if value:
      return self.schema.parse_raw(value)
    return None

  def delete(self, key: str) -> bool:
    """Deletea o objeto do cache"""
    return self.client.delete(self._update_key(key))

  def get_expiration(self, key: str) -> Optional[timedelta]:
    """Retorna o tempo de vida o objeto no cache"""
    expiration_time = self.client.ttl(self._update_key(key))
    if expiration_time <= 0:
      return None
    return timedelta(seconds=expiration_time)
