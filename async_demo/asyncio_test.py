import asyncio

async def main():
    print("hello")
    task = asyncio.create_task(foo("foo is here"))
    print("main is sleeping")
    await asyncio.sleep(3)
    # await foo("foo is here")
    # await task
    print("main is finished")
    await task
    print("Main returned, all done")


async def foo(msg):
    print(f"in foo - {msg}")
    await asyncio.sleep(12)
    print(f"in foo - finished")

asyncio.run(main())