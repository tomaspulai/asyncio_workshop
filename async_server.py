import asyncio
import json
import random

from utils import *

ip = "0.0.0.0"
port = 11112

#
# TPS_LOW = 100
# TPS_HIGH = 200
#
# low_delay = 1/TPS_LOW
# high_delay = 1/TPS_HIGH


async def conn_handler(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"{addr} connected")

    while True:
        try:
            # await asyncio.sleep(random.uniform(low_delay, high_delay))
            msg = await read_msg(reader)

            if msg is None:
                print("conn_handler: connection closed (EOF)")
                break

            msg = json.loads(msg)
            print(f"received: {msg}")

            # msg["result"] = random.choice(["APPROVE", "DECLINE"])

            # text_color = TermColors.GREEN
            # if msg["result"] != "APPROVE":
            #     text_color = TermColors.RED
            # print(f"{text_color}{msg['result']}{TermColors.ENDC}")
            #
            # msg = json.dumps(msg)
            #
            # await write_msg(writer, msg)

        except ConnectionError:
            break

    print(f"{addr} closed")


async def start_server():
    #asyncio.get_running_loop().set_exception_handler(custom_handler)
    server = await asyncio.start_server(conn_handler, ip, port)

    print(f'Serving on {server.sockets[0].getsockname()}')

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("Keyboard interrupt occurred")
