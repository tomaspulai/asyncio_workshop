import asyncio
import json
from utils import *


async def send_msgs_loop(writer):

    with open("msgs.json") as f:
        msgs = json.load(f)

        for msg in msgs:
            msg = json.dumps(msg)

            try:
                await write_msg(writer, msg)
            except ConnectionError:
                print(f"send_msgs_loop connection error")
                break
            else:
                print(f"sent: {msg}")


async def start_client():
    reader, writer = await asyncio.open_connection("localhost", 11112)
    send_task = asyncio.create_task(send_msgs_loop(writer))
    await send_task


if __name__ == '__main__':
    try:
        asyncio.run(start_client(), debug=False)
    except KeyboardInterrupt:
        print("Keyboard interrupt occurred")
