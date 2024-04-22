from client.Query import Query

class DelStu:
    @staticmethod
    def execute(client):
        keep_going = True
        while keep_going:
            student_name = input("Please input a student's name or exit: ")
            student_dict = {"name":""}   
            if student_name == "exit":
                keep_going = False
            else:
                status, scores= Query.execute(client, student_name)
                student_dict["name"] = student_name
                if status == "OK":
                    choose = input("Confirm to delete (y/n): ")
                    if str.lower(choose) == 'y': 
                        client.send_command("del", student_dict)
                        raw_data = client.wait_response()
                        print(f"delete {'success' if raw_data['status'] == 'OK' else 'Fail'}")
                else:
                    keep_going = False       
