import json
from data_formatters import decrypt_data



class Question:

    def __init__(self, directory: str, name: str, save_file_index: int, master) -> None:

        master.account.seek(save_file_index)
        temp = master.account.read(1)

        temp = decrypt_data(bytes(temp))

        if temp == ' ': self.completed = None
        if temp == '0': self.completed = False
        if temp == '1': self.completed = True; master.completed += 1

        print(f"save file index: {save_file_index}")
        print(f"temp: \"{temp}\"")
        print(f"self.completed: {self.completed}\n")

        self.directory = directory
        self.name = name
        self.save_file_index = save_file_index
        self.master = master

        self.extract_question_data()



    def extract_question_data(self):

        try:
            with open(f"{self.directory}\\data.json") as f:
                data = json.load(f)

        except:
            self.question_data = {}
            return

        for test_case in data['test cases']:
            
            test_case['input'] = tuple(test_case['input'])

        self.question_data = data



    def test_question(self, input):

        for index in range(len(self.question_data['test cases'])):

            self.question_data['test cases'][index]['output'] = input[index]

            self.question_data['test cases'][index]['correct'] = (self.question_data['test cases'][index]['output'] == self.question_data['test cases'][index]['answer'])

        print(f"test case output: {self.question_data['test cases']}")

        # evaluate whether or not the outputs were correct, and determine if the user passed the question (only pass if every test case is correct)
        # add the outputs to the question data dictionary, and also add a boolean that represents whether or not the answer was correct
        passed_question = True

        for test_case in self.question_data['test cases']:

            if not test_case['correct']:

                passed_question = False


        if passed_question:
            result = '\nYou passed the question.\n'
            if not self.completed:
                self.completed = True
                self.master.completed += 1

        else:
            result = '\nYou did not pass the question.\n'
            self.completed = False



        # update the test case display
        self.master.gui.update_test_display()

        self.master.update_save_file(self)

        print(result)
        return result