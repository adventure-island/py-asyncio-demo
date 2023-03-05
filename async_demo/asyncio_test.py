import asyncio

async def main():
    print("hello in main")
    # task = asyncio.create_task(foo("foo is here"))
    # print("main is sleeping")
    # await asyncio.sleep(3)
    await foo("foo is here")
    # await task
    # print("main is finished")
    # await task
    print("Main returned, all done")


async def main_still_sequential():
    print("hello in main, case demo - main_still_sequential")
    await foo("foo is here")
    print("Main returned, all done")

async def foo(msg):
    print(f"in foo - {msg}, sleeping")
    await asyncio.sleep(7)
    print(f"in foo - finished")


async def main_async_by_scheudling_task():
    print("hello in main, case demo - main_async_by_scheudling_task")
    task = asyncio.create_task(foo("foo is here"))
    print("Do sth in main for 3 secs")
    await asyncio.sleep(2.5)
    print("Small task in main returned after 2.5 secs")
    print("Awaiting task to return")
    await task
    print("Main returned, all done")

# asyncio.run(main_still_sequential())
asyncio.run(main_async_by_scheudling_task())
