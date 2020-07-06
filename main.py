from utilities.hash_table import HashTable
from utilities.parser import Parser
from utilities.formatter import Formatter
import datetime

INPUT_FILE_PATH = './inputPS12.txt'
INPUT_PROMPTS_FILE_PATH = './promptsPS12.txt'
OUTPUT_FILE_PATH = './outputPS12.txt'
VALID_YEAR = datetime.datetime.now().year - 10


class StudentManagement:
    def __init__(self):
        self.dep_records = HashTable()
        self.hall_of_fame_records = HashTable()
        self.new_course_candidate_records = HashTable()
        self.formatter = Formatter()

    def initializeHash(self):
        self.student_records = HashTable()
    
    def insertStudentRec(self, student_id, CGPA):
        department = student_id[4:7]
        if not self.dep_records.has(department):
            dep = HashTable()
            dep.set('max', 0.0)
            dep.set('avg', 0.0)
            self.dep_records.set(department, dep) # max and avg
        self.student_records.set(student_id, CGPA)
    
    def hallOfFame(self, maxCGPA):
        for student_id in self.student_records.keys():
            cgpa = self.student_records[student_id]
            year = int(student_id[0:4])
            if cgpa >= maxCGPA and year <= VALID_YEAR:
                self.hall_of_fame_records[student_id] = cgpa
        num_of_eligible_students = len(self.hall_of_fame_records)
        return self.formatter.format_hall_of_fame(num_of_eligible_students, self.hall_of_fame_records)

    def newCourseList(self, CGPAFrom, CPGATo):
        for student_id in self.student_records.keys():
            cpga = self.student_records[student_id]
            year = int(student_id[0:4])
            valid_year = datetime.datetime.now().year - 5
            if CGPAFrom <= cpga <= CPGATo and year <= valid_year:
                self.new_course_candidate_records[student_id] = cpga
        num_of_eligible_students = len(self.new_course_candidate_records)
        return self.formatter.format_new_course_candidates(num_of_eligible_students, self.new_course_candidate_records, CGPAFrom, CPGATo)
    
    def depAvg(self):
        for department in self.dep_records.keys():
            department_list = list(filter(lambda record: record[4:7] == department, self.student_records.keys()))
            department_list = list(map(lambda student_id: self.student_records[student_id], department_list))
            self.dep_records[department]['max'] = max(department_list)
            #NOTE: Rounding the average for two significant digits
            self.dep_records[department]['avg'] = round(sum(department_list) / len(department_list), 2)
        return self.formatter.format_department_cgpa(self.dep_records)

    def destroyHash(self):
        self.student_records.prune()


if __name__ == '__main__':
    student_management = StudentManagement()
    student_management.initializeHash()

    parser = Parser()
    input_student_records = parser.student_file_parser(INPUT_FILE_PATH, '/')
    min_cgpa, max_cgpa = parser.prompts_parser(INPUT_PROMPTS_FILE_PATH, ':')

    if not min_cgpa or not max_cgpa or input_student_records == []:
        print("Some error occured while parsing the files or there might be format/range errors in the files")
        print("So, exiting ...")
        exit()

    # Lazy evaluation of map in python3.
    # https://stackoverflow.com/questions/19342331/python-map-calling-a-function-not-working
    s = list(map(lambda record: student_management.insertStudentRec(record[0], record[1]), input_student_records))
    
    # uncomment them if you want to see the records
    # print(student_management.student_records.keys())
    # print(student_management.student_records.values())

    print(f"Got a total record of {len(student_management.student_records)} students")
    
    final_string = ""
    print("Calculating the hall of fame .....")
    final_string += student_management.hallOfFame(max_cgpa) #TODO: Write this into file

    print("Calculating new course candidates .....")
    final_string += student_management.newCourseList(min_cgpa, max_cgpa) #TODO: Write this into file

    print("Calculating the maximum and average for each department.....")
    final_string += student_management.depAvg() #TODO: Write this into file

    print("Outputting into the outputPS12.txt.....")
    parser.final_output_parser(OUTPUT_FILE_PATH, final_string)

    print("Pruning the student records.........")
    student_management.student_records.prune()
