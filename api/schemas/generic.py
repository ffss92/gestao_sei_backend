from typing import Optional
from pydantic import BaseModel


class Detail(BaseModel):
  detail: str

class Msg(BaseModel):
  msg: str

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenPayload(BaseModel):
  sub: Optional[int] = None

class Pagination(BaseModel):
  current_page: int
  total_pages: int
  count: int
  limit: int