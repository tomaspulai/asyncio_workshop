import asyncio
import random
import time

async def mock_io(io_delay):
    task_name = asyncio.current_task().get_name()
    print(f"{task_name} started")
    await asyncio.sleep(io_delay)
    print(f"{task_name} finihed")

    return random.choice(["one", "two", "three", "four", "five"])


async def main():
    print("create R1")
    R1 = asyncio.create_task(mock_io(5), name="R1")
    print("create R2")
    R2 = asyncio.create_task(mock_io(1), name="R2")
    print("create R3")
    R3 = asyncio.create_task(mock_io(3),name="R3")

    print("gather")
    print(await asyncio.gather(R1, R2, R3))

start = time.time()
asyncio.run(main())
end = time.time()

print(end - start)

