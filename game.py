import math
import curses #witches
import curses_usage
import time

class Game:
    # contains actual game handling and processing stats and stuff
    def __init__(self, plays, teams):
        self.stdscr = curses.initscr()
        self.is_skip = False
        if curses.COLS < 80 or curses.LINES < 24:
            self.__del__()
            raise Exception("Terminal window must be at least 80x24.")
        self.animwin = curses.newwin(24, 80, 0, 0)
        self.infowin = curses.newwin(5, 80, 19, 0)
        curses.noecho()
        curses.cbreak()
        
        for i in range(0, len(plays), 3):
            curses_usage.update_anim_window(self.animwin, parse_anim_from_str(plays[i + 1]), teams, plays[i])
            curses_usage.update_play_window(self.infowin, plays[i], plays[i + 1], "Play " + str(i/3 + 1) + "/" + str(len(plays)/3))
            self.stdscr.refresh()
            self.stdscr.getch()
            
        #no you have so much to live for
        self.__del__()
         
    def __del__(self):
        self.stdscr.clear()
        curses.nocbreak()
        
        #there is no keypad
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

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
                    pe_winning = percent_error(winner_score, bet[2][0])
                    pe_losing = percent_error(loser_score, bet[2][1])
                    
                    # Logistic growth model ( 100 - pe ) -> multiplier
                    # f(0) = 0.25
                    # CC = 25
                    
                    win_multiplier = 25 / (1 + math.e ** ((pe_winning * (1 / 12)) - 4))
                    loss_multiplier = 25 / (1 + math.e ** ((pe_losing * (1 / 12)) - 4))
                    
                    self.results.append((3, True, bet[2] * win_multiplier / 2 + bet[2] * loss_multiplier / 2))
                    
                case 4:
                    pe = percent_error(lead_changes, bet[2])
                    multiplier = 25 / (1 + math.e ** ((pe * (1 / 12)) - 4))
                    self.results.append((4, True, bet[2] * multiplier))
                case 5:
                    pe = percent_error(lead_changes, bet[2])
                    multiplier = 25 / (1 + math.e ** ((pe * (1 / 12)) - 4))
                    self.results.append((4, True, bet[2] * multiplier))
                case 6:
                    if bet[1] == biggest_lead:
                        self.results.append((6, True, bet[2]*2))
                    else:
                        self.results.append((6, False, 0))
                        
    def update_balance(self):
        for result in self.results:
                self.balance += result[2]

    
def parse_anim_from_str(string):
    if "jump shot" in string.lower():
        return 1
    if "layup" in string.lower():
        return 2
    if "dunk" in string.lower():
        return 0
    if "free throw" in string.lower():
        return 3
    return 3
    
def percent_error(actual, predicted):
    #percent error
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