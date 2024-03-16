import asyncio
import json


from utils import *

import time

# TPS = 1
# delay = 1/TPS


async def send_msgs_loop(writer):
    with open("msgs.json") as f:
        msgs = json.load(f)

        for msg in msgs:
            # await asyncio.sleep(delay)
            msg = json.dumps(msg)
            try:
                await write_msg(writer, msg)
            except ConnectionError:
                print(f"send_msgs_loop connection error")
                break
            else:
                print(f"sent: {msg}")


# async def read_msgs_loop(reader, end_signal):
#
#     while not end_signal.is_set():
#         try:
#             msg = await asyncio.wait_for(read_msg(reader), timeout=5.0)
#         except asyncio.TimeoutError:
#             continue
#
#         if msg is None:
#             break
#
#         text_color = TermColors.GREEN
#         if json.loads(msg)["result"] == "APPROVE":
#             text_color = TermColors.RED
#
#         print(f"{text_color}rcvd: {msg}{TermColors.ENDC}")


async def start_client():
    reader, writer = await asyncio.open_connection("localhost", 11111)

    # end_signal = asyncio.Event()

    send_task = asyncio.create_task(send_msgs_loop(writer))
    # read_task = asyncio.create_task(read_msgs_loop(reader, end_signal))

    await send_task
    # await asyncio.sleep(5)
    # end_signal.set()
    # await read_task

if __name__ == '__main__':
    try:
        asyncio.run(start_client())
    except KeyboardInterrupt:
        print("Keyboard interrupt occurred")
