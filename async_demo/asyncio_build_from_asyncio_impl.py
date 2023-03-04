from math import sqrt
import asyncio

def fib():
    
    a = 2
    b = 1
    yield a
    while True:
#         print(f'yielding {b}')
        yield b
        a, b = b, a + b
        
async def is_prime(x):
    if x < 2:
        return False

    for i in range(2, int(sqrt(x))+1):
        if x % i == 0:
            return False
        # yield to avoid blocking on large numbers
        await asyncio.sleep(0)
  
    return True 


async def search(iterable, predicate):
    
    print('search')
    for item in iterable:
#         print(f'search - checking {item}')
        if await predicate(item):
            print('predicate returned True')
            return item

        await asyncio.sleep(0)

    raise ValueError("Not found")
  

async def print_matches(iterable, async_predicate):
    for item in iterable:
        # ` yield from` allows the predicate to make progress
        # and yield control back to caller
        matches = await async_predicate(item)
        if matches:
            print(f"Found: {item}")

async def repetitive_message(msg, interval_secs):
    # Periodically print a message
    while True:
        print(msg)
        await asyncio.sleep(interval_secs)  
        

loop = asyncio.get_event_loop()
    
search_task = asyncio.ensure_future(
    print_matches(fib(), is_prime), loop=loop
)
 

repetitive_task = asyncio.ensure_future(
    repetitive_message('This is an async message!', 2), 
    loop=loop
)

all_future = asyncio.gather(search_task, repetitive_task)

loop.run_until_complete(all_future)
loop.close()
     

