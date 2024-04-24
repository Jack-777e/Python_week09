import json
from sqlite_example.SubjectInfoTable import SubjectInfoTable
from sqlite_example.StudentInfoTable import StudentInfoTable

class AddStu:
    def __init__(self):
        pass

    def execute(self):
        name = input("Please input a student's name: ")
        subject_scores = {}
        while True:
            subject = input("Please input a subject name or 'exit' to finish: ")
            if subject.lower() == "exit":
                break
            score = float(input(f"Please input {name}'s {subject} score or < 0 for discarding the subject: "))
            subject_scores[subject] = score

        self.add_student_info(name, subject_scores)
        print("Student added successfully.")

    def add_student_info(self, name, subject_scores):
        StudentInfoTable.insert_a_student(name)
        stu_id = StudentInfoTable.select_a_student(name)[0]
        for subject, score in subject_scores.items():
            SubjectInfoTable.insert_subject_info(stu_id, subject, score)

if __name__ == "__main__":
    add_stu = AddStu()
    add_stu.execute()
