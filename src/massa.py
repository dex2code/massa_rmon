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
from src.http_client import get_node_status, check_node_response
from src.telegram import node_notify


class MassaNode(BaseModel):
   name: AnyStr
   url: HttpUrl
   status: Union[bool, None] = None

   @logger.catch
   async def probe(self) -> None:
      final_node_status = False
      try:
         session_timeout = aiohttp.ClientTimeout(total=app_config.app_cycle_duration_seconds)
         async with aiohttp.ClientSession(timeout=session_timeout) as http_session:
            for _ in range(app_config.app_probes_per_cycle):
               node_status = await get_node_status(session=http_session, node_url=self.url.__str__())
               if check_node_response(node_response=node_status):
                  final_node_status = True
               else:
                  final_node_status = False
                  break
         await asyncio.sleep(0)
      except BaseException as E:
         logger.error(f"{E}")
         final_node_status = False
      finally:
         if self.status != final_node_status:
            self.status = final_node_status
            node_notify(node_name=self.name, node_status=self.status)


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
