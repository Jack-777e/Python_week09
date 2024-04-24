class DelStu :
    def execute(self,name,status,raw_data_dict) :
        if(status):
            confirm=input("Confirm to delete (y/n):")
            if confirm=='y':
                dict={}
                dict= name
                print(dict)
                return dict

    def query_name(self):
        query_name={}
        query_name['name'] = input("Please input a student's name: ")
        return query_name

"""
Please select: del
    Please input a student's name: Test2
        The client sent data => {'command': 'query', 'parameters': {'name': 'Test2'}}
        he client received data => {'status': 'OK', 'scores': {'Python': 19.0, 'Eng': 100.0}}
    Confirm to delete (y/n): y
        The client sent data => {'command': 'delete', 'parameters': {'name': 'Test2'}}
        The client received data => {'status': 'OK'}
        Delete success
"""