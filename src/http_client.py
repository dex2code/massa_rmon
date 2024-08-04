from __future__ import annotations
from loguru import logger

from typing import (
   Union,
   Dict
)

import aiohttp
import asyncio

from src.config import app_config

@logger.catch
async def get_node_status(session: aiohttp.ClientSession, node_url: str) -> Union[None, Dict]:
   node_status = None
   try:
      async with session.post(url=node_url,
                              headers=app_config.http_request_header,
                              json=app_config.http_request_payload) as node_response:
         if node_response.ok:
            node_status = await node_response.json()
      await asyncio.sleep(0)
   except BaseException as E:
      logger.error(f"Cannot probe node {node_url}: {E} ({E.__repr__()})")
      node_status = None
   finally:
      return node_status


@logger.catch
def check_node_response(node_response: dict) -> bool:
   try:
      node_chain_id = node_response['result']['chain_id']
   except BaseException as E:
      logger.error(f"{E}")
      return False
   else:
      return node_chain_id == app_config.massa_chain_id
