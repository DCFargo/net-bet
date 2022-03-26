import requests, bs4

class Scraper:
    #date should be in format of '2022-03-16'
    def __init__(self, date, teams):
        self.game_url = 'https://plaintextsports.com/nba/' + date + '/' + teams
        #Gets page from url, gets the text, then makes a Beautiful soup object with it for parsing
        self.game_site = bs4.BeautifulSoup(requests.get(self.game_url).text)
        
        #Gets the elements from the game site that have the urls to the teams
        elems = self.game_site.select('.text-fg')
        urls = list(set([x['href'] for x in elems]))
        
        #Make the url and BeautifulSoup for each team
        self.team1_url = 'https://plaintextsports.com' + urls[0]
        self.team2_url = 'https://plaintextsports.com' + urls[1]
        self.team1_site = bs4.BeautifulSoup(requests.get(self.team1_url).text)
        self.team2_site = bs4.BeautifulSoup(requests.get(self.team2_url).text)

    def get_plays(self):
        # getting play-by-play
        self.game_site.select('.play-by-play-toggle-content')
        # q-play-by-play
    def get_team_record(self):
        
    # this is for later
    @staticmethod
    def teams_on_day(date):
        url = 'https://plaintextsports.com/nba/' + date
