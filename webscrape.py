import requests, bs4, pandas

class Scraper:
    #date should be in format of '2022-03-16'
    def __init__(self, date, teams):
        self.game_url = 'https://plaintextsports.com/nba/' + date + '/' + teams
        #Gets page from url, gets the text, then makes a Beautiful soup object with it for parsing
        self.game_site = bs4.BeautifulSoup(requests.get(self.game_url).text)
        
        #Gets the elements from the page, then make self.team1site and team2site from them
        
        elems = self.game_site.select('.text-fg')
        urls = list(set([x[href] for x in elems]


        self.team1_url = ''
        self.team2_url = ''
        self.team1_site = bs4.BeautifulSoup(requests.get(self.team1_url).text)
        self.team2_site = bs4.BeautifulSoup(requests.get(self.team2_url).text)
        #REMEMBER TO RETURN STRINGS
    def get_plays(self):
        # getting play-by-play
        self.game_site.select('.play-by-play-toggle-content')
        self.plays = pandas.DataFrame()
        # q-play-by-play
    def get_team_record(self):
        # calculates the team record before the game
        
    def get_winner(self):
        
    def get_mvp(self):
        
    def get_lvp(self):
        
    def get_team_record(self):
                 
    def get_dumb_box_score_info(self):
        #this is weird and pain so we deal with it later
    # returns array of strings corr to teams
    @staticmethod
    def teams_on_day(date):
        url = 'https://plaintextsports.com/nba/' + date
