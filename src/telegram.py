from __future__ import annotations
from loguru import logger

from os import getenv as os_getenv

import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import NoReturn
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.utils.formatting import as_list
from aiogram.enums import ParseMode
from collections import deque

from src.config import app_config


if not load_dotenv():
   raise Exception(f"Cannot load .env file")

bot_session = AiohttpSession()
telegram_bot = Bot(
   token=os_getenv("RMON_TELEGRAM_TOKEN"),
   session=bot_session
)


class AppCourier(BaseModel):
   chat_id: int = int(os_getenv("RMON_TELEGRAM_CHAT"))
   queue: deque = deque()

   @logger.catch
   def append_message(self, text_message: str) -> None:
      try:
         assert isinstance(text_message, str)
         final_message = as_list(
            app_config.telegram_nickname.format(host_name=app_config.app_hostname),
            text_message
         ).as_html()
         self.queue.append(final_message)
      except BaseException as E:
         logger.error(f"Cannot queue message: {E.__repr__()}")
      else:
         logger.info(f"Added new message to courier queue ({text_message})")


app_courier = AppCourier()


@logger.catch
async def courier_loop() -> NoReturn:
   while True:
      await asyncio.sleep(delay=app_config.telegram_sending_delay_seconds)
      if len(app_courier.queue):
         try:
            await telegram_bot.send_message(
               chat_id=app_courier.chat_id,
               text=app_courier.queue.popleft(),
               parse_mode=ParseMode.HTML,
               request_timeout=app_config.telegram_sending_timeout_seconds
            )
         except BaseException as E:
            logger.error(f"Cannot send message: {E}")
         else:
            logger.info(f"Message sent successfully")


if __name__ == "__main__":
   pass
