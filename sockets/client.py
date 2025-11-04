from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, activeCount
from time import sleep
from traceback import format_exc
from signal import signal, SIGTERM, SIGINT
from sys import exit


FORMAT = 'UTF-8'
BUFFER = 1024


class Client(Thread):
    def __init__(self, ip, port, initiator=False):
        super().__init__()
        self.daemon = True
        self.port = port
        self.addr = (ip, port)
        self.initiator = initiator
        self.client = None
        self.isRunning = True
        self.isConnected = False
        self.command = None

    def run(self):
        while self.isRunning:
            print(f"[CONNECTING TO SERVER {self.addr[0]}:{self.addr[1]} ...]")
            while not self.isConnected and self.isRunning:
                try:
                    self.client = socket(AF_INET, SOCK_STREAM)
                    self.client.connect(self.addr)
                    self.isConnected = True
                    break
                except:
                    try:
                        self.client.close()
                    except:
                        pass
                    self.isConnected = False
                    sleep(0.5)
            if self.isConnected:
                print("[CONNECTED TO SERVER]")
            while self.isConnected and self.isRunning:
                try:
                    if self.initiator:

                        # Waits for a command. When done programmatically, remove this print
                        print("[TYPE A COMMAND] > ", end="", flush=True)
                        while self.command is None and self.isRunning:
                            sleep(0.5)
                        if not self.isRunning:
                            break
                        self.client.send(self.command.encode(FORMAT))
                        print(f"[SENT TO SERVER] '{self.command}'")
                        self.command = None

                        # Waits for a response
                        msg = self.client.recv(BUFFER).decode(FORMAT)
                        print(f"[RECEIVED] '{msg}'")
                        if msg in ["", "DISCONNECTED"]:
                            self.isConnected = False
                            break
                    else:
                        print("[WAITING FOR SERVER MESSAGE]")
                        msg = self.client.recv(BUFFER).decode(FORMAT)
                        print(f"[RECEIVED] '{msg}'")
                        if msg in ["", "DISCONNECT"]:
                            self.isConnected = False
                            break

                        # ADD VALID COMMAND HANDLERS HERE, if good send 'ok', if not 'err'
                        response = "ok"

                        self.client.send(response.encode(FORMAT))
                        print(f"[SENT TO SERVER] '{response}'")

                except:
                    # print(format_exc())
                    self.isConnected = False
                    self.command = None
                    try:
                        self.client.close()
                    except Exception:
                        pass
            try:
                self.client.close()
            except:
                pass
            print("[SERVER DISCONNECTED]")

    def send(self, cmd):
        self.command = cmd

    def stop(self):
        print("Client stopping ...")
        self.isRunning = False
        try:
            exit(0)
        except:
            pass


def signal_handler(signum, frame):
    print("\nExiting...")
    try:
        exit(0)
    except:
        raise SystemExit()


if __name__ == "__main__":
    signal(SIGINT, signal_handler)
    signal(SIGTERM, signal_handler)
    client = None
    try:
        server_ip = input("Enter the server IP: ")
        client = Client(server_ip, 5050, initiator=False)
        client.start()
        while True:
            command = input()
            client.send(command)
            sleep(0.5)
    except:
        # print(format_exc())
        if client is not None:
            client.send("DISCONNECT")
            client.stop()
            client.join()
        try:
            exit(0)
        except:
            pass
