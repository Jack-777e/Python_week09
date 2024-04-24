import json
from sqlite_example.SubjectInfoTable import SubjectInfoTable

class PrintAll:
    def __init__(self):
        pass

    def execute(self):
        response = self.get_student_data()
        print(response)

    def get_student_data(self):
        student_data = {}
        all_subject_info = SubjectInfoTable.select_all_subject_info()
        for record in all_subject_info:
            stu_id, subject, score = record
            if stu_id not in student_data:
                student_data[stu_id] = {"stu_id": stu_id, "scores": {subject: score}}
            else:
                student_data[stu_id]["scores"][subject] = score
        return student_data

if __name__ == "__main__":
    print_all = PrintAll()
    print_all.execute()
