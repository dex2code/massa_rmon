from __future__ import annotations
from socket import gethostname
from typing import (
   AnyStr,
   Dict
)
from pydantic import (
   BaseModel,
   PositiveInt,
   PositiveFloat,
   HttpUrl
)
from app_config import (
   app,
   telegram,
   nodes,
   http,
   massa
)


class AppConfig(BaseModel):
   app_hostname: AnyStr
   app_cycle_duration_seconds: PositiveInt
   app_probes_per_cycle: PositiveInt
   telegram_nickname: AnyStr
   telegram_message: AnyStr
   telegram_sending_delay_seconds: PositiveFloat
   telegram_sending_timeout_seconds: PositiveInt
   nodes: Dict[AnyStr, HttpUrl]
   http_request_header: Dict
   http_request_payload: Dict
   massa_find_key: AnyStr


app_config: AppConfig = AppConfig(
   app_hostname=gethostname(),
   app_cycle_duration_seconds=app['cycle_duration_seconds'],
   app_probes_per_cycle=app['probes_per_cycle'],
   telegram_nickname=telegram['nickname'],
   telegram_message=telegram['message'],
   telegram_sending_delay_seconds=telegram['sending_delay_seconds'],
   telegram_sending_timeout_seconds=telegram['sending_timeout_seconds'],
   nodes=nodes,
   http_request_header=http['request_header'],
   http_request_payload=http['request_payload'],
   massa_find_key=massa['find_key']
)


if __name__ == "__main__":
   pass
