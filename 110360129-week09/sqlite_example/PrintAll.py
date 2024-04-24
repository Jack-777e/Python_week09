
class PrintAll :
    def __init__(self, raw_data_dict):
        self.data = raw_data_dict

    def execute(self) :
        print("\n==== Student List ====")
        if not self.data:
            print("",end="")
        else:
            for name, info in self.data.items():
                print(f"\nName: {name}")
                if "scores" in info:
                    scores = info["scores"]
                    for subject, score in scores.items():
                        print(f" Subject: {subject}, Score: {score}")
                else:
                    print(" No scores found for this student.")
        print("\n======================")
        return