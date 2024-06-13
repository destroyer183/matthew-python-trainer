from enum import Enum



class DifficultyLevel(Enum):
    Level0 = 0
    Level1 = 1
    Level2 = 2
    Level3 = 3



class DifficultyGroup:

    def __init__(self, directory: str, question_difficulty: DifficultyLevel, name: str, content: dict) -> None:

        self.directory = directory
        self.content = content
        self.question_difficulty = question_difficulty
        self.name = name
        self.unlocked = False
        self.completed = None
        self.completion_count = 0
        self.completion_total = len(content.values())



    def check_completion(self):

        completion_data = [x.completed for x in self.content.values()]

        if True not in completion_data and False not in completion_data:
            return

        self.completed = True

        temp = 0

        for item in self.content.values():

            if not item.completed:
                self.completed = False
                continue
            
            temp += 1

        self.completion_count = temp