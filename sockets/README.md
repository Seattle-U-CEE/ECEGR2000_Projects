# Sockets

## Server

To instantiate [Server class](./server.py):
```
server = Server(5050, initiator=True)
server.start()
```
In this example, the server opens TCP port `5050`, and will initiate communications.

### methods

#### send_all(str:command)

Sends a command to all connected clients.

#### send(str:command, str:client_ip, int:client_port)

Sends a command to a specific connected client with IP `client_ip` and port `client_port`.

## Client

To instantiate [Client class](./client.py):
```
server_ip = "127.0.0.1"
client = Client(server_ip, 5050, initiator=False)
client.start()
```
In this example, the client will connect to the server at IP `127.0.0.1` on TCP port `5050`, and will not initiate communications.

### methods
#### send(str:command)

Sends a command to the server.

## Testing

Each Server and Client can run as stand-alone.
On the server device:
```
python server.py
```
The server will open TCP port 5050.
On the client device:
```
python client.py
```
The client will prompt the user for the server IP address. In the default test code, the server will initiate communication.
