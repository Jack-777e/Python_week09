from client.Query import Query

class AddStu:
    @staticmethod
    def execute(client):
        Keep_going = True
        while Keep_going:
            name = input("Please input a student's name or exit: ")
            if name == "exit":
                Keep_going = False
            student_dict = {'name' : name, 'scores' : {}}
            status, score = Query.execute(client, name)
            if status is None :
                while True:
                    subject = input("Please input a subject name or exit for ending: ")
                    if subject == "exit":
                        Keep_going = False
                        break
                    while True:
                        try:
                            score = float(input(f"Please input {name}'s {subject} score or < 0 for discarding the subject: "))
                            if score >= 0:
                                student_dict['scores'][subject] = score
                                break
                            else:
                                break
                        except ValueError as V:
                            print(f"Wrong format with reason {V}, try again")
                client.send_command('add', student_dict)
                raw_data = client.wait_response()
                print(f"Add {student_dict} {'success' if raw_data['status'] == 'OK' else 'Fail'}")
                Keep_going = False
            else:
                pass
