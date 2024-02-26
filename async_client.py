
import asyncio
import json
import uuid
import datetime
from utils import custom_handler, write_msg, read_msg

outstanding_msgs = []
msgs_count = 0

async def send_msgs_loop(writer):

    with open("msgs.json") as f:
        msgs = json.load(f)

        global msgs_count
        msgs_count = len(msgs)

        for msg in msgs:

            msg["id"] = str(uuid.uuid4())
            outstanding_msgs.append(msg["id"])

            msg = json.dumps(msg)

            try:
                await write_msg(writer, msg)
            except ConnectionError:
                print(f"send_msgs_loop connection error")
                break
            else:
                print(f"sent: {msg}")


async def read_msgs_loop(reader):

    received_count = 0
    while True:
        try:
            msg = await read_msg(reader)

            if msg is None:
                print("read_msgs_loop: connection closed (EOF)")
                break

            msg = json.loads(msg)
            if msg["id"] in outstanding_msgs:
                received_count = received_count + 1
                outstanding_msgs.remove(msg["id"])
                print(f"received: {msg}")

        except ConnectionError:
            print(f"read_msgs_loop: connection error")
            break

        if not outstanding_msgs and received_count == msgs_count:
            print("all responses received")
            break

async def start_client():

    asyncio.get_running_loop().set_exception_handler(custom_handler)

    reader, writer = await asyncio.open_connection("localhost", 11111)

    send_task = asyncio.create_task(send_msgs_loop(writer))
    receive_task = asyncio.create_task(read_msgs_loop(reader))

    await send_task
    await receive_task

if __name__ == '__main__':
    try:
        asyncio.run(start_client(), debug=False)
    except KeyboardInterrupt:
        print("Keyboard interrupt occurred")
