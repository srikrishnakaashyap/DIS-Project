from os.path import isfile, join
import os
import time

from constants.global_constants import GC
import json
import socket


class CommandService:
    @staticmethod
    def getFile(filename, CLIENT_DIR):
        client_socket = GC.CLIENT_SOCKET

        client_socket.sendall(f"get {filename}".encode("utf-8"))
        header = client_socket.recv(1024).decode("utf-8")
        if header.startswith("file:"):
            _, filename, filesize = header.split(":")
            filesize = int(filesize)
            start_time = time.time()
            with open(os.path.join(CLIENT_DIR, filename), "wb") as f:
                bytes_received = 0
                while bytes_received < filesize:
                    chunk = client_socket.recv(min(1024, filesize - bytes_received))
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_received += len(chunk)
            return f"{filename} with {filesize} received successfully in {time.time() - start_time} time"

    @staticmethod
    def sendCommand(command, CLIENT_DIR):
        client_socket = GC.CLIENT_SOCKET
        if command.split(" ")[0] == "get":
            if len(command.split(" ")) == 2:
                file_name = command.split(" ")[1]
                print("File Name", file_name)

                return CommandService.getFile(file_name, CLIENT_DIR)
            else:
                return "Invalid Command"
        else:
            client_socket.sendall(command.encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8")
            return response

    @staticmethod
    def makeConnection(USERNAME, PASSWORD, CLIENT_DIR):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((GC.HOST, GC.PORT))

        client_socket.sendall(f"{USERNAME} {PASSWORD}".encode("utf-8"))
        response = client_socket.recv(1024).decode("utf-8")

        if response == "Authentication successful":
            if not os.path.exists(CLIENT_DIR):
                os.makedirs(CLIENT_DIR)

            GC.CLIENT_SOCKET = client_socket
            return True
        else:
            # print("Authentication failed")
            client_socket.close()
            return False
