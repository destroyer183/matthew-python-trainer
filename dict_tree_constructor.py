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

                "Basics-1-0": Question(f"{directory}\\Introduction\\Basics\\Basics-1-0.py", 'Basics-1-0', index + 0),
                "Basics-1-1": Question(f"{directory}\\Introduction\\Basics\\Basics-1-1.py", 'Basics-1-1', index + 1),
                "Basics-1-2": Question(f"{directory}\\Introduction\\Basics\\Basics-1-2.py", 'Basics-1-2', index + 2),
                "Basics-1-3": Question(f"{directory}\\Introduction\\Basics\\Basics-1-3.py", 'Basics-1-3', index + 3),
                "Basics-1-4": Question(f"{directory}\\Introduction\\Basics\\Basics-1-4.py", 'Basics-1-4', index + 4),
                "Basics-1-5": Question(f"{directory}\\Introduction\\Basics\\Basics-1-5.py", 'Basics-1-5', index + 5),
                "Basics-1-6": Question(f"{directory}\\Introduction\\Basics\\Basics-1-6.py", 'Basics-1-6', index + 6),
                "Basics-1-7": Question(f"{directory}\\Introduction\\Basics\\Basics-1-7.py", 'Basics-1-7', index + 7),
                "Basics-1-8": Question(f"{directory}\\Introduction\\Basics\\Basics-1-8.py", 'Basics-1-8', index + 8)
            }),

            "Functions": QuestionGroup(f"{directory}\\Introduction\\Functions", QuestionType.Functions, 'Functions', {

                "Functions-1-0": Question(f"{directory}\\Introduction\\Functions\\Functions-1-0.py", 'Functions-1-0', index + 9),
                "Functions-1-1": Question(f"{directory}\\Introduction\\Functions\\Functions-1-1.py", 'Functions-1-1', index + 10),
                "Functions-1-2": Question(f"{directory}\\Introduction\\Functions\\Functions-1-2.py", 'Functions-1-2', index + 11),
                "Functions-1-3": Question(f"{directory}\\Introduction\\Functions\\Functions-1-3.py", 'Functions-1-3', index + 12)
            })
        }),

        "Level-1": DifficultyGroup(f"{directory}\\Level-1", DifficultyLevel.Level1, 'Level-1', {

            "Dictionaries-1": QuestionGroup(f"{directory}\\Level-1\\Dictionaries-1", QuestionType.Dictionaries, 'Dictionaries-1', {

                "Dictionaries-1-0": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-0.py", 'Dictionaries-1-0', index + 13),
                "Dictionaries-1-1": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-1.py", 'Dictionaries-1-1', index + 14),
                "Dictionaries-1-2": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-2.py", 'Dictionaries-1-2', index + 15),
                "Dictionaries-1-3": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-3.py", 'Dictionaries-1-3', index + 16),
                "Dictionaries-1-4": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-4.py", 'Dictionaries-1-4', index + 17),
                "Dictionaries-1-5": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-5.py", 'Dictionaries-1-5', index + 18),
                "Dictionaries-1-6": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-6.py", 'Dictionaries-1-6', index + 19),
                "Dictionaries-1-7": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-7.py", 'Dictionaries-1-7', index + 20),
                "Dictionaries-1-8": Question(f"{directory}\\Level-1\\Dictionaries-1\\Dictionaries-1-8.py", 'Dictionaries-1-8', index + 21)
            }),

            "Lists-1": QuestionGroup(f"{directory}\\Level-1\\Lists-1", QuestionType.Lists, 'Lists-1', {

                "Lists-1-0": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-0.py", 'Lists-1-0', index + 22),
                "Lists-1-1": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-1.py", 'Lists-1-1', index + 23),
                "Lists-1-2": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-2.py", 'Lists-1-2', index + 24),
                "Lists-1-3": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-3.py", 'Lists-1-3', index + 25),
                "Lists-1-4": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-4.py", 'Lists-1-4', index + 26),
                "Lists-1-5": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-5.py", 'Lists-1-5', index + 27),
                "Lists-1-6": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-6.py", 'Lists-1-6', index + 28),
                "Lists-1-7": Question(f"{directory}\\Level-1\\Lists-1\\Lists-1-8.py", 'Lists-1-7', index + 29)
            }),

            "Loops-1": QuestionGroup(f"{directory}\\Level-1\\Loops-1", QuestionType.Loops, 'Loops-1', {

                "Loops-1-0": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-0.py", 'Loops-1-0', index + 30),
                "Loops-1-1": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-1.py", 'Loops-1-1', index + 31),
                "Loops-1-2": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-2.py", 'Loops-1-2', index + 32),
                "Loops-1-3": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-3.py", 'Loops-1-3', index + 33),
                "Loops-1-4": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-4.py", 'Loops-1-4', index + 34),
                "Loops-1-5": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-5.py", 'Loops-1-5', index + 35),
                "Loops-1-6": Question(f"{directory}\\Level-1\\Loops-1\\Loops-1-6.py", 'Loops-1-6', index + 36)
            }),

            "Math-1": QuestionGroup(f"{directory}\\Level-1\\Math-1", QuestionType.Math, 'Math-1', {

                "Math-1-0": Question(f"{directory}\\Level-1\\Math-1\\Math-1-0.py", 'Math-1-0', index + 37),
                "Math-1-1": Question(f"{directory}\\Level-1\\Math-1\\Math-1-1.py", 'Math-1-1', index + 38),
                "Math-1-2": Question(f"{directory}\\Level-1\\Math-1\\Math-1-2.py", 'Math-1-2', index + 39),
                "Math-1-3": Question(f"{directory}\\Level-1\\Math-1\\Math-1-3.py", 'Math-1-3', index + 40),
                "Math-1-4": Question(f"{directory}\\Level-1\\Math-1\\Math-1-4.py", 'Math-1-4', index + 41),
                "Math-1-5": Question(f"{directory}\\Level-1\\Math-1\\Math-1-5.py", 'Math-1-5', index + 42),
                "Math-1-6": Question(f"{directory}\\Level-1\\Math-1\\Math-1-6.py", 'Math-1-6', index + 43),
                "Math-1-7": Question(f"{directory}\\Level-1\\Math-1\\Math-1-7.py", 'Math-1-7', index + 44)
            }),

            "Strings-1": QuestionGroup(f"{directory}\\Level-1\\Strings-1", QuestionType.Strings, 'Strings-1', {

                "Strings-1-0": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-0.py", 'Strings-1-0', index + 45),
                "Strings-1-1": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-1.py", 'Strings-1-1', index + 46),
                "Strings-1-2": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-2.py", 'Strings-1-2', index + 47),
                "Strings-1-3": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-3.py", 'Strings-1-3', index + 48),
                "Strings-1-4": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-4.py", 'Strings-1-4', index + 49),
                "Strings-1-5": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-5.py", 'Strings-1-5', index + 50),
                "Strings-1-6": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-6.py", 'Strings-1-6', index + 51),
                "Strings-1-7": Question(f"{directory}\\Level-1\\Strings-1\\Strings-1-7.py", 'Strings-1-7', index + 52)
            })
        }),

        "Level-2": DifficultyGroup(f"{directory}\\Level-2", DifficultyLevel.Level2, 'Level-2', {

            "Dictionaries-2": QuestionGroup(f"{directory}\\Level-2\\Dictionaries-2", QuestionType.Dictionaries, 'Dictionaries-2', {

                "Dictionaries-2-0": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-0.py", 'Dictionaries-2-0', index + 53),
                "Dictionaries-2-1": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-1.py", 'Dictionaries-2-1', index + 54),
                "Dictionaries-2-2": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-2.py", 'Dictionaries-2-2', index + 55),
                "Dictionaries-2-3": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-3.py", 'Dictionaries-2-3', index + 56),
                "Dictionaries-2-4": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-4.py", 'Dictionaries-2-4', index + 57),
                "Dictionaries-2-5": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-5.py", 'Dictionaries-2-5', index + 58),
                "Dictionaries-2-6": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-6.py", 'Dictionaries-2-6', index + 59),
                "Dictionaries-2-7": Question(f"{directory}\\Level-2\\Dictionaries-2\\Dictionaries-2-7.py", 'Dictionaries-2-7', index + 60)
            }),

            "Lists-2": QuestionGroup(f"{directory}\\Level-2\\Lists-2", QuestionType.Lists, 'Lists-2', {

                "Lists-2-0": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-0.py", 'Lists-2-0', index + 61),
                "Lists-2-1": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-1.py", 'Lists-2-1', index + 62),
                "Lists-2-2": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-2.py", 'Lists-2-2', index + 63),
                "Lists-2-3": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-3.py", 'Lists-2-3', index + 64),
                "Lists-2-4": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-4.py", 'Lists-2-4', index + 65),
                "Lists-2-5": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-5.py", 'Lists-2-5', index + 66),
                "Lists-2-6": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-6.py", 'Lists-2-6', index + 67),
                "Lists-2-7": Question(f"{directory}\\Level-2\\Lists-2\\Lists-2-7.py", 'Lists-2-7', index + 68)

            }),

            "Loops-2": QuestionGroup(f"{directory}\\Level-2\\Loops-2", QuestionType.Loops, 'Loops-2', {

                "Loops-2-0": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-0.py", 'Loops-2-0', index + 69),
                "Loops-2-1": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-1.py", 'Loops-2-1', index + 70),
                "Loops-2-2": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-2.py", 'Loops-2-2', index + 71),
                "Loops-2-3": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-3.py", 'Loops-2-3', index + 72),
                "Loops-2-4": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-4.py", 'Loops-2-4', index + 73),
                "Loops-2-5": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-5.py", 'Loops-2-5', index + 74),
                "Loops-2-6": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-6.py", 'Loops-2-6', index + 75),
                "Loops-2-7": Question(f"{directory}\\Level-2\\Loops-2\\Loops-2-7.py", 'Loops-2-7', index + 76)

            }),

            "Math-2": QuestionGroup(f"{directory}\\Level-2\\Math-2", QuestionType.Math, 'Math-2', {

                "Math-2-0": Question(f"{directory}\\Level-2\\Math-2\\Math-2-0.py", 'Math-2-0', index + 77),
                "Math-2-1": Question(f"{directory}\\Level-2\\Math-2\\Math-2-1.py", 'Math-2-1', index + 78),
                "Math-2-2": Question(f"{directory}\\Level-2\\Math-2\\Math-2-2.py", 'Math-2-2', index + 79),
                "Math-2-3": Question(f"{directory}\\Level-2\\Math-2\\Math-2-3.py", 'Math-2-3', index + 80),
                "Math-2-4": Question(f"{directory}\\Level-2\\Math-2\\Math-2-4.py", 'Math-2-4', index + 81),
                "Math-2-5": Question(f"{directory}\\Level-2\\Math-2\\Math-2-5.py", 'Math-2-5', index + 82),
                "Math-2-6": Question(f"{directory}\\Level-2\\Math-2\\Math-2-6.py", 'Math-2-6', index + 83),
                "Math-2-7": Question(f"{directory}\\Level-2\\Math-2\\Math-2-7.py", 'Math-2-7', index + 84)

            }),

            "Strings-2": QuestionGroup(f"{directory}\\Level-2\\Strings-2", QuestionType.Strings, 'Strings-2', {

                "Strings-2-0": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-0.py", 'Strings-2-0', index + 85),
                "Strings-2-1": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-1.py", 'Strings-2-1', index + 86),
                "Strings-2-2": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-2.py", 'Strings-2-2', index + 87),
                "Strings-2-3": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-3.py", 'Strings-2-3', index + 88),
                "Strings-2-4": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-4.py", 'Strings-2-4', index + 89),
                "Strings-2-5": Question(f"{directory}\\Level-2\\Strings-2\\Strings-2-5.py", 'Strings-2-5', index + 90)

            })
        }),

        "Level-3": DifficultyGroup(f"{directory}\\Level-3", DifficultyLevel.Level3, 'Level-3', {

            "Lists-3": QuestionGroup(f"{directory}\\Level-3\\Lists-3", QuestionType.Lists, 'Lists-3', {

                "Lists-3-0": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-0.py", 'Lists-3-0', index + 91),
                "lists-3-1": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-1.py", 'Lists-3-1', index + 92),
                "lists-3-2": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-2.py", 'Lists-3-2', index + 93),
                "lists-3-3": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-3.py", 'Lists-3-3', index + 94),
                "lists-3-4": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-4.py", 'Lists-3-4', index + 95),
                "lists-3-5": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-5.py", 'Lists-3-5', index + 96),
                "lists-3-6": Question(f"{directory}\\Level-3\\Lists-3\\Lists-3-6.py", 'Lists-3-6', index + 97)
            }),

            "Strings-3": QuestionGroup(f"{directory}\\Level-3\\Strings-3", QuestionType.Strings, 'Strings-3', {

                "Strings-3-0": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-0.py", 'Strings-3-0', index + 98),
                "Strings-3-1": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-1.py", 'Strings-3-1', index + 99),
                "Strings-3-2": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-2.py", 'Strings-3-2', index + 100),
                "Strings-3-3": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-3.py", 'Strings-3-3', index + 101),
                "Strings-3-4": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-4.py", 'Strings-3-4', index + 102),
                "Strings-3-5": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-5.py", 'Strings-3-5', index + 103),
                "Strings-3-6": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-6.py", 'Strings-3-6', index + 104),
                "Strings-3-7": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-7.py", 'Strings-3-7', index + 105),
                "Strings-3-8": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-8.py", 'Strings-3-8', index + 106),
                "Strings-3-9": Question(f"{directory}\\Level-3\\Strings-3\\Strings-3-9.py", 'Strings-3-9', index + 107)
            })
        })
    }

    return directory_tree