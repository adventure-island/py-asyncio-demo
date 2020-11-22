# coding=utf-8
"""
Synchronization Primitives

Although asyncio applications usually run as a single-threaded process, they are
still built as concurrent applications. Each coroutine or task may execute in 
an unpredictable order, based on delays and interrupts from I/O and other 
external events. To support safe concurrency, asyncio includes implementations 
of some of the same low-level primitives found in the threading and 
 `multiprocessing` modules.
"""

import asyncio
import random
import logging

FORMAT = "[%(asctime)s][%(funcName)10s()] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


async def mycoro(task_id: int) -> str:
    
    seconds = random.randint(1, 10)
    logger.debug(f'Starting task {task_id}, will sleep for {seconds} seconds')
    
    try:
        await asyncio.sleep(seconds)
    except asyncio.CancelledError:
        logger.debug(f'Task {task_id} was canceled')
        raise
    
    logger.debug(f'Finishing task {task_id}') # Runs later
    return str(task_id)


def unlock(lock):
    logger.debug('callback releasing lock')
    lock.release()


async def coro1(lock):
    """Demonstrate using asynchronous context manager to interact with the lock.
    """
    
    logger.debug('coro1 waiting for the lock')
    async with lock:
        logger.debug('coro1 acquired lock')
        seconds = random.randint(1, 10)
        logger.debug(f'sleep for {seconds} seconds')
        await asyncio.sleep(seconds)
        
    logger.debug('coro1 released lock')


async def coro2(lock):
    """A lock’s `acquire()` method can be invoked directly, using `await`, and 
    calling the `release()` method when done
    """
    
    logger.debug('coro2 waiting for the lock')
    
    await lock.acquire()
    try:
        logger.debug('coro2 acquired lock')
        seconds = random.randint(1, 10)
        logger.debug(f'sleep for {seconds} seconds')
        await asyncio.sleep(seconds)
        
    finally:
        logger.debug('coro2 released lock')
        lock.release()


async def main(loop):
    # Create and acquire a shared lock.
    lock = asyncio.Lock()
    logger.debug('acquiring the lock before starting coroutines')
    await lock.acquire()
    logger.debug('lock acquired: {}'.format(lock.locked()))

    # Schedule a callback to unlock the lock.
#     loop.call_later(0.1, functools.partial(unlock, lock))
    loop.call_later(0.1, unlock, lock)

    # Run the coroutines that want to use the lock.
    logger.debug('waiting for coroutines')
    await asyncio.wait([coro1(lock), coro2(lock)]),


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()    