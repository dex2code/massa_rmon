from __future__ import annotations
from loguru import logger

import asyncio
from typing import NoReturn
from sys import version_info

from src.massa import monitor_loop
from src.telegram import app_courier, courier_loop, bot_session


@logger.catch
async def main() -> NoReturn:
   app_courier.append_message(text_message=f"🏃 Started!")
   try:
      async with asyncio.TaskGroup() as t_group:
         def1_result = t_group.create_task(monitor_loop())
         def2_result = t_group.create_task(courier_loop())
   except BaseException as E:
      logger.error(f"Coros failed: {def1_result=}, {def2_result=}")
      await bot_session.close()
      raise


if __name__ == "__main__":
   logger.add(sink="logs/main.log", level="INFO",
              format="{time} | {level}\t| {file.path}:{line} '{message}'",
              backtrace=True, diagnose=True, enqueue=True,
              rotation="1 day", retention="1 month", compression="zip")
   logger.info(f"*** MASSA remote monitor starting...")
   assert (version_info.major == 3 and version_info.minor >= 11), "You need Python version 3.11+ to run"

   try:
      asyncio.run(main=main())
   except BaseException as E:
      logger.error(E.__repr__())
   finally:
      logger.critical(f"*** MASSA remote monitor stopped")
