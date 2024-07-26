import datetime
import asyncio
from aiologger import Logger

async def bot_logger():
    logger = Logger.with_default_handlers(name="bot-logger")

    logger.debug("debug", exc_info=1)
    logger.info("info", exc_info=1)
    logger.warning("warning", exc_info=1)
    logger.error("error", exc_info=1)
    logger.critical("critical", exc_info=1)
    
    await logger.shutdown()



