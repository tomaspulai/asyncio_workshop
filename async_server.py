import asyncio
import json
import random
from utils import custom_handler, read_msg, write_msg


async def conn_handler(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"{addr} connected")

    while True:
        try:
            msg = await read_msg(reader)

            if msg is None:
                print("conn_handler: connection closed (EOF)")
                break

            print(f"received: {msg}")

            msg = json.loads(msg)
            msg["result"] = random.choice(["approve", "decline"])
            msg = json.dumps(msg)

            await write_msg(writer, msg)

            print(f"sent: {msg}")
        except ConnectionError:
            break

    print(f"{addr} closed")


async def start_server():
    asyncio.get_running_loop().set_exception_handler(custom_handler)

    server = await asyncio.start_server(conn_handler, "0.0.0.0", 11112)

    print(f'Serving on {server.sockets[0].getsockname()}')

    async with server:
        await server.serve_forever()


try:
    asyncio.run(start_server())
except KeyboardInterrupt:
    print("keyboard interrupt occurred")