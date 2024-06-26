from directory_classes.difficulty_group import DifficultyGroup, DifficultyLevel
from directory_classes.question_group import QuestionGroup, QuestionType
from directory_classes.question import Question
from main_emulator import Emulator



'''
function to create the main dictionary tree of objects for the emulator
takes in 3 arguments:
the full directory path to the questions - string
the index of where the question data starts in the save file - integer
the main 'Emulator' class instance - 'Emulator' object
'''
def construct_dict_tree(directory: str, question_data_index: int, master: Emulator):

    # shorten variable name
    index = question_data_index

    # add to directory path
    directory = f"{directory}\\user_code"

    # create dict to represent directory tree
    directory_tree = {

        # each item in a dictionary will be an object of a class, which class it is part of depends on where it is located in the directory
        # the uppermost items will be 'DifficultyGroup' objects,
        # the content of 'DifficultyGroup' objects will be 'QuestionGroup' objects,
        # the content of 'QuestionGroup' objects will be 'Question' objects
        
        # for 'DifficultyGroup' objects, the data passed in is as follows:
        # the full directory path to the cooresponding folder - string
        # an enumeration value to provide information on exactly what content this folder holds - 'DifficultyLevel'
        # the name of the folder - string
        # the content in the folder, which is a dict containing more objects - dictionary
        "Introduction": DifficultyGroup(f"{directory}\\Introduction", DifficultyLevel.Level0, 'Introduction', {

            # for 'QuestionGroup objects, the data passed in is as follows:
            # the full directory path to the cooresponding folder - string
            # the enumeration value to provide information on exactly what type of question this folder holds - 'QuestionType' 
            # the name of the folder - string
            # the content in the folder, which is a dict containing more objects - dictionary
            "Basics": QuestionGroup(f"{directory}\\Introduction\\Basics", QuestionType.Basics, 'Basics', {

                # for 'Question' objects, the data passed in is as follows:
                # the full directory path to the cooresponding folder - string
                # the name of the folder - string
                # the index of where its cooresponding data is stored in the save file - integer
                # the instance of the 'Emulator' object it is connected to
                "Basics-1-0": Question(f"{directory}\\Introduction\\Basics\\Basics-1-0", 'Basics-1-0', index + 0, master),
                "Basics-1-1": Question(f"{directory}\\Introduction\\Basics\\Basics-1-1", 'Basics-1-1', index + 1, master),
                "Basics-1-2": Question(f"{directory}\\Introduction\\Basics\\Basics-1-2", 'Basics-1-2', index + 2, master),
                "Basics-1-3": Question(f"{directory}\\Introduction\\Basics\\Basics-1-3", 'Basics-1-3', index + 3, master),
                "Basics-1-4": Question(f"{directory}\\Introduction\\Basics\\Basics-1-4", 'Basics-1-4', index + 4, master),
                "Basics-1-5": Question(f"{directory}\\Introduction\\Basics\\Basics-1-5", 'Basics-1-5', index + 5, master),
                "Basics-1-6": Question(f"{directory}\\Introduction\\Basics\\Basics-1-6", 'Basics-1-6', index + 6, master),
                "Basics-1-7": Question(f"{directory}\\Introduction\\Basics\\Basics-1-7", 'Basics-1-7', index + 7, master),
                "Basics-1-8": Question(f"{directory}\\Introduction\\Basics\\Basics-1-8", 'Basics-1-8', index + 8, master)
            }),

            "Functions": QuestionGroup(f"{directory}\\Introduction\\Functions", QuestionType.Functions, 'Functions', {

                "Functions-1-0": Question(f"{directory}\\Introduction\\Functions\\Functions-1-0", 'Functions-1-0', index + 9, master),
                "Functions-1-1": Question(f"{directory}\\Introduction\\Functions\\Functions-1-1", 'Functions-1-1', index + 10, master),
                "Functions-1-2": Question(f"{directory}\\Introduction\\Functions\\Functions-1-2", 'Functions-1-2', index + 11, master),
                "Functions-1-3": Question(f"{directory}\\Introduction\\Functions\\Functions-1-3", 'Functions-1-3', index + 12, master)
            })
        }),

        "Level-1": DifficultyGroup(f"{directory}\\Level-1", DifficultyLevel.Level1, 'Level-1', {

            "Dictionaries-1": QuestionGroup(f"{directory}\\Level-1\\Dictionaries-1", QuestionType.Dictionaries, 'Dictionaries-1', {

                "Dictionaries-1-0": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-0", 'Dictionaries-1-0', index + 13, master),
                "Dictionaries-1-1": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-1", 'Dictionaries-1-1', index + 14, master),
                "Dictionaries-1-2": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-2", 'Dictionaries-1-2', index + 15, master),
                "Dictionaries-1-3": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-3", 'Dictionaries-1-3', index + 16, master),
                "Dictionaries-1-4": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-4", 'Dictionaries-1-4', index + 17, master),
                "Dictionaries-1-5": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-5", 'Dictionaries-1-5', index + 18, master),
                "Dictionaries-1-6": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-6", 'Dictionaries-1-6', index + 19, master),
                "Dictionaries-1-7": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-7", 'Dictionaries-1-7', index + 20, master),
                "Dictionaries-1-8": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-8", 'Dictionaries-1-8', index + 21, master)
            }),

            "Lists-1": QuestionGroup(f"{directory}\\Level-1\\Lists-1", QuestionType.Lists, 'Lists-1', {

                "Lists-1-0": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-0", 'Lists-1-0', index + 22, master),
                "Lists-1-1": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-1", 'Lists-1-1', index + 23, master),
                "Lists-1-2": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-2", 'Lists-1-2', index + 24, master),
                "Lists-1-3": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-3", 'Lists-1-3', index + 25, master),
                "Lists-1-4": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-4", 'Lists-1-4', index + 26, master),
                "Lists-1-5": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-5", 'Lists-1-5', index + 27, master),
                "Lists-1-6": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-6", 'Lists-1-6', index + 28, master),
                "Lists-1-7": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-8", 'Lists-1-7', index + 29, master)
            }),

            "Loops-1": QuestionGroup(f"{directory}\\Level-1\\Loops-1", QuestionType.Loops, 'Loops-1', {

                "Loops-1-0": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-0", 'Loops-1-0', index + 30, master),
                "Loops-1-1": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-1", 'Loops-1-1', index + 31, master),
                "Loops-1-2": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-2", 'Loops-1-2', index + 32, master),
                "Loops-1-3": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-3", 'Loops-1-3', index + 33, master),
                "Loops-1-4": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-4", 'Loops-1-4', index + 34, master),
                "Loops-1-5": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-5", 'Loops-1-5', index + 35, master),
                "Loops-1-6": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-6", 'Loops-1-6', index + 36, master)
            }),

            "Math-1": QuestionGroup(f"{directory}\\Level-1\\Math-1", QuestionType.Math, 'Math-1', {

                "Math-1-0": Question(f"{directory}\\Level-1\\Math-1\\Math-1-0", 'Math-1-0', index + 37, master),
                "Math-1-1": Question(f"{directory}\\Level-1\\Math-1\\Math-1-1", 'Math-1-1', index + 38, master),
                "Math-1-2": Question(f"{directory}\\Level-1\\Math-1\\Math-1-2", 'Math-1-2', index + 39, master),
                "Math-1-3": Question(f"{directory}\\Level-1\\Math-1\\Math-1-3", 'Math-1-3', index + 40, master),
                "Math-1-4": Question(f"{directory}\\Level-1\\Math-1\\Math-1-4", 'Math-1-4', index + 41, master),
                "Math-1-5": Question(f"{directory}\\Level-1\\Math-1\\Math-1-5", 'Math-1-5', index + 42, master),
                "Math-1-6": Question(f"{directory}\\Level-1\\Math-1\\Math-1-6", 'Math-1-6', index + 43, master),
                "Math-1-7": Question(f"{directory}\\Level-1\\Math-1\\Math-1-7", 'Math-1-7', index + 44, master)
            }),

            "Strings-1": QuestionGroup(f"{directory}\\Level-1\\Strings-1", QuestionType.Strings, 'Strings-1', {

                "Strings-1-0": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-0", 'Strings-1-0', index + 45, master),
                "Strings-1-1": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-1", 'Strings-1-1', index + 46, master),
                "Strings-1-2": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-2", 'Strings-1-2', index + 47, master),
                "Strings-1-3": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-3", 'Strings-1-3', index + 48, master),
                "Strings-1-4": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-4", 'Strings-1-4', index + 49, master),
                "Strings-1-5": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-5", 'Strings-1-5', index + 50, master),
                "Strings-1-6": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-6", 'Strings-1-6', index + 51, master),
                "Strings-1-7": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-7", 'Strings-1-7', index + 52, master)
            })
        }),

        "Level-2": DifficultyGroup(f"{directory}\\Level-2", DifficultyLevel.Level2, 'Level-2', {

            "Dictionaries-2": QuestionGroup(f"{directory}\\Level-2\\Dictionaries-2", QuestionType.Dictionaries, 'Dictionaries-2', {

                "Dictionaries-2-0": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-0", 'Dictionaries-2-0', index + 53, master),
                "Dictionaries-2-1": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-1", 'Dictionaries-2-1', index + 54, master),
                "Dictionaries-2-2": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-2", 'Dictionaries-2-2', index + 55, master),
                "Dictionaries-2-3": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-3", 'Dictionaries-2-3', index + 56, master),
                "Dictionaries-2-4": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-4", 'Dictionaries-2-4', index + 57, master),
                "Dictionaries-2-5": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-5", 'Dictionaries-2-5', index + 58, master),
                "Dictionaries-2-6": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-6", 'Dictionaries-2-6', index + 59, master),
                "Dictionaries-2-7": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-7", 'Dictionaries-2-7', index + 60, master)
            }),

            "Lists-2": QuestionGroup(f"{directory}\\Level-2\\Lists-2", QuestionType.Lists, 'Lists-2', {

                "Lists-2-0": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-0", 'Lists-2-0', index + 61, master),
                "Lists-2-1": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-1", 'Lists-2-1', index + 62, master),
                "Lists-2-2": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-2", 'Lists-2-2', index + 63, master),
                "Lists-2-3": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-3", 'Lists-2-3', index + 64, master),
                "Lists-2-4": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-4", 'Lists-2-4', index + 65, master),
                "Lists-2-5": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-5", 'Lists-2-5', index + 66, master),
                "Lists-2-6": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-6", 'Lists-2-6', index + 67, master),
                "Lists-2-7": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-7", 'Lists-2-7', index + 68, master)

            }),

            "Loops-2": QuestionGroup(f"{directory}\\Level-2\\Loops-2", QuestionType.Loops, 'Loops-2', {

                "Loops-2-0": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-0", 'Loops-2-0', index + 69, master),
                "Loops-2-1": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-1", 'Loops-2-1', index + 70, master),
                "Loops-2-2": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-2", 'Loops-2-2', index + 71, master),
                "Loops-2-3": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-3", 'Loops-2-3', index + 72, master),
                "Loops-2-4": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-4", 'Loops-2-4', index + 73, master),
                "Loops-2-5": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-5", 'Loops-2-5', index + 74, master),
                "Loops-2-6": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-6", 'Loops-2-6', index + 75, master),
                "Loops-2-7": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-7", 'Loops-2-7', index + 76, master)

            }),

            "Math-2": QuestionGroup(f"{directory}\\Level-2\\Math-2", QuestionType.Math, 'Math-2', {

                "Math-2-0": Question(f"{directory}\\Level-2\\Math-2\\Math-2-0", 'Math-2-0', index + 77, master),
                "Math-2-1": Question(f"{directory}\\Level-2\\Math-2\\Math-2-1", 'Math-2-1', index + 78, master),
                "Math-2-2": Question(f"{directory}\\Level-2\\Math-2\\Math-2-2", 'Math-2-2', index + 79, master),
                "Math-2-3": Question(f"{directory}\\Level-2\\Math-2\\Math-2-3", 'Math-2-3', index + 80, master),
                "Math-2-4": Question(f"{directory}\\Level-2\\Math-2\\Math-2-4", 'Math-2-4', index + 81, master),
                "Math-2-5": Question(f"{directory}\\Level-2\\Math-2\\Math-2-5", 'Math-2-5', index + 82, master),
                "Math-2-6": Question(f"{directory}\\Level-2\\Math-2\\Math-2-6", 'Math-2-6', index + 83, master),
                "Math-2-7": Question(f"{directory}\\Level-2\\Math-2\\Math-2-7", 'Math-2-7', index + 84, master)

            }),

            "Strings-2": QuestionGroup(f"{directory}\\Level-2\\Strings-2", QuestionType.Strings, 'Strings-2', {

                "Strings-2-0": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-0", 'Strings-2-0', index + 85, master),
                "Strings-2-1": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-1", 'Strings-2-1', index + 86, master),
                "Strings-2-2": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-2", 'Strings-2-2', index + 87, master),
                "Strings-2-3": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-3", 'Strings-2-3', index + 88, master),
                "Strings-2-4": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-4", 'Strings-2-4', index + 89, master),
                "Strings-2-5": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-5", 'Strings-2-5', index + 90, master)

            })
        }),

        "Level-3": DifficultyGroup(f"{directory}\\Level-3", DifficultyLevel.Level3, 'Level-3', {

            "Lists-3": QuestionGroup(f"{directory}\\Level-3\\Lists-3", QuestionType.Lists, 'Lists-3', {

                "Lists-3-0": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-0", 'Lists-3-0', index + 91, master),
                "lists-3-1": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-1", 'Lists-3-1', index + 92, master),
                "lists-3-2": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-2", 'Lists-3-2', index + 93, master),
                "lists-3-3": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-3", 'Lists-3-3', index + 94, master),
                "lists-3-4": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-4", 'Lists-3-4', index + 95, master),
                "lists-3-5": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-5", 'Lists-3-5', index + 96, master),
                "lists-3-6": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-6", 'Lists-3-6', index + 97, master)
            }),

            "Strings-3": QuestionGroup(f"{directory}\\Level-3\\Strings-3", QuestionType.Strings, 'Strings-3', {

                "Strings-3-0": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-0", 'Strings-3-0', index + 98, master),
                "Strings-3-1": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-1", 'Strings-3-1', index + 99, master),
                "Strings-3-2": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-2", 'Strings-3-2', index + 100, master),
                "Strings-3-3": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-3", 'Strings-3-3', index + 101, master),
                "Strings-3-4": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-4", 'Strings-3-4', index + 102, master),
                "Strings-3-5": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-5", 'Strings-3-5', index + 103, master),
                "Strings-3-6": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-6", 'Strings-3-6', index + 104, master),
                "Strings-3-7": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-7", 'Strings-3-7', index + 105, master),
                "Strings-3-8": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-8", 'Strings-3-8', index + 106, master),
                "Strings-3-9": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-9", 'Strings-3-9', index + 107, master)
            })
        })
    }

    # return the full dictionary tree
    return directory_tree