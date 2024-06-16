from enum import Enum
from .difficulty_group import DifficultyGroup



# create enumeration for question types
class QuestionType(Enum):
    Basics = 'Basic'
    Functions = 'Functions'
    Dictionaries = 'Dictionaries'
    Lists = 'Lists'
    Loops = 'Loops'
    Math = 'Math'
    Strings = 'Strings'



# create class for question groups, and inherit from 'DifficultyGroup' so that the 'check_completion()' function can be used here
class QuestionGroup(DifficultyGroup):

    # create main constructor for class, for arguments, take in the directory, question type, name, and content
    def __init__(self, directory: str, question_type: QuestionType, name: str, content: dict) -> None:

        # assign class attributes
        self.directory = directory
        self.question_type = question_type
        self.name = name
        self.completed = None
        self.content = content
        self.completion_count = 0
        self.completion_total = len(content.values())