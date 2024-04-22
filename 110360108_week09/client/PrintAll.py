class PrintAll:
    @staticmethod
    def execute(client):
        client.send_command('show', {})
        raw_data = client.wait_response()
        data = raw_data['parameters']
        print ("\n==== student list ====")
        
        for name, scores in data.items(): 
            print(f"\nName: {name}")
            for subject, score in scores['scores'].items():
                print(f"  subject: {subject}, score: {score}")
                
        print ("\n======================")
