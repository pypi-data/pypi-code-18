from .student import *

class Classroom():
    def __init__(self, zipfiles, tasks = [], unzip = True):
        self.zipfiles = zipfiles
        self.unzip = unzip
        self.tasks = tasks
        self.students = self.createStudents()

    def createStudents(self):
        students = []
        for zipfile in self.zipfiles:
            student = Student(zipfile)
            if self.unzip:
                student.unzip()
            students.append(student)
        return students

    def addStudentsTasks(self):
        for student in self.students:
            student.addTasks(self.tasks)

    def runTasks(self):
        for student in self.students:
            print(student.name)
            student.runAll()

    def undesired(self, desired, remove = True):
        for student in self.students:
            student.undesired(desired, remove)

    def saveResults(self, out_path):
        with open(out_path, 'w') as file:
            file.write("Name,User,Comments\n")
            for student in self.students:
                file.write(student.comments_text+"\n")
