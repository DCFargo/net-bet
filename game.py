
class Game:
    # contains actual game handling and processing stats and stuff
    def __init__(self, ):
        print('lol')

class Player:
    category = ["winner", "mvp", "lvp", "final score", "lead changes", "times tied", "biggest lead"]
    def __init__(self, start_money):
        self.balance = start_money

    def calc_results(self):
        pass
    
def parse_anim_from_str(string):
    if string.lower().contains("jump shot"):
        return 0
    if string.lower().contains("layup"):
        return 1
    if string.lower().contains("dunk"):
        return 2
    if string.lower().contains("free throw"):
        return 3