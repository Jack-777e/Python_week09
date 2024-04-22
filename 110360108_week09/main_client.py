import socket
import json
from client.AddStu import AddStu
from client.PrintAll import PrintAll
from client.DelStu import DelStu
from client.ModifyStu import ModifyStu

host = "127.0.0.1"
port = 20001
BUFFER_SIZE = 1940

action_list = {
    "add": AddStu, 
    "del": DelStu, 
    "modify": ModifyStu, 
    "show": PrintAll
}

class SocketClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        
    def send_command(self, command, student_dict):
        send_data = {'command': command, 'parameters': student_dict}
        self.client_socket.send(json.dumps(send_data).encode())
        print(f"The client sent data =>{send_data}")
    
    def wait_response(self):
        data = self.client_socket.recv(BUFFER_SIZE)
        raw_data = data.decode()
        print(f"The client received data =>{raw_data}")
        if raw_data == "closing":
            return False
        return json.loads(raw_data)
        
if __name__ == '__main__':
    client = SocketClient(host, port)

    keep_going = True
    while keep_going:
        print()
        print("add: Add a student's name and score")
        print("del: Delete a student")
        print("modify: Modify a student's score")
        print("show: Print all")
        print("exit: Exit")
        command = input("Please select: ")
        if (command != "exit") :
            try:
                action_list[command].execute(client)
            except:
                pass
        else :
            client.send_command("close",{})
            keep_going = client.wait_response()
