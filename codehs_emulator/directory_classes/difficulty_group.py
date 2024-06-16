from enum import Enum



# create enumeration for level difficulties
class DifficultyLevel(Enum):
    Level0 = 0
    Level1 = 1
    Level2 = 2
    Level3 = 3



# create class for difficulty groups
class DifficultyGroup:

    # create class constructor that takes in arguments for the directory path, the question difficulty, the name, and the content
    def __init__(self, directory: str, question_difficulty: DifficultyLevel, name: str, content: dict) -> None:

        # assigne class attributes
        self.directory = directory
        self.content = content
        self.question_difficulty = question_difficulty
        self.name = name
        self.unlocked = False
        self.completed = None
        self.completion_count = 0
        self.completion_total = len(content.values())



    # function to check if the content is completed or not
    def check_completion(self):

        # load the completion data of the object's contents
        completion_data = [x.completed for x in self.content.values()]

        # check if nothing has been completed or failed, meaning that they haven't even been attempted yet
        if True not in completion_data and False not in completion_data:

            # exit function if nothing has been attempted
            return

        # set completion to true
        self.completed = True

        # create temp counter
        temp = 0

        # loop over the values of the content
        for item in self.content.values():

            # check if item has not been completed
            if not item.completed:
                
                # set the completion to false and skip the rest of the loop
                self.completed = False
                continue
            
            # add to counter
            temp += 1

        # set the completion counter to the value of the counter
        self.completion_count = temp