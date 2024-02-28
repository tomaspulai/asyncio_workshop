from utils import *

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

        except ConnectionError:
            break

    print(f"{addr} closed")


async def start_server():
    server = await asyncio.start_server(conn_handler, "0.0.0.0", 11112)

    print(f'Serving on {server.sockets[0].getsockname()}')

    async with server:
        await server.serve_forever()

try:
    asyncio.run(start_server())
except KeyboardInterrupt:
    print("keyboard interrupt occurred")