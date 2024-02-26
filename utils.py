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
