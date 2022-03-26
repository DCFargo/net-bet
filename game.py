import math

class Game:
    # contains actual game handling and processing stats and stuff
    def __init__(self, plays, teams):
        pass

class Player:
    category = ["winner", "mvp", "lvp", "final score", "lead changes", "times tied", "biggest lead", 'done betting', 'quit']
    def __init__(self, start_money):
        self.balance = start_money
        Bet = tuple[int, int|tuple[int, int], float]
        self.bets: list[Bet] = []

    def calc_results(self, winner: int, win_loss_ratio: float, mvp: int, lvp: int, final_score: list[int], lead_changes: int, times_tied: int, biggest_lead: int):
        # results are list of [category, win, money won/lost]
        self.results: list[tuple[int, bool, float]] = []
        for bet in self.bets:
            match bet[0]:
                case 0:
                    if bet[1] == winner:
                        if winner == 0: # 0th / 1st = win_loss_ratio
                            self.results.append((0, True, float(math.floor(bet[2]*100 + (bet[2]/win_loss_ratio)*100))/100))
                        else:
                            self.results.append((0, True, float(math.floor(bet[2]*100 + (bet[2]*win_loss_ratio)*100))/100))
                    else:
                        self.results.append((0, False, 0))
                case 1:
                    if bet[1] == mvp:
                        self.results.append((1, True, bet[2]*3))
                    else:
                        self.results.append((1, False, 0))
                case 2:
                    if bet[1] == lvp:
                        self.results.append((2, True, bet[2]*3))
                    else:
                        self.results.append((2, False, 0))
                case 3:     # final score is [winner, loser]
                    if final_score[0] > final_score[1]:
                        winner_score = final_score[0]
                        loser_score = final_score[1]
                    else:
                        winner_score = final_score[1]
                        loser_score = final_score[0]
                    money_bet_winning = bet[2] / 2
                    money_bet_losing = bet[2] / 2
                    pe_winning = percent_error(winner_score, bet[2][0])
                    pe_losing = percent_error(loser_score, bet[2][1])
                   
                    # Logistic growth model ( 100 - pe ) -> multiplier
                    # f(0) = 0.25
                    # CC = 25
                    
                    multiplier = 25 / (1 + math.e ** ((pe_winning * (1 / 12)) - 4))

                    
                    self.results.append((3, True, bet[2] * multiplier))
                    
                case 4:
                    if bet[1] == lead_changes:
                        self.results.append((4, True, bet[2]*2))
                    else:
                        self.results.append((4, False, 0))
                case 5:
                    if bet[1] == times_tied:
                        self.results.append((5, True, bet[2]*2))
                    else:
                        self.results.append((5, False, 0))
                case 6:
                    if bet[1] == biggest_lead:
                        self.results.append((6, True, bet[2]*2))
                    else:
                        self.results.append((6, False, 0))
                        
    def update_balance(self):
        for result in self.results:
            if result[1]:
                self.balance += result[2]
            else:
                self.balance -= result[2]

    
def parse_anim_from_str(string):
    if string.lower().contains("jump shot"):
        return 1
    if string.lower().contains("layup"):
        return 2
    if string.lower().contains("dunk"):
        return 0
    if string.lower().contains("free throw"):
        return 3
    
def percent_error(actual, predicted):
    return (abs(float(predicted) - float(actual))) / float(actual) * 100.0





                                                                                
dunk = '''
              ███████████████████████████████▀º` ___
              ██                             ,████████▄
              ██                            ████████████▄
              ██                           ▐████████████████▄▄_
              ██       ╒▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄µ ▐█████████████   `7▀█▄
              ██       ▐█               █▌  ▀███████████∩      ▐█
              ██       ▐█               █▌   ^▀███████▀         █▌
              ██       ▐█               █▌        .             █▌
              ██       ▐█               █▌      ██░  _▄▄▄▄_    ▐█
              ██       ▐█               █▌      ██░ ▄██████▌   █▌
              ██       ▐█               █▌      ██░ ████████  ██
              ████████████████████████████████████░  ▀████▀  ▐█
                    ▐██▀▀▀███▀▀███▀▀███▀▀▓██∩            ▄█▌▄█
                     ██▌  ▐█▌  ▐█▌  ██▌  ██▌              ███∩
                     ▐██  ███  ▐██  ██▄ ▐██                ██_
                      ██▌(█▓█░ ███µ ███ ██▌                "██
                      ▐████ ██▐█ ████ ████                  ▐██
                       ███∩ j██▌ j██▌ ███▌                   ▐██
                       j█████████████████                     ███▄▄
                                                             ▐█▌`▀▀███▄_
                                                            ▐██      `▀▀
                                                           ╒██
'''

jumpshot = '''
                                              _▄▄▄▄_
         ___________________________       .██████████
        ▐█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀██      ▄████████████▄
        ▐█                        ██      ██████████████
        ▐█                        ██      ██████████████          ▄██████▄
        ▐█     j█▀▀▀▀▀▀▀▀▀▀▀█     ██      ª████████████    ╓█▌  (██████████
        ▐█     j▌           █     ██        ▀███████▀∩      "██_▐██████████
        ▐█     j▌           █     ██                          ██▄▀████████`
        ▐█     j▌           █     ██                           ▀█████▀▀`
        ▐█     j▌           █     ██                            º████
        ▐███████████████████████████                              ███
             "█▌  █▌ ▐█▌ ██  ██                                   ▐██
              ██ (██ ▐█▌ ██ ▐█∩                                   ▐██
               ███▌█ █▀█(██▄█▌                                    ▐██
               ▐██_▐██_██▌_██                                     ▐████▄
                ▀▀▀▀▀▀▀▀▀▀▀▀▀                                     ▐██.▀██▄_
                                                                  ▐██   "███
                                                                  ▐██
                                                                  ▐██
'''

freethrow = '''
                                   __
                            ▄▄▀▀▀▀777`º▀▀▀▀▄▄_
                        ▄█▀'                 `▀▀▄▄
      █▌          ▄▄▄,█▀                         `▀█▄
      █▌         █████                               ▀█▄
      █▌         ▀████                                  ▀█_
      █▌           `.                                     "█▄
      ██████████▌                                           ^█▄
      ██▌     (█                                              º█_
      ███     ██                                                        __
      █▓█     █∩                                                  "█▄  ████µ
      █▌▀▀▀▀▀▀▀                                                     ▀█_████∩
      █▌                                                              ▀██∩`
      █▌                                                               (█
      █▌                                                               j█
      █▌                                                               j█
      █▌                                                               j█
      █▌                                                               j█
      █▌                                                                ▀ 
'''

layup = '''
            ▐███████████████████████████
            ▐█                        ██
            ▐█                        ██
            ▐█      █▄▄▄▄▄▄▄▄▄▄▄█     ██
            ▐█     j▌           █     █▀ ,▄▄▄
            ▐█     j▌           █      ████████_
            ▐█     j▌           █     ██████████
            ▐█     j▌           █     ██████████
            ▐████████████████████████▄ ████████`
                 ▐█▌ º█▌ ▐█▌ ██⌐_██      █▌▀
                  ██  █▌ (█░ ██ ▐█▌     (█  ▄█████▄
                  "█▌█▌█ █▓█ ██_██      (█ ▐███████
                   ███ ▐██ ██▌▐██∩       █▌▐███████
                    ████████████▌         █▄ ██▀▀
                                           ▀███
                                             ▀█▌
                                              ██
                                              ▐█
                                              ███▄
                                            ▄█▀  `▀█▄
'''