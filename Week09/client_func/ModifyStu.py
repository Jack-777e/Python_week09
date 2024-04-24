class ModifyStu:
    def __init__(self, client):
        self.client = client

    def execute(self):
        name = input("Please input a student's name or exit: ")
        if str.lower(name) == "exit":
            return
        self.client.send_command('query', name)
        raw_data = self.client.wait_response()
        if raw_data['status'] == 'OK':
            print("current subjects are", *raw_data['scores'])
            subject = input("Please input a subject you want to change: ")
            if subject in raw_data['scores'].keys():
                try:
                    score = float(input(f"Please input {subject}'s new score of {name}: "))
                except Exception as e:
                    print(f"Wrong format with reason {e}")
                if score >= 0:
                    self.execute_score(name, subject, score, raw_data['scores'])
                    print(f"Modify [{name}, {subject}, {score}] success")
            else:
                try:
                    score = float(input(f"Add a new subject for {name} please input {subject} score or < 0 for discarding the subject: "))
                except Exception as e:
                    print(f"Wrong format with reason {e}")
                if score >= 0:
                    self.execute_score(name, subject, score, raw_data['scores'])
                    print(f"Add [{name}, {subject}, {score}] success")
        else:
            print(f"The name {name} is not found")
        
    def execute_score(self, name, subject, score, scores_dict):
        scores_dict[subject] = score
        parameters = {'name': name, 'scores_dict': scores_dict}
        self.client.send_command('modify', parameters)
        raw_data = self.client.wait_response()
