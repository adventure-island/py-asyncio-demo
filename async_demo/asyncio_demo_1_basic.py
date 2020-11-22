
import logging
import asyncio

FORMAT = "[%(threadName)s][%(funcName)10s()] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

# Adjust asyncio module's logging level
# logging.getLogger("asyncio").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

async def mycoro(task_id: int) -> str:
    logger.debug(f'Starting task {task_id}')
    
    try:
        await asyncio.sleep(1)
    except asyncio.CancelledError:
        logger.debug(f'Task {task_id} was canceled')
        raise
    
    logger.debug(f'Finishing task {task_id}') # Runs later
    return str(task_id)


def run_demo_warning():
    """Demonstrate the warning of starting tasking without waiting."""
    
    # Before Python 3.7
    c = mycoro(3)
#     myfuture1 = asyncio.ensure_future(c)
    # Python 3.7+
    # This creates and runs coroutine
    task = asyncio.create_task(c)
    

def run_demo_ensure_future():
    """Demonstrate waiting for task completion.ensure_future create_task"""
    
    c = mycoro(3)
    task = asyncio.ensure_future(c)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    loop.close()    
    
    
def run_demo_create_task():
    """Demonstrate executing task using `create_task`.
    
    To start a task, use create_task() to create a Task instance. The resulting 
    task will run as part of the concurrent operations managed by the event 
    loop as long as the loop is running and the coroutine does not return.
    """
    
    async def main(loop):
        logger.debug(f'Creating task 1')
        task = loop.create_task(mycoro(1))
        logger.debug(f'Waiting for task 1')
        return_value = await task
        logger.debug(f'Task completed and returned: {return_value}')
    
    
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop))
    finally:
        logger.debug('Closing event loop')
        event_loop.close()
    

def run_demo_run_py37():
    """Demonstrate waiting for task completion with Python 3.7+."""
    
    c = mycoro(3)
    asyncio.run(c)
    
    
def run_demo_gather():
    """Demonstrate combining task together."""
    
    many = asyncio.gather(
        mycoro(1),
        mycoro(2),
        mycoro(3),
        mycoro(4),
        mycoro(5)
    )
    
    logger.debug(f"Return type: {type(many)}")
    
    # won't work
#     asyncio.run(many)

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(many)
    loop.close()
    
    # will return a list of results in the same order as its input.
    logger.debug(f"result: {result}")


# -----------------------------------------------
# Demonstrate calling coroutines

def run_demo_calling_coro():
    """Demonstrate calling coroutines."""
    
    async def f2():
        logger.debug("start f2")
        await asyncio.sleep(1)
        logger.debug("stop f2")
        
    async def f1():
        logger.debug("start f1")
        # f2() will not be executed without `await`
        await f2()
        logger.debug("stop f1")
        
    loop = asyncio.get_event_loop()
    loop.run_until_complete(f1())
    loop.close()
    
    
def run_demo_canceling():
    """Demonstrate canceling tasks.
    
    Create and then cancel a task before starting the event loop. The result is
    a CancelledError exception from run_until_complete()
    """
    
    async def main(loop):
        logger.debug('Creating task 1')
        task = loop.create_task(mycoro(1))
        
        logger.debug('Canceling task')
        task.cancel()
    
        logger.debug(f'Canceled task {task}')
        
        try:
            await task
        except asyncio.CancelledError:
            logger.debug('Caught error from canceled task')
        else:
            logger.debug('Task result: {!r}'.format(task.result()))
    
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop))
    finally:
        event_loop.close()    
    

def run_demo_canceling_while_waiting():
    """Demonstrate canceling tasks.
    
    If a task is canceled while it is waiting for another concurrent operation, 
    the task is notified of its cancellation by having a CancelledError 
    exception raised at the point where it is waiting.
    """
    
    def task_canceller(t):
        logger.debug('in task_canceller')
        t.cancel()
        logger.debug('canceled the task')


    async def main(loop):
        logger.debug('creating task')
        task = loop.create_task(mycoro(3))
        
        logger.debug('scheduling canceler task')
        '''
        `call_soon` schedules the `task_canceller` callback to be called with 
        `task` arguments at the next iteration of the event loop.
        '''
        loop.call_soon(task_canceller, task)
        
        try:
            logger.debug('waiting task')
            await task
        except asyncio.CancelledError:
            logger.debug('main() also sees task as canceled')
    
    
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop))
    finally:
        event_loop.close()
       
if __name__ == '__main__': 
#     run_demo_warning()
#     run_demo_ensure_future()
#     run_demo_create_task()
#     run_demo_run_py37()
    run_demo_gather()
#     run_demo_calling_coro()
#     run_demo_canceling()
#     run_demo_canceling_while_waiting()
    
