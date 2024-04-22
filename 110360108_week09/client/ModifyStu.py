from client.Query import Query

class ModifyStu:
    @staticmethod
    def execute(client):
        keep_going = True
        while keep_going:
            student_name = input("Please input a student's name or 'exit': ")
            if student_name == "exit":
                keep_going = False
                continue

            status, scores = Query.execute(client, student_name)
            if status is None:
                print(f"The name {student_name} is not found.")
                continue

            current_subjects = " ".join(scores.keys())
            print(f"Current subjects are: {current_subjects}")

            subject = input("Please input a subject you want to change: ")

            if subject in scores:
                new_score = float(input(f"Please input {subject}'s new score for {student_name}: "))
                if new_score >= 0:
                    scores[subject] = new_score
                    client.send_command("modify", {"name": student_name, "scores": scores})
                    raw_data = client.wait_response()
                    if raw_data["status"] == "OK":
                        print(f"Modified [{student_name}, {subject}, {new_score}] successfully")
                    else:
                        print("Modification failed.")
                else:
                    print("Invalid score.")
        
            else:
                new_score = float(input(f"Please input {subject}'s score or < 0 for discarding: "))
                if new_score >= 0:
                    scores[subject] = new_score
                    client.send_command("modify", {"name": student_name, "scores": scores})
                    raw_data = client.wait_response()
                    if raw_data["status"] == "OK":
                        print(f"Added [{student_name}, {subject}, {new_score}] successfully")
                    else:
                        print("Addition failed.")
                else:
                    print("Discarded addition.")

            keep_going = False
