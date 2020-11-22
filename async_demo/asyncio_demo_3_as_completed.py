# coding=utf-8
"""Handling Background Operations as They Finish

as_completed() is a generator that manages the execution of a list of coroutines 
given to it and produces their results one at a time as they finish running. 
As with wait(), order is not guaranteed by as_completed(), but it is not 
necessary to wait for all of the background operations to complete before taking 
other action.
"""

import asyncio
import time
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


async def main(num_tasks: int, timeout=None):
    logger.debug('starting main()')
    tasks = [
        mycoro(i)
        for i in range(num_tasks)
    ]
    
    logger.debug('waiting for tasks to complete')
    
    start = time.perf_counter()
    
    results = []
    for next_to_complete in asyncio.as_completed(tasks):
        logger.debug(f'as_completed yielded a coroutine {next_to_complete}')
        logger.debug('calling await...')
        answer = await next_to_complete
        
        logger.debug('--> received answer {!r}'.format(answer))
        results.append(answer)
        
    logger.debug('results: {!r}'.format(results))
    
    finish = time.perf_counter()
    
    logger.debug(f"All tasks finished in {round(finish-start, 2)} second(s)")
    
    return results
    

event_loop = asyncio.get_event_loop()
try:
    logger.debug('calling run_until_complete')
    event_loop.run_until_complete(main(5))
    logger.debug('run_until_complete returned')
finally:
    logger.debug('closing event_loop')
    event_loop.close()
    logger.debug('event_loop closed')
    