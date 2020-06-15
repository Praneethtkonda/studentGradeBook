from utilities.hash_table import HashTable
from utilities.parser import Parser
from utilities.formatter import Formatter

INPUT_FILE_PATH = './inputPS12.txt'
INPUT_PROMPTS_FILE_PATH = './propmtsPS12.txt'
OUTPUT_FILE_PATH = './outputPS12.txt'


class StudentManagement:
    def __init__(self):
        #TODO: Need to fill any
        print()

    def initializeHash(self):
        self.student_records = HashTable()
    
    def insertStudentRec(self, studentId, CGPA):
        self.student_records.set(studentId, CGPA)
    
    def hallOfFame(self):
        #TODO: Write Code
        print()
    
    def newCourseList(self, CGPAFrom, CPGATo):
        #TODO: Write Code
        print()
    
    def depAvg(self):
        #TODO: Write Code
        print()

    def destroyHash(self):
        print("Pruning the student records.........")
        self.student_records.prune()


if __name__ == '__main__':
    student_management = StudentManagement()
    student_management.initializeHash()

    parser = Parser()
    input_student_records = parser.file_parser(INPUT_FILE_PATH, '/')
    
    # Lazy evaluation of map in python3.
    # https://stackoverflow.com/questions/19342331/python-map-calling-a-function-not-working
    s = list(map(lambda record: student_management.insertStudentRec(record[0], record[1]), input_student_records))
    
    print(student_management.student_records.keys())
    print(student_management.student_records.values())

