import socket
import json
from AddStu import AddStu
from PrintAll import PrintAll

host = "127.0.0.1"
port = 20001
BUFFER_SIZE = 1940

class SocketClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.add_stu = AddStu(self.client_socket)
        self.print_all = PrintAll()

    def send_command(self, command):
        send_data = {'command': command}
        self.client_socket.send(json.dumps(send_data).encode())

    def wait_response(self):
        data = self.client_socket.recv(BUFFER_SIZE)
        raw_data = data.decode()
        print(raw_data)

        if raw_data == "closing":
            return False
        return True


if __name__ == '__main__':
    client = SocketClient(host, port)

    print("add: Add a student's name and score")
    print("show: Print all")
    print("exit: Exit")

    keep_going = True
    while keep_going:
        command = input("Please select: ")
        if command.lower() == "add":
            client.add_stu.execute()
        elif command.lower() == "show":
            client.print_all.execute()
        elif command.lower() == "exit":
            client.send_command("exit")
            keep_going = client.wait_response()
        else:
            client.send_command(command)
            keep_going = client.wait_response()
