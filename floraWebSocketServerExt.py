import threading
import asyncio
import socket
from queue import Queue, Empty
from TDStoreTools import StorageManager
import datetime

websockets = op('td_pip').ImportModule('websockets')
version = '0.3.3'
date = datetime.datetime.now().strftime("%m/%d/%Y")

class floraWebSocketServerExt:
    def __init__(self, ownerComp):
        self.ownerComp = ownerComp
        self.port = int(parent.FloraInParent.par.Port.eval())  # Directly read the port

        # Initialize StorageManager and store all relevant data there
        self.stored = StorageManager(self, self.ownerComp, [
            # {'name': 'server_thread', 'default': None},
            {'name': 'Port', 'default': self.port}
            # {'name': 'Server', 'default': None},
            # {'name': 'Loop', 'default': None},
            # {'name': 'Queue', 'default': None},
            # {'name': 'Clients', 'default': set()}
        ])
        self.server_thread = None
        self.server = None
        self.loop = None
        self.queue = None
        self.clients = set()  # Initialize clients if not stored
        
        # Load previously stored values
        self.port = self.stored['Port'] if self.stored['Port'] else int(parent.FloraInParent.par.Port.eval())
        parent.FloraInParent.par.Version = version
        parent.FloraInParent.par.Date = date

    def Start(self):
        # Stop the server if it's already running
        # if self.stored['server_thread'] and self.stored['server_thread'].is_alive():
        if self.server_thread and self.server_thread.is_alive():
            self.Stop()

        self.port = int(parent.FloraInParent.par.Port.eval())  # Directly read the port
        self.stored['Port'] = self.port  # Store the port

        # Prepare a queue for thread communication and store it
        self.queue = Queue()

        # Start the server in a new thread
        server_thread = threading.Thread(target=self._runServer)
        server_thread.daemon = True  # Ensure it terminates with the main process
        server_thread.start()

        # Store the thread reference in StorageManager
        # self.stored['server_thread'] = server_thread
        self.server_thread = server_thread

        # Monitor the queue for successful start
        try:
            success_message = self.queue.get(timeout=10)  # Wait for success or timeout after 10 seconds
            if success_message == "ServerStarted":
                debug("WebSocket server successfully started.")
                # op('websocket1').par.Active = True
                # op('websocket1').par.Port = self.port
                op('websocket1').par.reset.pulse()
            else:
                debug("Failed to start the WebSocket server.")
        except Empty:
            debug("Error: WebSocket server startup timed out.")

    def Stop(self):
        # Stop the server thread if it exists
        # if self.stored['server_thread'] and self.stored['server_thread'].is_alive():
        if self.server_thread and self.server_thread.is_alive():
            debug("Stopping the WebSocket server...")
            self._stopThread()

    def _runServer(self):
        # Create a new event loop and store it in StorageManager
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        server = None
        try:
            server = self.loop.run_until_complete(
                websockets.serve(self._handleConnection, 'localhost', self.port)
            )
            self.server = server
            self.queue.put("ServerStarted")  # Notify that server has started
            self.loop.run_forever()
        except Exception as e:
            self.queue.put("ServerFailed")
            debug(f"Error starting WebSocket server: {e}")
        finally:
            # Ensure cleanup even if an exception occurred
            self.loop.call_soon_threadsafe(self.loop.stop)  # Stop the event loop
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())  # Close async generators
            self.loop.close()
            self._releaseResources()

    def _stopThread(self):
        # Stop the server and release the port
        if self.server:
            debug("Closing WebSocket server and releasing port...")
            try:
                # Schedule the coroutine in the correct event loop
                future = asyncio.run_coroutine_threadsafe(self._closeServer(self.server), self.loop)
                future.result()  # Wait for the coroutine to complete
            except Exception as e:
                debug(f"Error closing the WebSocket server: {e}")
            self.server = None  # Clear stored server instance

        # Clear the thread and loop
        # self.stored['server_thread'] = None
        self.server_thread = None
        self.loop = None

    async def _closeServer(self, server):
        # Close the server and wait for it to release the port
        if server:
            server.close()
            # try:
            #     await asyncio.wait_for(server.wait_closed(), timeout=0.01)  # Set timeout to 2 seconds
            #     debug("Server closed and port released.")
            # except asyncio.TimeoutError:
            #     debug("Server close timed out.")

    def _releaseResources(self):
        """
        Releases the resources by shutting down the WebSocket server and closing connections.
        """
        if self.server:
            debug("Releasing WebSocket server resources...")
            # Gracefully close all active connections
            close_tasks = []
            for client in list(self.clients):
                try:
                    close_tasks.append(asyncio.create_task(self._closeClient(client)))
                except Exception as e:
                    debug(f"Error closing client: {e}")
                self.clients.remove(client)

            # Wait for all client close tasks to complete
            if close_tasks:
                asyncio.run(asyncio.gather(*close_tasks))

            if isinstance(self.server, asyncio.base_events.Server):
                asyncio.create_task(self._closeServer(self.server))

    async def _closeClient(self, client):
        # Close the client connection with a shorter timeout
        try:
            await asyncio.wait_for(client.close(close_timeout=1), timeout=1)
        except asyncio.TimeoutError:
            debug("Client close timed out.")
            
    async def _handleConnection(self, websocket, path):
        # Add the client to the stored set
        self.clients.add(websocket)
        debug(f"Client connected: {websocket}")
        try:
            async for message in websocket:
                await self._broadcastMessage(message, websocket)
        except websockets.exceptions.ConnectionClosed:
            debug("Client disconnected")
        finally:
            self.clients.remove(websocket)

    async def _broadcastMessage(self, message, sender):
        # Broadcast the message to all clients except the sender
        for client in self.clients:
            if client != sender:
                try:
                    await client.send(message)
                except websockets.exceptions.ConnectionClosed:
                    debug(f"Client {client} disconnected during broadcast.")