import socket
import json

BUFFER_SIZE = 1940
class SocketClient:
    def __init__(self):
        host = "127.0.0.1"
        port = 20001
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        
    def send_command(self,command,parameters):
        self.add_data=parameters
        send_data = {'command': command , 'parameters': parameters}
        print(f"The client sent data =>{send_data}")
        self.client_socket.send(json.dumps(send_data).encode())
    
    def send_query(self,query_name):
        send_data = {'command': 'query' , 'parameters': query_name}
        print(f"The client sent data =>{send_data}")
        self.client_socket.send(json.dumps(send_data).encode())
    
    def wait_response(self):
        data = self.client_socket.recv(BUFFER_SIZE)
        raw_data = data.decode()
        print(f"The client received data => {raw_data}")
        raw_data_dict = json.loads(raw_data)
        if raw_data == "closing":
            return False
        return True,raw_data_dict
    
    def wait_query_response(self):
        data = self.client_socket.recv(BUFFER_SIZE)
        raw_data = data.decode()
        print(f"The client received data => {raw_data}")
        raw_data_dict = json.loads(raw_data)
        if raw_data == "closing":
            return False
        return True,raw_data_dict
