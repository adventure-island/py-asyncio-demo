# coding=utf-8
"""Waiting for Multiple Coroutines

In situations where the order of execution doesn't matter, and where there may 
be an arbitrary number of operations, wait() can be used to pause one coroutine
until the other background operations complete.

"""

import asyncio
import time
import logging

FORMAT = "[%(asctime)s][%(funcName)10s()] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

# Adjust asyncio module's logging level
# logging.getLogger("asyncio").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


async def mycoro(task_id: int) -> str:
    logger.debug(f'Starting task {task_id}, sleeping {task_id} seconds...')
    
    try:
        await asyncio.sleep(task_id)
    except asyncio.CancelledError:
        logger.debug(f'Task {task_id} was canceled')
        raise
    
    logger.debug(f'Finishing task {task_id}') # Runs later
    return str(task_id)


async def main(num_tasks: int, timeout=None):
    logger.debug('starting main')
    tasks = [
        mycoro(i)
        for i in range(num_tasks)
    ]
    
    
    start = time.perf_counter()
    
    """
    Internally, wait() uses a `set` to hold the Task instances it creates. This 
    results in them starting, and finishing, in an unpredictable order. The 
    return value from wait() is a tuple containing two sets holding the finished 
    and pending tasks.
    
    There will only be pending operations left if wait() is used with a timeout 
    value.
    """
    logger.debug('Calling wait() to wait for tasks to complete')
    completed, pending = await asyncio.wait(tasks, timeout=timeout)
    
    finish = time.perf_counter()
    
    logger.debug('wait returned {} completed tasks and {} pending tasks'.format(
        len(completed), len(pending)
    ))
    
    results = [t.result() for t in completed]
    logger.debug('results: {!r}'.format(results))
    
    logger.debug(f"All tasks finished in {round(finish-start, 2)} second(s)")
    
    # Cancel remaining tasks so they do not generate errors
    # as we exit without finishing them.
    if pending:
        logger.debug('canceling tasks')
        for t in pending:
            t.cancel()
    logger.debug('exiting main')
    

event_loop = asyncio.get_event_loop()
try:
    logger.debug('calling run_until_complete')
#     event_loop.run_until_complete(main(5))
    event_loop.run_until_complete(main(5, timeout=2))
    logger.debug('run_until_complete returned')
finally:
    logger.debug('closing event_loop')
    event_loop.close()
    logger.debug('event_loop closed')
    