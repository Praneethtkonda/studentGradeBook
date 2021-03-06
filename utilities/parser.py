from utilities.errors import CgpaNotInRangeError, WrongInputFormat
class Parser():
    """ Utility class which has member functions that will be used for parsing inputPS12.txt and promptPS12.txt and has some exception handling. """
    def __init__(self):
        self.stu_format = 'YYYYGRPSTID / CGPA'
        self.prompt_format = 'courseOffer: min_cgpa : max_cgpa'

    def _student_string_parser(self, student_string, delimiter):
        """ Private method used to parse a student_id string and return the student_id and cgpa
            Throws error for the following reasons:-
              1.) Wrong student string format
              2.) Wrong cgpa range value
              3.) Floating point exception
        """
        stud_list = student_string.strip().split(delimiter)
        stud_details_list = []
        stud_id = stud_list[0].strip().replace(" ", "")
        dep = stud_id[4:7].replace(" ", "")
        year = stud_id[0:4].replace(" ", "")
        # Validating the format
        if len(stud_list) != 2 or len(stud_id) != 11 or len(dep) != 3 or year.isdecimal() == False or dep.isdecimal():
            raise WrongInputFormat(f"Wrong input student format as it is not in the format {self.stu_format} for {student_string}")
        stud_cgpa = float(stud_list[1].strip())
        if not 0.0 <= stud_cgpa <= 5.0:
            raise CgpaNotInRangeError(stud_cgpa)
        stud_details_list.extend([stud_id, stud_cgpa])
        return stud_details_list

    def student_file_parser(self, file_name, delimiter):
        """ Parses the inputPS12.txt and returns a list of students to be inserted.
            It has exception handling which does the needful according to the error raised
        """
        final_list = []
        try:
            file = open(file_name, "r")
            input_list = file.readlines()
            # final_list = list(map(lambda student_string: self._student_string_parser(student_string, delimiter), input_list))
            for student_string in input_list:
                if student_string.strip() == '':
                    continue
                val = self._student_string_parser(student_string, delimiter)
                final_list.append(val)
        except WrongInputFormat as e:
            print(f"ERROR: {e.args[0]} at file:- {file_name}")
            final_list = []
        except ValueError:
            print(f"ERROR: Could not parse the file {file_name} because of floating point conversion")
            final_list = []
        except CgpaNotInRangeError as e:
            print(f"CGPA {e.args[0]} not in range at file:- {file_name}")
            # Setting this will not insert any record
            final_list = []
        except IOError:
            print('Error while reading/opening into the file :- {file_name}')
            final_list = []
        finally:
            file.close()
            return final_list
    
    def prompts_parser(self, file_name, delimiter):
        """ Parses the promptsPS12.txt and returns a list of students to be inserted.
            It has exception handling which does the needful according to the error raised
        """
        output_tuple = (None, None)
        try:
            file = open(file_name, "r")
            file_data = file.readlines()
            if(len(file_data) != 2):
                raise WrongInputFormat("PromptsPS12.txt is not in the correct format i.e it doesnot have the hallOfFame label")
            cgpa_range_str = file_data[1]
            final = cgpa_range_str.split(delimiter, cgpa_range_str.count(delimiter))
            if final[0] != 'courseOffer' or len(final) != 3:
                raise WrongInputFormat(f"PromptsPS12.txt is not in the correct format i.e {self.prompt_format}")
            min_cgpa = float(final[1].strip())
            max_cgpa = float(final[2].strip())
            if not 0.0 < min_cgpa <= 5.0:
                raise CgpaNotInRangeError(min_cgpa)
            if not 0.0 < max_cgpa <= 5.0:
                raise CgpaNotInRangeError(max_cgpa)
            output_tuple = (min_cgpa, max_cgpa)
        except ValueError:
            print(f"ERROR: Could not parse the file {file_name} because of floating point conversion")
        except IOError:
            print('ERROR: Cannot find the file or read data')
        except WrongInputFormat as e:
            print(f'ERROR: {e.args[0]} at file:- {file_name}')
        except CgpaNotInRangeError as e:
            print(f'ERROR: CGPA {e.args[0]} not in range at file:- {file_name}')
        finally:
            file.close()
            return output_tuple

    def final_output_parser(self, file_name, output_string):
        """ Method to write the formatted strings into the outputPS12.txt file"""
        try:
            file = open(file_name, "w")
            file.write(output_string)
        except IOError:
            print("ERROR: Outputting into the file failed")
        finally:
            file.close()

# p = Parser()
# p.file_parser('./test.txt')
# print(list(map(lambda x: x.strip(), student_string.strip().split(delimiter))))
# stud_details_list.append(stud_list[0].strip())
# stud_details_list.append(float(stud_list[1].strip()))
#return list(map(lambda x: x.strip(), student_string.strip().split(delimiter))))