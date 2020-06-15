class Formatter:
    def __init__(self):
        super().__init__()
    
    def _set_back_format(self, student):
        return student[0] + '/' + str(student[1])

    def format_hall_of_fame(self, number_of_eligible_students, students):
        formatter_string = '---------- hall of fame ----------\n'
        formatter_string += 'Total eligible students' + number_of_eligible_students
        formatter_string += '\n Qualified Students:\n'
        #TODO: Use reduce
        return formatter_string