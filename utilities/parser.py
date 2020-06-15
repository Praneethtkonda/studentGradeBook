class Parser():
    def __init__(self):
        super().__init__()

    def _student_string_parser(self, student_string, delimiter):
        return list(map(lambda x: x.strip(), student_string.strip().split(delimiter)))

    def file_parser(self, file_name, delimiter):
        file = open(file_name, 'r')
        input_list = file.readlines()
        final_list = list(map(lambda student_string: self._student_string_parser(student_string, delimiter), input_list))
        return final_list
    
    def student_id_parser(self, student_id):
        return 0


# p = Parser()
# p.file_parser('./test.txt')
