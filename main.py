from utilities.hash_table import MyHashTable
from utilities.parser import Parser
from utilities.formatter import Formatter
import datetime

INPUT_FILE_PATH = './inputPS12.txt'
INPUT_PROMPTS_FILE_PATH = './promptsPS12.txt'
OUTPUT_FILE_PATH = './outputPS12.txt'
# Students who graduate on and before 2020 i.e From 2010 - 2014 batch to 2016 - 2020 batch assuming 10th anniversary will be on 2020
VALID_START_YEAR_FOR_GRADUATION = datetime.datetime.now().year - 4


class StudentManagement:
    def __init__(self):
        """Initializer method which sets a formatter instance as a member.
           Formatter class has methods which gives you a formatted string based on the input value
        """
        self.formatter = Formatter()

    def initializeHash(self):
        """Initializes the hashtables for students, hall of fame records, department wise records and new course candidate records"""
        self.student_records = MyHashTable()
        self.dep_records = MyHashTable()
        self.hall_of_fame_records = MyHashTable()
        self.new_course_candidate_records = MyHashTable()
    
    def insertStudentRec(self, student_id, CGPA):
        """Inserts the Student records in the Hash Table and initializes the department wise records with default values"""
        department = student_id[4:7]
        if not self.dep_records.has(department):
            dep = MyHashTable()
            # Setting default max and avg values for each department
            dep.set('max', 0.0)
            dep.set('avg', 0.0)
            self.dep_records.set(department, dep) # max and avg
        self.student_records.set(student_id, CGPA)
    
    def hallOfFame(self, maxCGPA):
        """Inserts the student in hall_of_fame_records hashtable if he falls under hall of fame category
           Criteria:-
           We are assuming the maxCGPA from the promptsPS12.txt as the maxcpga.
           Example:-
           2013ECE2809/3.1 => Not valid because of less cpga
           2017ECE2811/4.1 => Not valid because, he is not yet graduated 2017 + 4 <= 2020 (max graduated year)
           2013CSE2807/4.1 => Valid because he will be graduated on 2013 + 4 <= 2020
        """
        for student_id in self.student_records.keys():
            cgpa = self.student_records[student_id]
            year = int(student_id[0:4])
            if cgpa >= maxCGPA and self._is_graduate(year) and year <= VALID_START_YEAR_FOR_GRADUATION:
                self.hall_of_fame_records[student_id] = cgpa
        num_of_eligible_students = len(self.hall_of_fame_records)
        return self.formatter.format_hall_of_fame(num_of_eligible_students, self.hall_of_fame_records)

    def newCourseList(self, CGPAFrom, CPGATo):
        """Inserts the student in new_course_candidate_records hashtable if he falls under prescribed category
           Criteria:-
           We are taking the CGPAFrom, CPGATo from the promptsPS12.txt
           Also, he should be graduated on or before the year 2018, considering the current academic year as 2019 - 2020
           Example:-
           2013MEC2608/3.1 => Not valid because of cpga is not in range of 3.5 and 4.0
           2017ECE2811/4.1 => Not valid because, he is not yet graduated 2017 + 4 <= 2020 (max graduated year)
           2011CSE1250/3.6 => Valid because he will be graduated on 2011 + 4 (2015) <= 2018
        """
        for student_id in self.student_records.keys():
            cpga = self.student_records[student_id]
            year = int(student_id[0:4])
            # Students graduated in the last five years i.e 2014, 2015, 2016, 2017, 2018 because current academic year is 2019 - 2020
            valid_year = datetime.datetime.now().year - 5
            if CGPAFrom <= cpga <= CPGATo and year <= valid_year and self._is_graduate(year):
                self.new_course_candidate_records[student_id] = cpga
        num_of_eligible_students = len(self.new_course_candidate_records)
        return self.formatter.format_new_course_candidates(num_of_eligible_students, self.new_course_candidate_records, CGPAFrom, CPGATo)
    
    def depAvg(self):
        """Filters out students department wise and calculates the max and avg cgpa and inserts in the dep_records hashtable"""
        for department in self.dep_records.keys():
            department_list = list(filter(lambda record: record[4:7] == department, self.student_records.keys()))
            department_list = list(map(lambda student_id: self.student_records[student_id], department_list))
            self.dep_records[department]['max'] = max(department_list)
            #NOTE: Rounding the average for one significant digit
            self.dep_records[department]['avg'] = round(sum(department_list) / len(department_list), 1)
        return self.formatter.format_department_cgpa(self.dep_records)

    def destroyHash(self):
        """Method to destroy the records in the all the created hashtables"""
        self.student_records.prune()
        self.dep_records.prune()
        self.hall_of_fame_records.prune()
        self.new_course_candidate_records.prune()

    def _is_graduate(self, year):
        """Private utility method to see whether based on the start year a particular student is graduated or not"""
        graduated_year = year + 4
        current_year = datetime.datetime.now().year
        return graduated_year <= current_year


if __name__ == '__main__':
    student_management = StudentManagement()
    student_management.initializeHash()

    # Parser class has file parsing logic and exception handling
    parser = Parser()
    input_student_records = parser.student_file_parser(INPUT_FILE_PATH, '/')
    min_cgpa, max_cgpa = parser.prompts_parser(INPUT_PROMPTS_FILE_PATH, ':')

    # Note:- Our assumption is that even if one entry in the input file is wrong in terms of value or format we don't evaluate the rest.
    if not min_cgpa or not max_cgpa or input_student_records == []:
        print("Some error occured while parsing the files or there might be format/range errors in the files")
        print("So, exiting ...")
        exit()

    # Lazy evaluation of map in python3.
    # https://stackoverflow.com/questions/19342331/python-map-calling-a-function-not-working
    s = list(map(lambda record: student_management.insertStudentRec(record[0], record[1]), input_student_records))
    
    # un comment them if you want to see the records
    # print(student_management.student_records.keys())
    # print(student_management.student_records.values())
    print(f"Got a total record of {len(student_management.student_records)} students")
    
    final_string = ""
    print("Calculating the hall of fame .....")
    final_string += student_management.hallOfFame(max_cgpa)

    print("Calculating new course candidates .....")
    final_string += student_management.newCourseList(min_cgpa, max_cgpa)

    print("Calculating the maximum and average for each department.....")
    final_string += student_management.depAvg()

    print("Outputting into the outputPS12.txt.....")
    parser.final_output_parser(OUTPUT_FILE_PATH, final_string)

    print("Pruning the student records.........")
    student_management.destroyHash()
