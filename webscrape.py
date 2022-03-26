import re
import requests, bs4

class Scraper:
    #date should be in format of '2022-03-16'
    def __init__(self, date, teams):
        
        self.game_url = 'https://plaintextsports.com/nba/' + date + '/' + teams
        self.teams = teams.upper()
        #Gets page from url, gets the text, then makes a Beautiful soup object with it for parsing
        self.game_site = bs4.BeautifulSoup(requests.get(self.game_url).text)
        
        #Gets the elements from the page, then make self.team1site and team2site from them
        
        elems = self.game_site.select('.text-fg')
        urls = list(set([x[href] for x in elems]))


        self.team1_url = "https://plaintextsports.com" + self.game_site.select('.flex.justify-between > div.flex.flex-1.flex-col.items-center > b')[0].a['href']
        self.team2_url = "https://plaintextsports.com" + self.game_site.select('.flex.justify-between > div.flex.flex-1.flex-col.items-center > b')[-1].a['href']
        #REMEMBER TO RETURN STRINGS
        create_player_impact_list(self)
    def get_plays(self):
        # self.plays = []

        # not_done = True
        # for quarter in range(1, 5):
        #     for play in range(0, 200):
        #         curr = self.main_site.select('#play-q{}-{} + div'.format(quarter, play))
        #         try:
        #             lol = curr[0].getText()
        #             print(lol)
        #             self.plays.append(lol[:-2])
        #         except:
        #             continue
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
        self.plays = formatted
    def get_team_record(self, ):
        # calculates the team record before the game
        pass
    def get_winner(self):
        
        if self.score1 > self.score2:
            return self.teams[0:3]
        if self.score2 > self.score1:
            return self.teams[4:7]
        return "TIE"
            
    def get_final_score(self):
        self.scores = str(self.game_site.select(".container.text-center"))
        self.scores = str(self.game_site.select(".container.text-center"))
        self.scores = self.scores.splitlines()
        self.score1 = int(self.scores[2][len(self.scores[2])-9: len(self.scores[2])-6])
        self.score2 = int(self.scores[3][len(self.scores[3])-7: len(self.scores[3])-4])
        return [self.score1, self.score2]
        # [score1, score2]
    
    # HACK: this method is NOT static, only for test
    @staticmethod
    def get_player_array():
        # [[team1 start], [team1 bench], [team2 start], [team2 bench]]
        # HACK: this is test, pls remove
        test_site = bs4.BeautifulSoup(requests.get("https://plaintextsports.com/nba/2022-03-25/was-det").text)
        players = []
        
        box_player_elems = test_site.select('.box-score-players > div')
        for player in range(0, len(box_player_elems), 2):
            players.append(box_player_elems[player].getText())
        return players
        

   
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
        teams_site = bs4.BeautifulSoup(requests.get(url).text)
        for link in teams_site.select('a.text-fg.no-underline'):
            text = link.get('href')
            teams.append(text[len(text) - 7::])
        return teams
    
    @staticmethod
    def get_full_name(team):
        match team:
            case 'ATL':
                return 'atlanta-hawks'
            case 'BOS':
                return 'boston-celtics'
            case 'BKN':
                return 'brooklyn-nets'
            case 'CHA':
                return 'charlotte-hornets'
            case 'CHI':
                return 'chicago-bulls'
            case 'CLE':
                return 'cleveland-cavaliers'
            case 'DAL':
                return 'dallas-mavericks'
            case 'DEN':
                return 'denver-nuggets'
            case 'DET':
                return 'detroit-pistons'
            case 'GSW':
                return 'golden-state-warriors'
            case 'HOU':
                return 'houston-rockets'
            case 'IND':
                return 'indiana-pacers'
            case 'LAC':
                return 'los-angeles-clippers'
            case 'LAL':
                return 'los-angeles-lakers'
            case 'MEM':
                return 'memphis-grizzlies'
            case 'MIA':
                return 'miami-heat'
            case 'MIL':
                return 'milwaukee-bucks'
            case 'MIN':
                return 'minnesota-timberwolves'
            case 'NOP':
                return 'new-orleans-pelicans'
            case 'NYK':
                return 'new-york-knicks'
            case 'OKC':
                return 'oklahoma-city-thunder'
            case 'ORL':
                return 'orlando-magic'
            case 'PHI':
                return 'philadelphia-76ers'
            case 'PHX':
                return 'phoenix-suns'
            case 'POR':
                return 'portland-trail-blazers'
            case 'SAC':
                return 'sacramento-kings'
            case 'SAS':
                return 'san-antonio-spurs'
            case 'TOR':
                return 'toronto-raptors'
            case 'UTA':
                return 'utah-jazz'
            case 'WAS':
                return 'washington-wizards'
            case _:
                return '!!invalid!!'
