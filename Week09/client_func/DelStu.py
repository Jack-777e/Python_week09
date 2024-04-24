class DelStu:
    def __init__(self, client):
        self.client = client

    def execute(self):
        name = input("Please input a student's name or exit: ")
        if str.lower(name) == "exit":
            return
        self.client.send_command('query', name)
        raw_data = self.client.wait_response()
        if raw_data['status'] == 'OK':
            confirm = str.lower(input("Confirm to delete (y/n): "))
            if confirm == 'y':
                self.client.send_command('delete', {'name': name})
                raw_data = self.client.wait_response()
                print(f"Del {name} success")
            else:
                print(f"Del {name} fail")
        else:
            print(f"The name {name} is not found")