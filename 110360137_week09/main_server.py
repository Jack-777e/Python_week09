from threading import Thread
import socket
import json
from sqlite_example.DBConnection import DBConnection
from sqlite_example.DBInitializer import DBInitializer
from sqlite_example.StudentInfoTable import StudentInfoTable
from sqlite_example.SubjectInfoTable import SubjectInfoTable

host = "127.0.0.1"
port = 20001
BUFFER_SIZE = 1940
student_data = {}

class SocketServer:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.initialize_database()

    def initialize_database(self):
        DBConnection.db_file_path = "example.db"
        DBInitializer.execute()

    def serve(self):
        while True:
            connection, address = self.server_socket.accept()
            print("{} connected".format(address))
            self.new_connection(connection=connection, address=address)

    def new_connection(self, connection, address):
        data = connection.recv(BUFFER_SIZE)
        message = json.loads(data.decode())
        command = message.get('command')
        if command == "show":
            if student_data:
                response = {'status': 'OK', 'parameters': student_data}
            else:
                response = {'status': 'No data.'}
            connection.send(json.dumps(response).encode())
        elif command == "add":
            self.add_student(message)
            response = {'status': 'OK'}
            connection.send(json.dumps(response).encode())
        elif command == "exit":
            response = {'status': 'closing'}
            connection.send(json.dumps(response).encode())
            connection.close()
        else:
            response = {'status': 'Error', 'message': 'Invalid command'}
            connection.send(json.dumps(response).encode())

    def add_student(self, message):
        parameters = message.get('parameters')
        name = parameters.get('name')
        scores = parameters.get('scores')
        student_data[name] = {'name': name, 'scores': scores}
        StudentInfoTable.insert_a_student(name)
        stu_id = StudentInfoTable.select_a_student(name)[0]
        for subject, score in scores.items():
            SubjectInfoTable.insert_subject_info(stu_id, subject, score)

if __name__ == '__main__':
    server = SocketServer(host, port)
    server.serve()
