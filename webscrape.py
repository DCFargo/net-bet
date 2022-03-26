import requests, bs4, pandas

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


        self.team1_url = ''
        self.team2_url = ''
        self.team1_site = bs4.BeautifulSoup(requests.get(self.team1_url).text)
        self.team2_site = bs4.BeautifulSoup(requests.get(self.team2_url).text)
        #REMEMBER TO RETURN STRINGS
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
        plays_unformatted = self.main_site.select('.play-by-play-toggle-content .play-by-play > b.score > div')
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
        self.plays = formatted
    def get_team_record(self):
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
    def get_mvp(self):
        pass
    def get_lvp(self):
        pass
    def get_team_record(self):
        pass
    def get_dumb_box_score_info(self):
        #this is weird and pain so we deal with it later
        # returns array of strings corr to teams
        pass
    @staticmethod
    def teams_on_day(date):
        teams = []
        url = 'https://plaintextsports.com/nba/' + date
        teams_site = bs4.BeautifulSoup(requests.get(url).text)
        for link in teams_site.select('a.text-fg.no-underline'):
            text = link.get('href')
            teams.append(text[len(text) - 7::])
        return teams
        
