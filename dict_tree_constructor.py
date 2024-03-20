import question_tester
from question_tester import DifficultyGroup, QuestionGroup, Question
from question_tester import DifficultyLevel, QuestionType


def construct_dict_tree(directory):

    directory = f"{directory}\\user_code"

    directory_tree = {

        "directory": directory,

        "Introduction": DifficultyGroup(f"{directory}\\Introduction", DifficultyLevel.Level0, 'Introduction', {

            "Basics": QuestionGroup(f"{directory}\\Introduction\\Basics", QuestionType.Basics, 'Basics', {

                "Basics-1-1": Question(f"{directory}\\Introduction\\Basics\\Basics-1-1.py", 'Basics-1-1'),
                "Basics-1-2": Question(f"{directory}\\Introduction\\Basics\\Basics-1-2.py", 'Basics-1-2'),
                "Basics-1-3": Question(f"{directory}\\Introduction\\Basics\\Basics-1-3.py", 'Basics-1-3'),
                "Basics-1-4": Question(f"{directory}\\Introduction\\Basics\\Basics-1-4.py", 'Basics-1-4'),
                "Basics-1-5": Question(f"{directory}\\Introduction\\Basics\\Basics-1-5.py", 'Basics-1-5'),
                "Basics-1-6": Question(f"{directory}\\Introduction\\Basics\\Basics-1-6.py", 'Basics-1-6'),
                "Basics-1-7": Question(f"{directory}\\Introduction\\Basics\\Basics-1-7.py", 'Basics-1-7'),
                "Basics-1-8": Question(f"{directory}\\Introduction\\Basics\\Basics-1-8.py", 'Basics-1-8'),
                "Basics-1-9": Question(f"{directory}\\Introduction\\Basics\\Basics-1-9.py", 'Basics-1-9')
            }),

            "Functions": QuestionGroup(f"{directory}\\Introduction\\Functions", QuestionType.Functions, 'Functions', {

                "Functions-1-1": Question(f"{directory}\\Introduction\\Functions\\Functions-1-1.py", 'Functions-1-1'),
                "Functions-1-2": Question(f"{directory}\\Introduction\\Functions\\Functions-1-2.py", 'Functions-1-2'),
                "Functions-1-3": Question(f"{directory}\\Introduction\\Functions\\Functions-1-3.py", 'Functions-1-3'),
                "Functions-1-4": Question(f"{directory}\\Introduction\\Functions\\Functions-1-4.py", 'Functions-1-4')
            })
        }),

        "Level-1": DifficultyGroup(f"{directory}\\Level-1", DifficultyLevel.Level1, 'Level-1', {

            "Dictionaries-1": QuestionGroup(f"{directory}\\Level-1\\Dictionaries-1", QuestionType.Dictionaries, 'Dictionaries-1', {

                "Dictionaries-1-1": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-1.py", 'Dictionaries-1-1'),
                "Dictionaries-1-2": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-2.py", 'Dictionaries-1-2'),
                "Dictionaries-1-3": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-3.py", 'Dictionaries-1-3'),
                "Dictionaries-1-4": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-4.py", 'Dictionaries-1-4'),
                "Dictionaries-1-5": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-5.py", 'Dictionaries-1-5'),
                "Dictionaries-1-6": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-6.py", 'Dictionaries-1-6'),
                "Dictionaries-1-7": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-7.py", 'Dictionaries-1-7'),
                "Dictionaries-1-8": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-8.py", 'Dictionaries-1-8'),
                "Dictionaries-1-9": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-9.py", 'Dictionaries-1-9')
            }),

            "Lists-1": QuestionGroup(f"{directory}\\Level-1\\Lists-1", QuestionType.Lists, 'Lists-1', {}),

            "Loops-1": QuestionGroup(f"{directory}\\Level-1\\Loops-1", QuestionType.Loops, 'Loops-1', {}),

            "Math-1": QuestionGroup(f"{directory}\\Level-1\\Math-1", QuestionType.Math, 'Math-1', {}),

            "Strings-1": QuestionGroup(f"{directory}\\Level-1\\Strings-1", QuestionType.Strings, 'Strings-1', {})
        }),

        "Level-2": DifficultyGroup(f"{directory}\\Level-2", DifficultyLevel.Level2, 'Level-2', {

            "Dictionaries-2": QuestionGroup(f"{directory}\\Level-2\\Dictionaries-2", QuestionType.Dictionaries, 'Dictionaries-2', {}),

            "Lists-2": QuestionGroup(f"{directory}\\Level-2\\Lists-2", QuestionType.Lists, 'Lists-2', {}),

            "Loops-2": QuestionGroup(f"{directory}\\Level-2\\Loops-2", QuestionType.Loops, 'Loops-2', {}),

            "Math-2": QuestionGroup(f"{directory}\\Level-2\\Math-2", QuestionType.Math, 'Math-2', {}),

            "Strings-2": QuestionGroup(f"{directory}\\Level-2\\Strings-2", QuestionType.Strings, 'Strings-2', {})
        }),

        "Level-3": DifficultyGroup(f"{directory}\\Level-3", DifficultyLevel.Level3, 'Level-3', {

            "Lists-3": QuestionGroup(f"{directory}\\Level-3\\Lists-3", QuestionType.Lists, 'Lists-3', {}),

            "Strings-3": QuestionGroup(f"{directory}\\Level-3\\Strings-3", QuestionType.Strings, 'Strings-3', {})
        })
        
    }

    return directory_tree