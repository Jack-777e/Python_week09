class ModifyStu :
    def execute(self,name,status,raw_data_dict) :
        scores={}
        dict={}
        subject=0
        new_score=0
        insert_new=False
        if(status==True):
            print("current subjects are", " ".join(raw_data_dict['scores'].keys()))
            subject=input("Please input a subject you want to change: ")
            if subject in raw_data_dict['scores'].keys():
                insert_new=False
                new_score=input(f"Please input {subject}'s new score of {name['name']}:")
            else:
                insert_new=True
                new_score=input(f"Add a new subject for {name['name']} please input {subject} score or < 0 for discarding the subject: ")

            try:
                new_score = float(new_score)
            except ValueError:
                print(f"Wrong format with reason could not convert string to float:'{new_score}'")

            if new_score >= 0:
                raw_data_dict['scores'][subject] =new_score
                scores['scores']=raw_data_dict['scores']
                dict['name'] = name['name']
                dict['scores_dict'] = scores['scores']
        return dict,name['name'],subject,new_score,insert_new
    
    def query_name(self):
        query_name={}
        query_name['name'] = input("Please input a student's name: ")
        return query_name
    

"""
Please select: modify
  Please input a student's name: Test2
    The client sent data => {'command': 'query', 'parameters': {'name': 'Test2'}}
    The client received data => {'status': 'OK', 'scores': {'Python': 11.0}}
  current subjects are Python

  Please input a subject you want to change: Eng
  Add a new subject for Test2 please input Eng score or < 0 for discarding the subject: 100
    The client sent data => {'command': 'modify', 'parameters': {'name': 'Test2', 'scores_dict': {'Python': 11.0, 'Eng': 100.0}}}
    The client received data => {'status': 'OK'}
    Add [Test2, Eng, 100.0] success

Please select: modify
  Please input a student's name: Test3
    The client sent data => {'command': 'query', 'parameters': {'name': 'Test3'}}
    The client received data => {'status': 'Fail', 'reason': 'The name is not found.'}
    The name Test3 is not found



Please select: modify
  Please input a student's name: Test2
    The client sent data => {'command': 'query', 'parameters': {'name': 'Test2'}}
    The client received data => {'status': 'OK', 'scores': {'Python': 11.0, 'Eng': 100.0}}
  current subjects are Python Eng 

  Please input a subject you want to change: Python
  Please input Python's new score of Test2: 19
    The client sent data => {'command': 'modify', 'parameters': {'name': 'Test2', 'scores_dict': {'Python': 19.0, 'Eng': 100.0}}}
    The client received data => {'status': 'OK'}
    Modify [Test2, Python, 19.0] success
"""