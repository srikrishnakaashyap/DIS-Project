import socket
import os
import shutil
import traceback
import select
import threading


client_sockets = []
CREDENTIALS = {}


def cleanup(client_dir):
    """Delete the client's private directory."""
    shutil.rmtree(client_dir)


def handle_client(conn, addr, username):
    client_dir = f"{username}_dir"
    while True:
        data = conn.recv(1024).decode("utf-8")
        if not data:
            break

        command = data.split()[0]
        args = data.split()[1:]

        if command == "ls":
            response = "\n".join(os.listdir("."))
        elif command == "cd":
            try:
                path = os.path.join(client_dir, command[3:])

                if not os.path.abspath(path).startswith(os.path.abspath(client_dir)):
                    raise ValueError("Access denied")
                os.chdir(path)
                # os.chdir(args[0])
                response = "Directory changed"
            except:
                response = "Unable to change directory"
        elif command == "pwd":
            response = os.getcwd().replace(client_dir, "", 1)
        elif command == "get":
            try:
                filename = args[0]
                filepath = os.path.join(client_dir, filename)
                print("filePath", filepath, filename)
                try:
                    filesize = os.path.getsize(filename)
                    print("File Size", filesize)
                except Exception:
                    print("Error")
                    filesize = 200
                    traceback.print_exc()

                with open(filename, "rb") as f:
                    conn.sendall(f"file:{filename}:{filesize}".encode("utf-8"))
                    while True:
                        chunk = f.read(1024)
                        if not chunk:
                            break
                        conn.sendall(chunk)
            except:
                response = "Unable to get file"
        else:
            response = "Unknown command"

        conn.sendall(response.encode("utf-8"))


def process():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Server listening on port {PORT}")

    while True:
        try:
            read_sockets, _, _ = select.select([server_socket] + client_sockets, [], [])
        except Exception as e:
            print("112", e)

        for sock in read_sockets:
            conn, addr = sock.accept()
            authenticated = False

            while not authenticated:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    break

                username, password = data.split()

                if username in CREDENTIALS and password in CREDENTIALS[username]:
                    authenticated = True
                    client_dir = f"{username}_dir"

                    if not os.path.exists(client_dir):
                        os.makedirs(client_dir)

                    conn.sendall("Authentication successful".encode("utf-8"))
                else:
                    conn.sendall("Authentication failed".encode("utf-8"))

                print("Authenticated", authenticated)

            if authenticated:
                t = threading.Thread(target=handle_client, args=(conn, addr, username))
                t.start()
                # handle_client(conn, addr, username)


if __name__ == "__main__":
    # global HOST
    # global PORT
    # global USERNAME
    # global PASSWORD

    HOST = "localhost"
    PORT = 12345
    CREDENTIALS["kaashyap"] = "test"
    CREDENTIALS["abhilash"] = "test"
    CREDENTIALS["test"] = "test"

    process()
