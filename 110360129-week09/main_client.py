import socket
import json
from AddStu import AddStu
from DelStu import DelStu
from ModifyStu import ModifyStu
from PrintAll import PrintAll
from SocketClient import SocketClient

action_list = {
    "add": AddStu,
    "del": DelStu,
    "modify":ModifyStu,
}

def main():
    keep_going = True
    while keep_going:
        print()
        print("add: Add a student's name and score")
        print("del: Delete a student")
        print("modify: Modify a student's score")
        print("show: Print all")
        print("exit: Exit")
        parameters={}
        query_name={}
        
        command = input(">>>")
        if (command != "exit") :
            if (command == "show") :
                parameters = ""
                socket_client.send_command(command,parameters)
                keep_going,raw_data_dict = socket_client.wait_response()
                status=action_success(raw_data_dict)
                if (status):
                    print_data=raw_data_dict["parameters"]
                    PrintAll(print_data).execute()
                else:
                    print("Fail to get student list.")
            else:
                try:
                    query_name = action_list[command]().query_name()
                except Exception as e :
                    print(f"Action list error :{e}")
                else:
                    socket_client.send_query(query_name)
                    keep_going,raw_data_dict = socket_client.wait_query_response()
                    if keep_going == False:
                        break
                    else:
                        status=action_success(raw_data_dict)
                        if command=="modify" :
                            parameters,name,subject,score,insert_new = action_list[command]().execute(query_name,status,raw_data_dict)
                            if parameters=={}:
                                print(f"The name {name} is not found")
                                continue
                        else:
                            parameters = action_list[command]().execute(query_name,status,raw_data_dict)
                        socket_client.send_command(command,parameters)
                        keep_going,raw_data_dict = socket_client.wait_response()
                        if action_success(raw_data_dict):
                            if command=="add": print(f"Add {parameters} success")
                            elif command=="del": print(f"Delete success")
                            elif command=="modify":
                                if insert_new : print(f"Add [{name},{subject},{score}] success")
                                else:print(f"Modify [{name},{subject},{score}] success")
                        else:
                            if command=="add": print(f"Add {parameters} Failed")
                            elif command=="del": print(f"Delete Failed")
                            elif command=="modify":print(f"The name {name} is not found")

        else :
            keep_going = False
            break
    
def action_success(raw_data_dict):
    if raw_data_dict["status"] == "OK" :
        return True
    else:
        return False

if __name__ == '__main__':
    socket_client=SocketClient()
    main()



"""
if (command == "add"):
    query_name = AddStu().query_name()
    SocketClient.send_command('query')
    keep_going = SocketClient.wait_response()
    if keep_going == False:
        break
    else:
        parameters = AddStu().execute(query_name)
        print(parameters)
if (command == "del") :
    query_name = DelStu().query_name()
    SocketClient.send_command('query')
    keep_going = SocketClient.wait_response()
    if keep_going == False:
        break
    else:
        parameters = DelStu().execute(query_name)
        print(parameters)
if (command == "modify") :
    query_name = ModifyStu().query_name()
    SocketClient.send_command('query')
    keep_going = SocketClient.wait_response()
    if keep_going == False:
        break
    else:
        parameters = ModifyStu().execute(query_name)
        print(parameters)
"""