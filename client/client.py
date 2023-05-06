import socket
import os
import readline

commands = ["ls", "cd", "pwd", "get"]

readline.parse_and_bind("tab: complete")
readline.set_completer_delims(" ")


def getFile(client_socket, filename):
    print("calling getFile")
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
    s = f"{USERNAME} {PASSWORD}".encode("utf-8")

    client_socket.sendall(s)
    response = client_socket.recv(1024).decode("utf-8")

    if response == "Authentication successful":
        if not os.path.exists(CLIENT_DIR):
            os.makedirs(CLIENT_DIR)
        while True:
            command = input("> ").strip()
            completer = readline.get_completer()
            readline.set_completer(
                lambda text, state: completer(text, state)
                if state is not None
                else commands
            )
            # set up history
            readline.set_history_length(1000)
            readline.write_history_file(os.path.join(CLIENT_DIR, "history"))

            try:
                client_socket.sendall(command.encode("utf-8"))
                response = client_socket.recv(1024).decode("utf-8")
                print(response)
            except KeyboardInterrupt:
                pass
            except:
                print("Connection error. Closing socket.")
                client_socket.close()
                break

            if command.split(" ")[0] == "get":
                if len(command.split(" ")) == 2:
                    file_name = command.split(" ")[1]
                    print("File Name", file_name)

                    getFile(client_socket, file_name)
                else:
                    print("Invalid Command")

            # else:
            #     client_socket.sendall(command.encode("utf-8"))
            #     response = client_socket.recv(1024).decode("utf-8")
            #     print(response)
    else:
        print("Authentication failed")
        client_socket.close()


if __name__ == "__main__":
    global HOST
    global PORT
    global USERNAME
    global PASSWORD
    global CLIENT_DIR

    HOST = "localhost"
    PORT = 12345
    USERNAME = input("Enter the username: ")
    PASSWORD = input("Enter the password: ")
    CLIENT_DIR = "cliet_dir"

    sendCommand()
