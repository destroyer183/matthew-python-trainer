import question_tester
from question_tester import DifficultyGroup, QuestionGroup, Question
from question_tester import DifficultyLevel, QuestionType


def construct_dict_tree(directory, question_data_index, completion_list: list):

    index = question_data_index

    directory = f"{directory}\\user_code"

    directory_tree = {

        "directory": directory,

        "Introduction": DifficultyGroup(f"{directory}\\Introduction", DifficultyLevel.Level0, 'Introduction', {

            "Basics": QuestionGroup(f"{directory}\\Introduction\\Basics", QuestionType.Basics, 'Basics', {

                "Basics-1-0": Question(f"{directory}\\Introduction\\Basics\\Basics-1-0.py", 'Basics-1-0'),
                "Basics-1-1": Question(f"{directory}\\Introduction\\Basics\\Basics-1-1.py", 'Basics-1-1'),
                "Basics-1-2": Question(f"{directory}\\Introduction\\Basics\\Basics-1-2.py", 'Basics-1-2'),
                "Basics-1-3": Question(f"{directory}\\Introduction\\Basics\\Basics-1-3.py", 'Basics-1-3'),
                "Basics-1-4": Question(f"{directory}\\Introduction\\Basics\\Basics-1-4.py", 'Basics-1-4'),
                "Basics-1-5": Question(f"{directory}\\Introduction\\Basics\\Basics-1-5.py", 'Basics-1-5'),
                "Basics-1-6": Question(f"{directory}\\Introduction\\Basics\\Basics-1-6.py", 'Basics-1-6'),
                "Basics-1-7": Question(f"{directory}\\Introduction\\Basics\\Basics-1-7.py", 'Basics-1-7'),
                "Basics-1-8": Question(f"{directory}\\Introduction\\Basics\\Basics-1-8.py", 'Basics-1-8')
            }),

            "Functions": QuestionGroup(f"{directory}\\Introduction\\Functions", QuestionType.Functions, 'Functions', {

                "Functions-1-0": Question(f"{directory}\\Introduction\\Functions\\Functions-1-0.py", 'Functions-1-0'),
                "Functions-1-1": Question(f"{directory}\\Introduction\\Functions\\Functions-1-1.py", 'Functions-1-1'),
                "Functions-1-2": Question(f"{directory}\\Introduction\\Functions\\Functions-1-2.py", 'Functions-1-2'),
                "Functions-1-3": Question(f"{directory}\\Introduction\\Functions\\Functions-1-3.py", 'Functions-1-3')
            })
        }),

        "Level-1": DifficultyGroup(f"{directory}\\Level-1", DifficultyLevel.Level1, 'Level-1', {

            "Dictionaries-1": QuestionGroup(f"{directory}\\Level-1\\Dictionaries-1", QuestionType.Dictionaries, 'Dictionaries-1', {

                "Dictionaries-1-0": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-0.py", 'Dictionaries-1-0'),
                "Dictionaries-1-1": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-1.py", 'Dictionaries-1-1'),
                "Dictionaries-1-2": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-2.py", 'Dictionaries-1-2'),
                "Dictionaries-1-3": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-3.py", 'Dictionaries-1-3'),
                "Dictionaries-1-4": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-4.py", 'Dictionaries-1-4'),
                "Dictionaries-1-5": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-5.py", 'Dictionaries-1-5'),
                "Dictionaries-1-6": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-6.py", 'Dictionaries-1-6'),
                "Dictionaries-1-7": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-7.py", 'Dictionaries-1-7'),
                "Dictionaries-1-8": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-8.py", 'Dictionaries-1-8')
            }),

            "Lists-1": QuestionGroup(f"{directory}\\Level-1\\Lists-1", QuestionType.Lists, 'Lists-1', {

                "Lists-1-0": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-0.py", 'Lists-1-0'),
                "Lists-1-1": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-1.py", 'Lists-1-1'),
                "Lists-1-2": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-2.py", 'Lists-1-2'),
                "Lists-1-3": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-3.py", 'Lists-1-3'),
                "Lists-1-4": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-4.py", 'Lists-1-4'),
                "Lists-1-5": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-5.py", 'Lists-1-5'),
                "Lists-1-6": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-6.py", 'Lists-1-6'),
                "Lists-1-7": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-8.py", 'Lists-1-7')
            }),

            "Loops-1": QuestionGroup(f"{directory}\\Level-1\\Loops-1", QuestionType.Loops, 'Loops-1', {

                "Loops-1-0": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-0.py", 'Loops-1-0'),
                "Loops-1-1": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-1.py", 'Loops-1-1'),
                "Loops-1-2": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-2.py", 'Loops-1-2'),
                "Loops-1-3": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-3.py", 'Loops-1-3'),
                "Loops-1-4": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-4.py", 'Loops-1-4'),
                "Loops-1-5": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-5.py", 'Loops-1-5'),
                "Loops-1-6": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-6.py", 'Loops-1-6')
            }),

            "Math-1": QuestionGroup(f"{directory}\\Level-1\\Math-1", QuestionType.Math, 'Math-1', {

                "Math-1-0": Question(f"{directory}\\Level-1\\Math-1\\Math-1-0.py", 'Math-1-0'),
                "Math-1-1": Question(f"{directory}\\Level-1\\Math-1\\Math-1-1.py", 'Math-1-1'),
                "Math-1-2": Question(f"{directory}\\Level-1\\Math-1\\Math-1-2.py", 'Math-1-2'),
                "Math-1-3": Question(f"{directory}\\Level-1\\Math-1\\Math-1-3.py", 'Math-1-3'),
                "Math-1-4": Question(f"{directory}\\Level-1\\Math-1\\Math-1-4.py", 'Math-1-4'),
                "Math-1-5": Question(f"{directory}\\Level-1\\Math-1\\Math-1-5.py", 'Math-1-5'),
                "Math-1-6": Question(f"{directory}\\Level-1\\Math-1\\Math-1-6.py", 'Math-1-6'),
                "Math-1-7": Question(f"{directory}\\Level-1\\Math-1\\Math-1-7.py", 'Math-1-7')
            }),

            "Strings-1": QuestionGroup(f"{directory}\\Level-1\\Strings-1", QuestionType.Strings, 'Strings-1', {

                "Strings-1-0": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-0.py", 'Strings-1-0'),
                "Strings-1-1": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-1.py", 'Strings-1-1'),
                "Strings-1-2": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-2.py", 'Strings-1-2'),
                "Strings-1-3": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-3.py", 'Strings-1-3'),
                "Strings-1-4": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-4.py", 'Strings-1-4'),
                "Strings-1-5": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-5.py", 'Strings-1-5'),
                "Strings-1-6": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-6.py", 'Strings-1-6'),
                "Strings-1-7": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-7.py", 'Strings-1-7')
            })
        }),

        "Level-2": DifficultyGroup(f"{directory}\\Level-2", DifficultyLevel.Level2, 'Level-2', {

            "Dictionaries-2": QuestionGroup(f"{directory}\\Level-2\\Dictionaries-2", QuestionType.Dictionaries, 'Dictionaries-2', {

                "Dictionaries-2-0": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-0.py", 'Dictionaries-2-0'),
                "Dictionaries-2-1": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-1.py", 'Dictionaries-2-1'),
                "Dictionaries-2-2": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-2.py", 'Dictionaries-2-2'),
                "Dictionaries-2-3": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-3.py", 'Dictionaries-2-3'),
                "Dictionaries-2-4": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-4.py", 'Dictionaries-2-4'),
                "Dictionaries-2-5": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-5.py", 'Dictionaries-2-5'),
                "Dictionaries-2-6": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-6.py", 'Dictionaries-2-6'),
                "Dictionaries-2-7": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-7.py", 'Dictionaries-2-7')
            }),

            "Lists-2": QuestionGroup(f"{directory}\\Level-2\\Lists-2", QuestionType.Lists, 'Lists-2', {

                "Lists-2-0": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-0.py", 'Lists-2-0'),
                "Lists-2-1": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-1.py", 'Lists-2-1'),
                "Lists-2-2": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-2.py", 'Lists-2-2'),
                "Lists-2-3": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-3.py", 'Lists-2-3'),
                "Lists-2-4": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-4.py", 'Lists-2-4'),
                "Lists-2-5": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-5.py", 'Lists-2-5'),
                "Lists-2-6": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-6.py", 'Lists-2-6'),
                "Lists-2-7": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-7.py", 'Lists-2-7')

            }),

            "Loops-2": QuestionGroup(f"{directory}\\Level-2\\Loops-2", QuestionType.Loops, 'Loops-2', {

                "Loops-2-0": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-0.py", 'Loops-2-0'),
                "Loops-2-1": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-1.py", 'Loops-2-1'),
                "Loops-2-2": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-2.py", 'Loops-2-2'),
                "Loops-2-3": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-3.py", 'Loops-2-3'),
                "Loops-2-4": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-4.py", 'Loops-2-4'),
                "Loops-2-5": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-5.py", 'Loops-2-5'),
                "Loops-2-6": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-6.py", 'Loops-2-6'),
                "Loops-2-7": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-7.py", 'Loops-2-7')

            }),

            "Math-2": QuestionGroup(f"{directory}\\Level-2\\Math-2", QuestionType.Math, 'Math-2', {

                "Math-2-0": Question(f"{directory}\\Level-2\\Math-2\\Math-2-0.py", 'Math-2-0'),
                "Math-2-1": Question(f"{directory}\\Level-2\\Math-2\\Math-2-1.py", 'Math-2-1'),
                "Math-2-2": Question(f"{directory}\\Level-2\\Math-2\\Math-2-2.py", 'Math-2-2'),
                "Math-2-3": Question(f"{directory}\\Level-2\\Math-2\\Math-2-3.py", 'Math-2-3'),
                "Math-2-4": Question(f"{directory}\\Level-2\\Math-2\\Math-2-4.py", 'Math-2-4'),
                "Math-2-5": Question(f"{directory}\\Level-2\\Math-2\\Math-2-5.py", 'Math-2-5'),
                "Math-2-6": Question(f"{directory}\\Level-2\\Math-2\\Math-2-6.py", 'Math-2-6'),
                "Math-2-7": Question(f"{directory}\\Level-2\\Math-2\\Math-2-7.py", 'Math-2-7')

            }),

            "Strings-2": QuestionGroup(f"{directory}\\Level-2\\Strings-2", QuestionType.Strings, 'Strings-2', {

                "Strings-2-0": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-0.py", 'Strings-2-0'),
                "Strings-2-1": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-1.py", 'Strings-2-1'),
                "Strings-2-2": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-2.py", 'Strings-2-2'),
                "Strings-2-3": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-3.py", 'Strings-2-3'),
                "Strings-2-4": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-4.py", 'Strings-2-4'),
                "Strings-2-5": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-5.py", 'Strings-2-5')

            })
        }),

        "Level-3": DifficultyGroup(f"{directory}\\Level-3", DifficultyLevel.Level3, 'Level-3', {

            "Lists-3": QuestionGroup(f"{directory}\\Level-3\\Lists-3", QuestionType.Lists, 'Lists-3', {

                "Lists-3-0": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-0.py", 'Lists-3-0'),
                "lists-3-1": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-1.py", 'Lists-3-1'),
                "lists-3-2": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-2.py", 'Lists-3-2'),
                "lists-3-3": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-3.py", 'Lists-3-3'),
                "lists-3-4": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-4.py", 'Lists-3-4'),
                "lists-3-5": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-5.py", 'Lists-3-5'),
                "lists-3-6": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-6.py", 'Lists-3-6')
            }),

            "Strings-3": QuestionGroup(f"{directory}\\Level-3\\Strings-3", QuestionType.Strings, 'Strings-3', {

                "Strings-3-0": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-0.py", 'Strings-3-0'),
                "Strings-3-1": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-1.py", 'Strings-3-1'),
                "Strings-3-2": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-2.py", 'Strings-3-2'),
                "Strings-3-3": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-3.py", 'Strings-3-3'),
                "Strings-3-4": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-4.py", 'Strings-3-4'),
                "Strings-3-5": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-5.py", 'Strings-3-5'),
                "Strings-3-6": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-6.py", 'Strings-3-6'),
                "Strings-3-7": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-7.py", 'Strings-3-7'),
                "Strings-3-8": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-8.py", 'Strings-3-8'),
                "Strings-3-9": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-9.py", 'Strings-3-9')
            })
        })
    }

    return directory_tree