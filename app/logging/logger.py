"""
Пример асинхронного logger'a.
#TODO Переписать logger под свой код!

"""
import logging
from logging.handlers import QueueHandler
from logging.handlers import QueueListener
from logging import StreamHandler
from random import random
from queue import Queue
import asyncio


# helper coroutine to setup and manage the logger
async def init_logger():
    # get the root logger
    log = logging.getLogger()
    # create the shared queue
    que = Queue()
    # add a handler that uses the shared queue
    log.addHandler(QueueHandler(que))
    # log all messages, debug and up
    log.setLevel(logging.DEBUG)
    # create a listener for messages on the queue
    listener = QueueListener(que, StreamHandler())
    try:
        # start the listener
        listener.start()
        # report the logger is ready
        logging.debug(f'Logger has started')
        # wait forever
        while True:
            await asyncio.sleep(60)
    finally:
        # report the logger is done
        logging.debug(f'Logger is shutting down')
        # ensure the listener is closed
        listener.stop()


# task that does work and logs
async def task(value):
    # log a message
    logging.info(f'Task {value} is starting')
    # simulate doing work
    await asyncio.sleep(random() * 5)
    # log a message
    logging.info(f'Task {value} is done')


# main coroutine
async def main():
    # initialize the logger
    logger = asyncio.create_task(init_logger())
    # allow the logger to start
    await asyncio.sleep(0)
    # log a message
    logging.info(f'Main is starting')
    # issue many tasks
    async with asyncio.TaskGroup() as group:
        for i in range(10):
            _ = group.create_task(task(i))
    # log a message
    logging.info(f'Main is done')


# start the event loop
asyncio.run(main())
