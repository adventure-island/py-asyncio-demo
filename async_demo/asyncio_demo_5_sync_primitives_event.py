# coding=utf-8
"""
Events

An asyncio.Event is based on threading.Event, and is used to allow multiple 
consumers to wait for something to happen without looking for a specific value 
to be associated with the notification.
"""

import asyncio
import logging
import functools

FORMAT = "[%(asctime)s][%(funcName)10s()] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)


async def coro1(event):
    logger.debug('coro1 waiting for event')
    await event.wait()
    logger.debug('coro1 triggered')


async def coro2(event):
    logger.debug('coro2 waiting for event')
    await event.wait()
    logger.debug('coro2 triggered')


def set_event(event):
    logger.debug('setting event in callback')
    event.set()
    
async def main(loop):
    # Create a shared event
    event = asyncio.Event()
    logger.debug('event start state: {}'.format(event.is_set()))

    # Trigger the event with a delay
    loop.call_later(
        3, functools.partial(set_event, event)
    )

    await asyncio.wait([coro1(event), coro2(event)])
    logger.debug('event end state: {}'.format(event.is_set()))


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()