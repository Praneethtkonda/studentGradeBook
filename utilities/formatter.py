class Formatter:
    """Utility class which has member functions that will return formatted strings which will be used for writing into the outputPS12.txt"""
    def __init__(self):
        super().__init__()

    def _set_back_format(self, students):
        """Private utility methods which takes MyHashTable of records and gives it back in the input student format"""
        stu_str = ""
        for student_id in students.keys():
            stu_str += f"{student_id} / {str(students[student_id])}\n"
        return stu_str

    def _set_back_dep_format(self, department_details):
        """Private utility methods which takes MyHashTable of department records and returns a formatted string"""
        dep_str = ""
        for key in department_details.keys():
            dep_str += f"{key}: max: {department_details[key]['max']}, avg: {department_details[key]['avg']}\n"
        return dep_str

    def format_hall_of_fame(self, num_of_eligible_students, students):
        """Returns a formatted string for the hall_of_fame eligible students"""
        formatter_string = (
            f"---------- hall of fame ----------\n"
            f"Total eligible students: {str(num_of_eligible_students)}\n"
            f"Qualified Students:\n"
            f"{self._set_back_format(students)}"
            f"-------------------------------------\n"
        )
        return formatter_string

    def format_new_course_candidates(self, number_of_eligible_students, students, min_cgpa, max_cpga):
        """Returns a formatted string for the new_course_candidates"""
        formatter_string = (
            f"---------- new course candidates ----------\n"
            f"Input: {str(min_cgpa)} to {str(max_cpga)}\n"
            f"Total eligible students: {str(number_of_eligible_students)}\n"
            f"Qualified Students:\n"
            f"{self._set_back_format(students)}"
            f"-------------------------------------\n"
        )
        return formatter_string

    def format_department_cgpa(self, department_details):
        """Returns a formatted string for the departmemt wise cgpa details"""
        formatter_string = (
            f"---------- department CGPA ----------\n"
            f"{self._set_back_dep_format(department_details)}"
            f"-------------------------------------\n"
        )
        return formatter_string

# USAGE
# f = Formatter()
# from hash_table import MyHashTable
# hall_records = MyHashTable()
# hall_records.set("2010CSE1223", 3.5)
# hall_records.set("2010ECE1203", 3.9)
# hall_records.set("2010CSE1225", 4.5)
# f.format_hall_of_fame(3, hall_records)
# f.format_new_course_candidates(3, hall_records, 3.5, 5.0)