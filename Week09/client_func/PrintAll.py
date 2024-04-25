class PrintAll:
    def __init__(self, client):
        self.client = client
        
    def execute(self):
        self.client.send_command('show', {})
        raw_data = self.client.wait_response()
        data = raw_data['parameters']
        print ("\n==== student list ====\n")
        for name in data.keys():
            print(f"Name: {name}")
            for subject, score in data[name]['scores'].items():
                print(f"  subject: {subject}, score: {score}")
            print()
        print ("======================")
