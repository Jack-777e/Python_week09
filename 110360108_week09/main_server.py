from threading import Thread
from sqlite_example.DBConnection import DBConnection
from sqlite_example.DBInitializer import DBInitializer
from sqlite_example.StudentInfoTable import StudentInfoTable
from sqlite_example.SubjectInfoTable import SubjectInfoTable
import socket
import json

host = "127.0.0.1"
port = 20001

class SocketServer(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The following setting is to avoid the server crash. So, the binded address can be reused
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.student_dict = {}
        DBConnection.db_file_path = "example.db"
        DBInitializer().execute()
        
        self.student_info_table = StudentInfoTable()
        self.subject_info_table = SubjectInfoTable()
        
        self.sync_with_database()

    def sync_with_database(self):
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT stu_id, name FROM student_info")
            students = cursor.fetchall()
            
            for student in students:
                student_id = student["stu_id"]
                student_name = student["name"]
                
                cursor.execute(
                    "SELECT subject, score FROM subject_info WHERE stu_id = ?",
                    (student_id,),
                )
                subjects = cursor.fetchall()
                
                scores = {subject["subject"]: subject["score"] for subject in subjects}
                self.student_dict[student_name] = {"name": student_name, "scores": scores}

    def serve(self):
        self.start()

    def run(self):
        while True:
            connection, address = self.server_socket.accept()
            print(f"{address} connected")
            self.new_connection(connection=connection, address=address)

    def new_connection(self, connection, address):
        Thread(target=self.receive_message_from_client,
               kwargs={"connection": connection, "address": address}, daemon=True).start()

    def receive_message_from_client(self, connection, address):
        keep_going = True
        while keep_going:
            try:
                message = connection.recv(1024).strip().decode()
            except Exception as e:
                print(f"Exception: {e}, {address}")
                keep_going = False
            else:
                if not message:
                    keep_going = False
                message = json.loads(message)
                if message["command"] == "close":
                    connection.send("closing".encode())
                    keep_going = False
                else:
                    self.process_message(message, connection, address)

        connection.close()
        print(f"{address} close connection")

    def process_message(self, message, connection, address):
        print(message)
        if message["command"] == "query":
            Query.execute(self, connection, address, message)
        elif message["command"] == "add":
            AddStu.execute(self, connection, address, message)
        elif message["command"] == "del":
            DelStu.execute(self, connection, address, message)
        elif message["command"] == "show":
            PrintAll.execute(self, connection, address, message)
        elif message["command"] == "modify":
            ModifyStu.execute(self, connection, address, message)

class AddStu:
    @staticmethod
    def execute(server, connection, address, message):
        reply_msg = {"status": "OK"}
        print(f"server received:{message} from {address}")
        student_name = message["parameters"]["name"]
        server.student_dict[student_name] = message["parameters"]
        server.student_info_table.insert_a_student(student_name)
        scores = message["parameters"].get("scores", {})
        stu_id = server.student_info_table.select_a_student(student_name)[0]

        for subject, score in scores.items():
            server.subject_info_table.insert_subject_info(stu_id, subject, score)

        connection.send(json.dumps(reply_msg).encode())

class Query:
    @staticmethod
    def execute(server, connection, address, message):
        reply_msg = {"status": "OK", "scores": {}}
        print(f"server received:{message} from {address}")
        student_name = message["parameters"]["name"]

        if student_name in server.student_dict:
            scores = server.student_dict[student_name].get("scores", {})
            reply_msg["scores"] = scores
        else:
            reply_msg["status"] = "Fail"
            reply_msg["reason"] = "Student not found."
            
        connection.send(json.dumps(reply_msg).encode())

class PrintAll:
    @staticmethod
    def execute(server, connection, address, message):
        print(f"server received:{message} from {address}")
        reply_msg = {"status": "OK", "parameters": server.student_dict}
        connection.send(json.dumps(reply_msg).encode())

class DelStu:
    @staticmethod
    def execute(server, connection, address, message):
        print(f"server received:{message} from {address}")
        reply_msg = {"status": "OK"}
        student_name = message["parameters"]["name"]
        
        if student_name in server.student_dict:
            del server.student_dict[student_name]
        
        stu_id = server.student_info_table.select_a_student(student_name)[0]
        server.student_info_table.delete_a_student(stu_id)
        server.subject_info_table.delete_subject_info(stu_id)

        connection.send(json.dumps(reply_msg).encode())

class ModifyStu:
    @staticmethod
    def execute(server, connection, address, message):
        reply_msg = {"status": "OK"}
        print(f"server received:{message} from {address}")
        student_name = message["parameters"]["name"]
        
        if student_name in server.student_dict:
            scores = server.student_dict[student_name].get("scores", {})
            new_scores = message["parameters"].get("scores", {})
            scores.update(new_scores)
            server.student_dict[student_name]["scores"] = scores
            
            stu_id = server.student_info_table.select_a_student(student_name)[0]

            for subject, score in new_scores.items():
                existing_scores = server.subject_info_table.select_subject_info(stu_id)
                if subject in existing_scores:
                    server.subject_info_table.update_subject_info(stu_id, subject, score)
                else:
                    server.subject_info_table.insert_subject_info(stu_id, subject, score)

        connection.send(json.dumps(reply_msg).encode())

if __name__ == '__main__':
    server = SocketServer(host, port)
    server.daemon = True
    server.serve()

    while True:
        command = input()
        if command == "finish":
            break

    server.server_socket.close()
    print("leaving ....... ")
