from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread, activeCount
from time import sleep
from traceback import format_exc
from signal import signal, SIGTERM, SIGINT
from sys import exit


FORMAT = 'UTF-8'
BUFFER = 1024


class Server(Thread):
    def __init__(self, port, initiator=True):
        super().__init__()
        self.daemon = True
        self.port = port
        self.addr = ("0.0.0.0", port)
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.active_connections = activeCount()
        self.initiator = initiator
        self.isRunning = True
        self.commands = {"ALL": None}
        self.thread = None

    def __handle_client(self, conn, addr):
        try:
            print(f"[NEW CONNECTION] {addr[0]}:{addr[1]} connected.")
            connected = True
            self.commands[f"{addr[0]}:{addr[1]}"] = None
            while connected and self.isRunning:
                if self.initiator:

                    # Waits for a command. When done programmatically, remove this print
                    print("[TYPE A COMMAND] > ", end="", flush=True)
                    while self.commands["ALL"] is None and self.commands[f"{addr[0]}:{addr[1]}"] is None and self.isRunning:
                        sleep(0.5)
                    command = None
                    if not self.isRunning:
                        break
                    elif self.commands["ALL"] is not None:
                        command = self.commands["ALL"]
                        self.commands["ALL"] = None
                    else:  # use socket command
                        command = self.commands[f"{addr[0]}:{addr[1]}"]
                        self.commands[f"{addr[0]}:{addr[1]}"] = None
                    conn.send(command.encode(FORMAT))
                    print(f"[SENT TO CLIENT {addr[0]}:{addr[1]}] \'{command}'")

                    # Waits for a response
                    msg = conn.recv(BUFFER).decode(FORMAT)
                    print(f"[RECEIVED] '{msg}'")
                    if msg in ["", "DISCONNECT"]:
                        connected = False
                        break

                else:
                    print("[WAITING FOR CLIENT MESSAGE]")
                    msg = conn.recv(BUFFER).decode(FORMAT)
                    print(f"[RECEIVED] '{msg}'")
                    if msg in ["", "DISCONNECT"]:
                        connected = False
                        break

                    # ADD VALID COMMAND HANDLERS HERE, if good send 'ok', if not 'err'
                    response = "ok"

                    conn.send(response.encode(FORMAT))
                    print(f"[SENT TO CLIENT {addr[0]}:{addr[1]}] \'{response}'")

            conn.close()
        except:
            # print(format_exc())
            pass
        print(f"[CLIENT {addr[0]}:{addr[1]} DISCONNECTED]")

    def run(self):
        self.server.bind(self.addr)
        self.server.listen()
        print(f"[LISTENING] Server is listening on port {self.port}")
        self.active_connections = activeCount()
        while self.isRunning:
            try:
                conn, addr = self.server.accept()
                self.thread = Thread(target=self.__handle_client, args=(conn, addr), daemon=True)
                self.thread.start()
            except:
                # print(format_exc())
                self.isRunning = False

    def send_all(self, command):
        self.commands["ALL"] = command

    def send(self, command, client_ip, client_port):
        self.commands[f"{client_ip}:{client_port}"] = command

    def stop(self):
        print("Server stopping ...")
        self.isRunning = False
        if self.thread is not None:
            self.thread.join()
        try:
            exit(0)
        except:
            raise SystemExit()


def signal_handler(signum, frame):
    print("\nExiting...")
    try:
        exit(0)
    except:
        raise SystemExit()


if __name__ == "__main__":
    signal(SIGINT, signal_handler)
    signal(SIGTERM, signal_handler)
    server = None
    try:
        server = Server(5050, initiator=True)
        server.start()
        while True:
            command = input()
            server.send_all(command)
            sleep(0.5)
    except:
        # print(format_exc())
        if server is not None:
            server.send_all("DISCONNECT")
            server.stop()
            server.join()
        try:
            exit(0)
        except:
            pass


