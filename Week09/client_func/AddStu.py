class AddStu:
    def __init__(self, client):
        self.client = client
        
    def execute(self):
        exit = False
        while not exit:
            name = input("Please input a student's name or exit: ")
            if str.lower(name) == "exit":
                break
            self.client.send_command('query', name)
            raw_data = self.client.wait_response()
            student_dict = {'name' : name, 'scores' : {}}
            while raw_data['status'] == 'Fail':
                subject = input("Please input a subject name or exit for ending: ")
                if str.lower(subject) == "exit":
                    self.client.send_command('add', student_dict)
                    raw_data = self.client.wait_response()
                    if raw_data['status'] == 'OK':
                        print(f"Add {student_dict} success")
                    elif raw_data['status'] == 'Fail':
                        print(f"Add {student_dict} fail")
                    exit = True
                    break
                while True:
                    try:
                        score = float(input(f"Please input {name}'s {subject} score or < 0 for discarding the subject: "))
                    except Exception as e:
                        print(f"Wrong format with reason {e}, try again")
                        continue
                    if score >= 0:
                        student_dict['scores'][subject] = score
                    break

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