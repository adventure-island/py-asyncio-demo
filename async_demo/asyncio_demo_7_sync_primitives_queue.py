# coding=utf-8
"""
Queues

An asyncio.Queue provides a first-in, first-out data structure for coroutines 
like a queue.Queue does for threads or a multiprocessing.Queue does for 
processes.
"""

import asyncio
import logging
import random

FORMAT = "[%(asctime)s][%(funcName)10s()] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

async def consumer(n: int, q: asyncio.Queue) -> None:
    
    logger.debug('consumer {}: starting'.format(n))
    while True:
        logger.debug('consumer {}: waiting for item'.format(n))
        item = await q.get()
        logger.debug('consumer {}: retrieved item {} from queue'.format(n, item))
        if item is None:
            logger.debug('consumer {}: got None from queue'.format(n))
            
            # None is the signal to stop.
            q.task_done()
            break
        else:
            seconds = random.randint(1, 7)
            logger.debug(f'consumer {n}: sleeping for {seconds} seconds')
            await asyncio.sleep(seconds)
            
            # Now signal the queue that the task has be completed
            logger.debug(f'consumer {n}: completed  task {item}')
            q.task_done()
            
    logger.debug('consumer {}: completed'.format(n))


async def producer(q: asyncio.Queue, num_workers: int):
    logger.debug('producer: starting')
    
    # Add 5 numbers to the queue to simulate jobs
    for i in range(5):
        logger.debug('producer: adding task {} to the queue...'.format(i))
        await q.put(i)
        logger.debug('producer: added task {} to the queue, pause for 3 seconds...'.format(i))
        # Pause for a few seconds to see consumer's reaction when task is retrieved
        await asyncio.sleep(2)
        
    # Add None entries in the queue
    # to signal the consumers to exit
    logger.debug('>>>>producer: adding stop signals to the queue')
    for i in range(num_workers):
        await q.put(None)
        
        
    logger.debug('producer: waiting for queue to empty by calling join()')
    await q.join()
    logger.debug('producer: ending')


async def main(loop, num_consumers):
    # Create the queue with a fixed size so the producer
    # will block until the consumers pull some items out.
    q = asyncio.Queue(maxsize=num_consumers)

    # Scheduled the consumer tasks.
    consumers = [
        loop.create_task(consumer(i, q))
        for i in range(num_consumers)
    ]

    # Schedule the producer task.
    prod = loop.create_task(producer(q, num_consumers))

    # Wait for all of the coroutines to finish.
    await asyncio.wait(consumers + [prod])


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop, 2))
finally:
    event_loop.close()