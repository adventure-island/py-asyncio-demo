'''
Created on Oct 31, 2020

CPU-BOUND: Computation-intensive tasks, can get worse when using threading
        because added overhead cost involved when creating/destroying threads
IO-BOUND: IO-blocking tasks, lots of waiting around INPUT and OUTPUT ops

Threading with GIL: 
 - NOT running code at the same time
 - An 'illusion' of parallelism
 
@author: JJ
'''

import logging
import time
from math import sqrt
import asyncio

FORMAT = "[%(threadName)s][%(filename)s:%(lineno)s - %(funcName)10s()] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

logger = logging.getLogger(__name__)





def fib():
    
    a = 2
    b = 1
    yield a
    while True:
#         logger.debug(f'yielding {b}')
        yield b
        a, b = b, a + b

        
async def is_prime(x):
#     logger.debug('is_prime')
    if x < 2:
        return False

    for i in range(2, int(sqrt(x)) + 1):
        if x % i == 0:
            return False
        # yield to avoid blocking on large numbers
#         logger.debug(f'yielding None')
        await asyncio.sleep(0)
    
    return True


async def search(iterable, predicate):
    
    logger.debug('search')
    for item in iterable:
#         logger.debug(f'search - checking {item}')
        if await predicate(item):
            logger.debug('predicate returned True')
            return item

        await asyncio.sleep(0)

    raise ValueError("Not found")


async def print_matches(iterable, async_predicate):
    for item in iterable:
        # ` yield from` allows the predicate to make progress
        # and yield control back to caller
        matches = await async_predicate(item)
        if matches:
            logger.debug(f"Found: {item}")


async def repetitive_message(msg, interval_secs):
    # Periodically print a message
    while True:
        logger.debug(msg)
        await asyncio.sleep(interval_secs)    
        
        
async def x_digit_prime(x):
    return (await is_prime(x)) and len(str(x)) == 12


async def monitor_future(fut, interval):
    logger.debug('monitor_future...')
    while not fut.done():
        logger.debug('Waiting...')
        await asyncio.sleep(interval)
    logger.debug('Task done!')
    

if __name__ == '__main__':    
    loop = asyncio.get_event_loop()
    
    search_task = asyncio.ensure_future(
        search(fib(), x_digit_prime), loop=loop
    )
     
    monitor_task = asyncio.ensure_future(
        monitor_future(search_task, 1.0), loop=loop
    )
    
#     repetitive_task = asyncio.ensure_future(
#         repetitive_message('hello repetitive_task !', 2.5), loop=loop)

    all_future = asyncio.gather(search_task, monitor_task)
    
    loop.run_until_complete(all_future)
    logger.debug(f'Result: {search_task.result()}')
    loop.close()
