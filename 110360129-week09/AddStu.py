class AddStu :
    def execute(self,name,status,raw_data_dict) :
        if(status==False):
            print("add: Add a student's name and score")
            student_exit = False
            student_dict={}
            while not student_exit:
                subject_exit = False
                scores={}
                while not subject_exit:
                    subject = input("Please input a subject name or 'exit' for ending: ")
                    if subject.lower() == "exit":
                        subject_exit = True
                        student_exit = True
                        break
                    while True:
                        try:
                            score_input = input(f"Please input {name}'s {subject} score or < 0 for discarding the subject: ")
                            score = float(score_input)
                            break
                        except ValueError:
                            print(f"Wrong format with reason could not convert string to float:'{score_input}', try again.")
                    if score >= 0:
                        scores[subject] =score
                        student_dict['name'] = name['name']
                        student_dict['scores'] = scores
            return student_dict
    
    def query_name(self):
        query_name={}
        query_name['name'] = input("Please input a student's name: ")
        return query_name
