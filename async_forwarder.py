import asyncio
import json

from utils import *


# q = asyncio.Queue()

in_ip = "0.0.0.0"
in_port = 11111

out_ip = "localhost"
out_port = 11112


async def forward(reader, writer, direction):
    print(f"forwarding started: {direction} ")
    while True:
        try:
            msg = await read_msg(reader)
            if msg is None:
                print(f"forward {direction}: connection closed (EOF)")
                break
        except ConnectionError:
            print(f"ConnectionResetError occurred on reader {direction}")
            break

        # q.put_nowait(json.loads(msg))

        try:
            await write_msg(writer, msg)
        except ConnectionError:
            print(f"ConnectionAbortedError occurred on writer {direction}")
            break

    writer.close()
    try:
        await writer.wait_closed()
    except ConnectionError:
        pass

    print(f"forwarding stopped: {direction} ")


async def conn_handler(in_reader, in_writer):
    addr = in_writer.get_extra_info('peername')
    print(f"{addr} connected..trying to establish forwarding")

    out_reader, out_writer = await asyncio.open_connection(out_ip, out_port)
    print(f" {in_ip}, {in_port} forwarded to {out_ip}, {out_port}")

    task_in_out = asyncio.create_task(forward(in_reader, out_writer, "IN->OUT"))
    task_out_in = asyncio.create_task(forward(out_reader, in_writer, "OUT->IN"))

    await task_in_out
    await task_out_in


# async def read_queue():
#     while True:
#         msgs_to_insert = []
#
#         msgs_to_insert.append(await q.get())
#         while True:
#             try:
#                 msgs_to_insert.append(q.get_nowait())
#             except asyncio.QueueEmpty:
#                 break
#
#         print(f"writing {len(msgs_to_insert)} msgs to DB ")
#         await asyncio.sleep(1) #mocking the db write


async def start_server():

    server = await asyncio.start_server(conn_handler, in_ip, in_port)

    print(f'Serving on {server.sockets[0].getsockname()}')

    # read_task = asyncio.create_task(read_queue())

    async with server:
        await server.serve_forever()

    # await read_task

if __name__ == '__main__':
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("Keyboard interrupt occurred")
