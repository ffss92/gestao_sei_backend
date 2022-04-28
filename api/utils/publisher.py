import json

from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from api.core.settings import settings 
from api import schemas
import pika

class EventPublisher:

  exchange_declared = False

  def __init__(
    self, 
    host: str = settings.RABBITMQ_HOST, 
    port: str = settings.RABBITMQ_PORT,
    exchange_name: str = "events",
    enabled: bool = settings.RABBITMQ_ENABLED,
  ):
    self.host = host
    self.port = port
    self.exchange_name = exchange_name
    self.enabled = enabled

  def _create_connection(self) -> pika.BlockingConnection:
    connection = pika.BlockingConnection(
      pika.ConnectionParameters(host=self.host, port=self.port)
    )
    return connection

  def _create_channel(self, connection: BlockingConnection) -> BlockingChannel:
    channel = connection.channel()
    if not self.exchange_declared:
      channel.exchange_declare(exchange=self.exchange_name, exchange_type="topic")
      self.exchange_declared = True
    return channel

  def destination_event(self, *, type_: str, db_obj, user):
    if not self.enabled:
      return
    try:
      connection = self._create_connection()
      channel = self._create_channel(connection)
      channel.basic_publish(
        exchange=self.exchange_name,
        routing_key=f"destination.{type_}",
        body=json.dumps({
            "type": type_,
            "resource": "destination",
            "user_id": user.id,
            "payload": schemas.Destination.from_orm(db_obj).dict()
          }, 
          default=str
        )
      )
      connection.close()
    except Exception as e:
      print(e)

  def process_event(self, *, type_: str, db_obj, user):
    if not self.enabled:
      return
    try:
      connection = self._create_connection()
      channel = self._create_channel(connection)
      channel.basic_publish(
        exchange=self.exchange_name,
        routing_key=f"process.{type_}",
        body=json.dumps({
            "type": type_,
            "resource": "process",
            "user_id": user.id,
            "payload": schemas.Process.from_orm(db_obj).dict()
          }, 
          default=str
        )
      )
      connection.close()
    except Exception as e:
      print(e)



event_publisher = EventPublisher()