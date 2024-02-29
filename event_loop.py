import datetime
import asyncio


def print_now():
    print(datetime.datetime.now())


def trampoline(name=""):
    print(name, end=" ")
    print_now()
    loop.call_later(0.5, trampoline, name)


def hog():
    print("hog start")
    sum = 0
    for i in range(10_000):
        for j in range(10_000):
            sum += j

    print("hog end")
    return sum


loop = asyncio.get_event_loop()

loop.call_soon(trampoline, "One")
loop.call_soon(trampoline, "Two")
loop.call_soon(trampoline, "Three")

loop.call_later(5, hog)

loop.call_later(15, loop.stop)

loop.run_forever()
