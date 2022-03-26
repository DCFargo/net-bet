import re
import requests, bs4

class Scraper:
    #date should be in format of '2022-03-16'
    def __init__(self, date, teams):
        
        self.game_url = 'https://plaintextsports.com/nba/' + date + '/' + teams
        self.teams = teams.upper()
        #Gets page from url, gets the text, then makes a Beautiful soup object with it for parsing
        self.game_site = bs4.BeautifulSoup(requests.get(self.game_url).text, features="lxml")
        

        #Gets the elements from the page, then make self.team1site and team2site from them
        
        elems = self.game_site.select('.text-fg')
        # HACK this was throwing an error, god help me this doesn't break anything
        #urls = list(set([x[href] for x in elems]))

        # Initialize player lists
        # t1_players, t2_players

        self.team1_url = "https://plaintextsports.com" + self.game_site.select('.flex.justify-between > div.flex.flex-1.flex-col.items-center > b')[0].a['href']
        self.team2_url = "https://plaintextsports.com" + self.game_site.select('.flex.justify-between > div.flex.flex-1.flex-col.items-center > b')[-1].a['href']
        self.team1_site = bs4.BeautifulSoup(requests.get(self.team1_url).text, features='lxml')
        #team1_site = bs4.BeautifulSoup(requests.get(team1_url).text, features='lxml')
        #team1_url = "https://plaintextsports.com" + game_site.select('.flex.justify-between > div.flex.flex-1.flex-col.items-center > b')[0].a['href']

        self.team2_site = bs4.BeautifulSoup(requests.get(self.team2_url).text, features='lxml')
        self.get_player_array()
        
        self.get_plays()
        #REMEMBER TO RETURN STRINGS
        #self.create_player_impact_list(self)
    def get_plays(self):
        plays_unformatted = self.game_site.select('.play-by-play-toggle-content .play-by-play > b.score > div')
        formatted = []
        counter = 1
        for val in plays_unformatted:
            if counter == 1:
                formatted.append(val.getText()[:-1])
                counter += 1
            elif counter == 2:
                formatted.append(val.getText()[:-2])
                counter += 1
            else:
                formatted.append(val.getText().split(" ")[-1])
                counter = 1
        formatted.reverse()
        self.plays = formatted  # Has all the scoring plays, the time left in the match,
                                # and statements of what happened in the plays
    def get_winner(self):
        
        if self.score1 > self.score2:
            return self.teams[0:3]
        if self.score2 > self.score1:
            return self.teams[4:7]
        return "TIE"
            
    def get_final_score(self):
        #
        final_score = self.game_site.select('.flex.justify-between > div.flex.flex-1.flex-col.items-center > span')[1].parent
        final_score.span.extract()
        final_score = final_score.getText().split(' - ')
        self.score1 = final_score[0]
        self.score2 = final_score[1]
        return final_score
        # [score1, score2]
    
    
    @staticmethod
    def clean_player_string(player_string):
        valid = re.compile(r"\s?[\+|\-]?[0-9]+")
        if valid.match(player_string[len(player_string) - 2:]) is None:
            return player_string.strip()
        return player_string[0:len(player_string)-2].replace("+", "").replace("-", "").strip()
    
    def get_player_array(self):
        # [[team1 start], [team1 bench], [team2 start], [team2 bench]]
        self.players = []
        
        # TODO separate by team
        t1_site = bs4.BeautifulSoup(requests.get(self.game_url).text, features="lxml")
        box_player_elems = t1_site.select('.box-score-players > div')
        for player in box_player_elems:
            self.players.append(player.getText())
        self.players = list(filter(lambda x: x[0:1]!=" " and x[len(x)-1:]!="S", self.players))
        self.players = list(map(lambda x: Scraper.clean_player_string(x), self.players))
   
    def create_player_impact_list(self):
        self.player_impact_list = self.game_site.find_all(".text-gray")
        for x in self.player_impact_list:
            if not (x[0:1] == "+" or x[0:1] == "-"):
                self.player_impact_list.remove(x)
        
    def get_mvp(self):
        h_pos = 0
        for x in range(1, len(self.player_impact_list)):
            if(self.player_impact_list>self.player_impact_list[h_pos]):
                h_pos = x
        return self.players[h_pos]
        
    def get_lvp(self):
        l_pos = 0
        for x in range(1, len(self.player_impact_list)):
            if(self.player_impact_list<self.player_impact_list[l_pos]):
                l_pos = x
        return self.players[l_pos]
    
    def get_team_record(self): 
        def is_our_game(tag: bs4.Tag):
            if tag.has_attr('href'):
                return "https://plaintextsports.com" + tag['href'] == self.game_url
            return False

        self.teams_record: list[tuple[int, int]] = []

        attempt = self.team1_site.find(is_our_game)
        dub_or_l = attempt.span.getText() # "W" or "L"
        attempt.span.extract()
        win_loss_record: list[int] = attempt.next_sibling.strip().split('-')
        win_loss_record = [int(win_loss) for win_loss in win_loss_record]
        if (dub_or_l.upper() == 'W'):
            win_loss_record[0] -= 1
        else:
            win_loss_record[1] -= 1
        self.teams_record.append(win_loss_record)
        attempt2 = self.team2_site.find(is_our_game)
        dub_or_l = attempt2.span.getText()
        attempt2.span.extract()
        win_loss_record: list[int, int] = attempt.next_sibling.strip().split('-')
        win_loss_record = [int(win_loss) for win_loss in win_loss_record]
        if (dub_or_l.upper() == 'W'):
            win_loss_record[0] -= 1
        else:
            win_loss_record[1] -= 1
        self.teams_record.append(win_loss_record)
        



    def get_dumb_box_score_info(self):
        #this is weird and pain so we deal with it later
        # returns array of strings corr to teams
        # first lead changes
        lead_changes = self.game_site.find_all('b', string='Lead Changes: ')[0].parent
        lead_changes.b.extract()
        self.lead_changes = lead_changes.getText()
        # then times tied
        times_tied = self.game_site.find_all('b', string='Times Tied: ')[0].parent
        times_tied.b.extract()
        self.times_tied = times_tied.getText()
        # then the biggest lead pain
        biggest_lead = self.game_site.find_all('b', string='Biggest Lead: ')[0].parent
        biggest_lead.b.extract()
        lead_list = biggest_lead.getText().split(", ")  # [ 'team: num', 'team: num' ]
        lead_list = [string.split(": ") for string in lead_list]    # [ [team, num], [team, num]  ]
        self.biggest_lead = {listed[0]:listed[1] for listed in lead_list}   # {team:num, team:num}
    @staticmethod
    def teams_on_day(date):
        teams = []
        url = 'https://plaintextsports.com/nba/' + date
        teams_site = bs4.BeautifulSoup(requests.get(url).text, features="lxml")
        for link in teams_site.select('a.text-fg.no-underline'):
            text = link.get('href')
            teams.append(text[len(text) - 7::])
        return teams
    
    @staticmethod
    def get_full_name(team):
        match team.upper():
            case 'ATL':
                return 'Atlanta Hawks'
            case 'BOS':
                return 'Boston Celtics'
            case 'BKN':
                return 'Brooklyn Nets'
            case 'CHA':
                return 'Charlotte Hornets'
            case 'CHI':
                return 'Chicago Bulls'
            case 'CLE':
                return 'Cleveland Cavaliers'
            case 'DAL':
                return 'Dallas Mavericks'
            case 'DEN':
                return 'Denver Nuggets'
            case 'DET':
                return 'Detroit Pistons'
            case 'GSW':
                return 'Golden State Warriors'
            case 'HOU':
                return 'Houston Rockets'
            case 'IND':
                return 'Indiana Pacers'
            case 'LAC':
                return 'Los Angeles Clippers'
            case 'LAL':
                return 'Los Angeles Lakers'
            case 'MEM':
                return 'Memphis Grizzlies'
            case 'MIA':
                return 'Miami Heat'
            case 'MIL':
                return 'Milwaukee Bucks'
            case 'MIN':
                return 'Minnesota Timberwolves'
            case 'NOP':
                return 'New Orleans Pelicans'
            case 'NYK':
                return 'New York Knicks'
            case 'OKC':
                return 'Oklahoma City Thunder'
            case 'ORL':
                return 'Orlando Magic'
            case 'PHI':
                return 'Philadelphia 76ers'
            case 'PHX':
                return 'Phoenix Suns'
            case 'POR':
                return 'Portland Trail Blazers'
            case 'SAC':
                return 'Sacramento Kings'
            case 'SAS':
                return 'San Antonio Spurs'
            case 'TOR':
                return 'Toronto Raptors'
            case 'UTA':
                return 'Utah Jazz'
            case 'WAS':
                return 'Washington Wizards'
            case _:
                return '!!invalid!!'
    
    def get_team_arr_from_teams(self):
        return [Scraper.get_full_name(self.teams[:3]), Scraper.get_full_name(self.teams[len(self.teams) - 3:])]

