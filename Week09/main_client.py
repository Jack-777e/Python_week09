import socket 
import json
from client_func.AddStu import AddStu
from client_func.PrintAll import PrintAll
from client_func.ModifyStu import ModifyStu
from client_func.DelStu import DelStu

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
            return json.loads(raw_data)
        
        return json.loads(raw_data)
    
def print_menu():
    print()
    print("add: Add a student's name and score")
    print("del: Delete a student")
    print("modify: Modify a student's score")
    print("show: Print all")
    print("exit: Exit")
    selection = input("Please select: ")

    return selection

if __name__ == '__main__':
    client = SocketClient(host, port)

    select_result = "initial"
    while select_result != "exit":
        select_result = print_menu()
        try:
            action_list[select_result](client).execute()
        except Exception as e:
            print(e)
'''
{
    'Bill': {
        'name': 'Bill', 
        'scores': {
            'English': 99.0, 
            'Chinese': 60.0
        }
    }
}
'''