import json
from data_formatters import decrypt_data



# create class for questions
class Question:

    # create constructor for class, for arguments, take in the directory, the name, the save file index, and the master instance
    def __init__(self, directory: str, name: str, save_file_index: int, master) -> None:

        # read the data stored at the location in the save file where the data for this question is stored
        master.account.seek(save_file_index)
        temp = master.account.read(1)

        # decrypt the data
        temp = decrypt_data(bytes(temp))

        # set the value of the completion value depending on the value of the saved data
        if temp == ' ': self.completed = None
        if temp == '0': self.completed = False
        if temp == '1': self.completed = True; master.completed += 1 # add to global completion counter if quetsion is completed

        # print out data
        print(f"save file index: {save_file_index}")
        print(f"temp: \"{temp}\"")
        print(f"self.completed: {self.completed}\n")

        # assign object attributes
        self.directory = directory
        self.name = name
        self.save_file_index = save_file_index
        self.master = master

        # call function to extract the question data
        self.extract_question_data()



    # function to extract question data
    def extract_question_data(self):

        # try/except block so that errors don't occur if no question data has been found, since most questions haven't been created
        try:

            # load the question data from a json file with the json module
            with open(f"{self.directory}\\data.json") as f:
                data = json.load(f)

        # set the question data to an empty dicttionary if no json file is found, then return to skip the rest of the function
        except:
            self.question_data = {}
            return

        # convert the input lists in the test cases to tuples so that they aren't accidentally accessed
        for test_case in data['test cases']:
            
            test_case['input'] = tuple(test_case['input'])

        # assign 'question_data' attribute
        self.question_data = data



    # function to test a question that takes in arguments for:
    # the list of outputs from a question
    # the name of the question folder
    def test_question(self, input: str, question_folder: str):

        # loop over the question test cases by index
        for index in range(len(self.question_data['test cases'])):

            # set the output value of the test case
            self.question_data['test cases'][index]['output'] = input[index]

            # set the bool value of whether or not the test case was solved correctly
            self.question_data['test cases'][index]['correct'] = (self.question_data['test cases'][index]['output'] == self.question_data['test cases'][index]['answer'])

        # print out data
        print(f"test case output: {self.question_data['test cases']}")

        # evaluate whether or not the outputs were correct, and determine if the user passed the question (only pass if every test case is correct)
        # add the outputs to the question data dictionary, and also add a boolean that represents whether or not the answer was correct

        # create variable to represent whether or not the user passed the question
        passed_question = True

        # loop over every test case
        for test_case in self.question_data['test cases']:

            # check if the question was not solved correctly
            if not test_case['correct']:

                # set variable to false
                passed_question = False



        # check if the user passed the question or not 
        if passed_question:

            # set variable for result
            result = '\nYou passed the question.\n'

            # only update completion data if the question was not previously completed
            if not self.completed:
                self.completed = True
                self.master.completed += 1

        else:

            # set variable for result
            result = '\nYou did not pass the question.\n'

            # update class attribute to show that the question was not completed only if it has not been previously completed successfully
            if not self.completed:
                self.completed = False



        # update the test case display
        self.master.gui.update_test_display(question_folder)

        # update save file
        self.master.update_save_file(self)

        # print out result and return it
        print(result)
        return result