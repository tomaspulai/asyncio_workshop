import asyncio


def custom_handler(loop, context):
    exception = context.get("exception")
    if isinstance(exception, KeyboardInterrupt):
        # Ignore it
        return
    else:
        # Call the default exception handler
        loop.default_exception_handler(context)


async def read_msg(reader):
    try:
        msg_len = int.from_bytes(await reader.readexactly(2), byteorder="big")
        return await reader.readexactly(msg_len)

    except asyncio.IncompleteReadError:
        return None


async def write_msg(writer, msg):
    msg_len = len(msg)
    msg_len = msg_len.to_bytes(2, byteorder="big")

    if isinstance(msg, str):
        msg = msg.encode()

    writer.write(msg_len + msg)
    await writer.drain()


async def write_msg_slow_network(writer, msg, chunk_size = 2):
    msg_len = len(msg)
    msg_len = msg_len.to_bytes(2, byteorder="big")

    if isinstance(msg, str):
        msg = msg.encode()

    writer.write(msg_len)
    await writer.drain()

    for i in range(0, len(msg), 2):
        await asyncio.sleep(0.1)
        writer.write(msg[i:i+chunk_size])
        await writer.drain()





