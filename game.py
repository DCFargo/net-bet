
class Game:
    # contains actual game handling and processing stats and stuff
    def __init__(self, ):
        print('lol')

class Player:
    def __init__(self, start_money):
        self.start_money = start_money

    def bet(self, category, prediction):
        self.bet = [category, prediction]
    