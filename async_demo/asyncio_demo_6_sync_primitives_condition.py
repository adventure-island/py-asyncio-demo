# coding=utf-8
"""
Conditions

A Condition works similarly to an Event except that rather than notifying all 
waiting coroutines the number of waiters awakened is controlled with an 
argument to notify().
"""

import asyncio
import logging

FORMAT = "[%(asctime)s][%(funcName)10s()] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)


async def consumer(condition, n):
    async with condition:
        logger.debug('consumer {} is waiting'.format(n))
        await condition.wait()
        logger.debug('consumer {} triggered'.format(n))
    logger.debug('ending consumer {}'.format(n))


async def manipulate_condition(condition):
    logger.debug('starting manipulate_condition')

    # pause to let consumers start
    await asyncio.sleep(2)

    # Notify 1 consumer in the first the iteration
    # then notify 2 consumer in the second iteration
    # then notify all remaining awaiting consumers 
    for i in range(1, 3):
        async with condition:
            logger.debug('notifying {} consumers'.format(i))
            condition.notify(n=i)
        await asyncio.sleep(3)

    async with condition:
        logger.debug('notifying remaining consumers')
        condition.notify_all()

    logger.debug('ending manipulate_condition')


async def main(loop):
    # Create a condition
    condition = asyncio.Condition()

    # Set up tasks watching the condition
    consumers = [
        consumer(condition, i)
        for i in range(5)
    ]

    # Schedule a task to manipulate the condition variable
    loop.create_task(manipulate_condition(condition))

    # Wait for the consumers to be done
    await asyncio.wait(consumers)


event_loop = asyncio.get_event_loop()
try:
    result = event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
    