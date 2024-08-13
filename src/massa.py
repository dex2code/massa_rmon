from __future__ import annotations
from loguru import logger

import asyncio
import aiohttp
from time import monotonic
from typing import (
   AnyStr,
   Union,
   List,
   NoReturn
)
from pydantic import (
   BaseModel,
   HttpUrl
)

from src.config import app_config
from src.telegram import app_courier


class MassaNode(BaseModel):
   name: AnyStr
   url: HttpUrl
   status: Union[bool, None] = None
   err: AnyStr = ""

   @logger.catch
   async def get_status(self) -> bool:
      try:
         node_status = False

         async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=app_config.app_cycle_duration_seconds)
         ) as http_session:

            for _ in range(app_config.app_probes_per_cycle):
               async with http_session.post(url=self.url.__str__(),
                                            headers=app_config.http_request_header,
                                            json=app_config.http_request_payload) as node_response:
                  if node_response.ok:
                     node_answer = await node_response.json()

                     if isinstance(node_answer, dict) and app_config.massa_find_key in node_answer:
                        node_status = True
                     else:
                        raise Exception(f"Node responded with an invalid data or the key '{app_config.massa_find_key}' was not found in node answer")

                  else:
                     raise Exception(f"Invalid HTTP code received: {node_response.status}")

         await asyncio.sleep(0.250)

      except BaseException as E:
         logger.error(E.__repr__())
         node_status = False
         self.err = E.__repr__()
      
      else:
         self.err = ""

      return node_status

   @logger.catch
   def notify(self) -> None:
      text_status = "❓ Unknown"
      if self.status: text_status = "🟢 Online"
      else: text_status = "🔴 Offline"
      text_message = app_config.telegram_message.format(
         node_name=self.name,
         node_status=text_status,
         node_error=self.err
      )
      logger.warning(text_message)
      app_courier.append_message(text_message=text_message)
      return None
   
   @logger.catch
   async def probe(self) -> None:
      new_node_status = await self.get_status()
      if self.status != new_node_status:
         self.status = new_node_status
         self.notify()
      return None


app_nodes: List[MassaNode] = [
   MassaNode(name=node, url=app_config.nodes[node]) for node in app_config.nodes
]


@logger.catch
async def monitor_loop() -> NoReturn:
   logger.info("Entering main loop...")
   while True:
      probes_started_at = monotonic()

      probe_tasks = [
         asyncio.create_task(node.probe()) for node in app_nodes
      ]
      await asyncio.wait(probe_tasks)

      probes_duration = monotonic() - probes_started_at

      if probes_duration >= app_config.app_cycle_duration_seconds:
         cycle_pause = 0
      else:
         cycle_pause = app_config.app_cycle_duration_seconds - probes_duration

      logger.info(f"Cycle started at: {probes_started_at}, duration: {probes_duration}, go sleep for {cycle_pause} seconds...")
      await asyncio.sleep(delay=cycle_pause)


if __name__ == "__main__":
   pass
