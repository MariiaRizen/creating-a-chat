import asyncio
from datetime import datetime


async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    if message[0] == '?':
        if message == '?date':
            message = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        elif message == '?hello':
            message = 'hello friend'
        elif message == '?goodbye':
            message = 'See you late'
        else:
            message = 'Dont have that command'
    else:
        print(f"Send: {message!r}")

    message = message.encode()
    print(f"Send: {message!r}")
    writer.write(message)
    await writer.drain()

    print("Close the connection")
    writer.close()


async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 18888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
