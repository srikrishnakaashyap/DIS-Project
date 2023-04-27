import socket
import os


def getFile(client_socket, filename):
    client_socket.sendall(f"get {filename}".encode("utf-8"))
    header = client_socket.recv(1024).decode("utf-8")
    if header.startswith("file:"):
        _, filename, filesize = header.split(":")
        filesize = int(filesize)
        with open(os.path.join(CLIENT_DIR, filename), "wb") as f:
            bytes_received = 0
            while bytes_received < filesize:
                chunk = client_socket.recv(min(1024, filesize - bytes_received))
                if not chunk:
                    break
                f.write(chunk)
                bytes_received += len(chunk)
        print(f"{filename} received successfully")


def sendCommand():
    # pass

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    client_socket.sendall(f"{USERNAME} {PASSWORD}".encode("utf-8"))
    response = client_socket.recv(1024).decode("utf-8")

    if response == "Authentication successful":
        while True:
            command = input("> ").strip()
            if command.split(" ")[0] == "get":
                if len(command.split(" ")) == 2:
                    print("File Name", file_name)
                    file_name = command.split(" ")[1]
                    getFile(client_socket, file_name)
                else:
                    print("Invalid Command")
            else:
                client_socket.sendall(command.encode("utf-8"))
                response = client_socket.recv(1024).decode("utf-8")
                print(response)
    else:
        print("Authentication failed")
        client_socket.close()


if __name__ == "__main__":
    s = input("Enter the device name: ")

    global HOST
    global PORT
    global USERNAME
    global PASSWORD
    global CLIENT_DIR

    HOST = "localhost"
    PORT = 12345
    USERNAME = "admin"
    PASSWORD = "password"
    CLIENT_DIR = "cliet_dir"

    sendCommand()
