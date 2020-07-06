class Formatter:
    def __init__(self):
        super().__init__()

    def _set_back_format(self, students):
        stu_str = ""
        for student_id in students.keys():
            stu_str += f"{student_id} / {str(students[student_id])}\n\n"
        return stu_str

    def _set_back_dep_format(self, department_details):
        dep_str = ""
        for key in department_details.keys():
            dep_str += f"{key}: max: {department_details[key]['max']}, avg: {department_details[key]['avg']}\n\n"
        return dep_str

    def format_hall_of_fame(self, num_of_eligible_students, students):        
        formatter_string = (
            f"---------- hall of fame ----------\n\n"
            f"Total eligible students: {str(num_of_eligible_students)}\n\n"
            f"Qualified Students:\n\n"
            f"{self._set_back_format(students)}"
            f"-------------------------------------\n\n"
        )
        return formatter_string

    def format_new_course_candidates(self, number_of_eligible_students, students, min_cgpa, max_cpga):
        formatter_string = (
            f"---------- new course candidates ----------\n\n"
            f"Input: {str(min_cgpa)} to {str(max_cpga)}\n\n"
            f"Total eligible students: {str(number_of_eligible_students)}\n\n"
            f"Qualified Students:\n\n"
            f"{self._set_back_format(students)}"
            f"-------------------------------------\n\n"
        )
        return formatter_string

    def format_department_cgpa(self, department_details):
        formatter_string = (
            f"---------- department CGPA ----------\n\n"
            f"{self._set_back_dep_format(department_details)}"
            f"-------------------------------------\n\n"
        )
        return formatter_string

# USAGE
# f = Formatter()
# from hash_table import HashTable
# hall_records = HashTable()
# hall_records.set("2010CSE1223", 3.5)
# hall_records.set("2010ECE1203", 3.9)
# hall_records.set("2010CSE1225", 4.5)
# f.format_hall_of_fame(3, hall_records)
# f.format_new_course_candidates(3, hall_records, 3.5, 5.0)