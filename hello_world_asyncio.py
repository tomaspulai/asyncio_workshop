import asyncio
import time
import random


async def mock_io(io_delay):
    await asyncio.sleep(io_delay)
    return random.choice(["one", "two", "three", "four", "five"])


async def main():

    R1 = asyncio.create_task(mock_io(5), name="R1")
    R2 = asyncio.create_task(mock_io(1), name="R2")
    R3 = asyncio.create_task(mock_io(3), name="R3")

    # print(await R1)
    # print(await R2)
    # print(await R3)

    print(await asyncio.gather(R1, R2, R3))


asyncio.run(main())

#
# print(end - start)
#
# async def hello():
#     print("hello start")
#     await asyncio.sleep(1)
#     print("hello", end=" ", flush=True)
#
# async def world():
#     print("world start")
#     await asyncio.sleep(2)
#     print("world", end=" ", flush=True)
#
# async def via():
#     print("via start")
#     await asyncio.sleep(3)
#     print("via", end=" ", flush=True)
#
# async def async_io():
#     print("asyncio start")
#     await asyncio.sleep(4)
#     print("asyncio", end=" ", flush=True)
#
#
# async def main():
#     print("main start")
#     h = asyncio.create_task(hello())
#     w = asyncio.create_task(world())
#     v = asyncio.create_task(via())
#     a = asyncio.create_task(async_io())
#
#     print("gather")
#     await asyncio.gather(h,w,v,a)
#     print("main end")
#
# start = time.time()
# asyncio.run(main())
# print()
# print(time.time() - start)
#
