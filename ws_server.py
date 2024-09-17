import asyncio
import websockets
import atexit

connected_clients = set()
server = None

async def handler(websocket, path):
    # Register client
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast message to all connected clients except the sender
            for client in list(connected_clients):  # Create a copy of the set
                if client != websocket:
                    try:
                        await client.send(message)
                    except websockets.exceptions.ConnectionClosedOK:
                        connected_clients.discard(client)  # Remove disconnected client
    finally:
        # Unregister client
        connected_clients.discard(websocket)  # Use discard to avoid KeyError

async def ping_clients():
    while True:
        await asyncio.sleep(10)  # Ping every 10 seconds
        for client in list(connected_clients):  # Create a copy of the set
            try:
                await client.ping()
            except websockets.exceptions.ConnectionClosed:
                connected_clients.discard(client)  # Use discard to avoid KeyError

def initialize_server(host="localhost", port=8080):
    global server
    server = websockets.serve(handler, host, port)

async def start_server():
    global server
    loop = asyncio.get_event_loop()
    server_instance = await server
    loop.create_task(ping_clients())
    try:
        await server_instance.wait_closed()
    except asyncio.CancelledError:
        pass

async def stop_server():
    global server
    if server:
        server_instance = await server
        server_instance.close()
        await server_instance.wait_closed()

def cleanup():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(stop_server())

# Register the cleanup function to be called on exit
atexit.register(cleanup)

# Example usage:
initialize_server()
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server())