import requests, bs4

class Scraper:
    #date should be in format of '2022-03-16'
    def __init__(self, date, teams):
        self.game_url = 'https://plaintextsports.com/nba/' + date + '/' + teams
        #Gets page from url, gets the text, then makes a Beautiful soup object with it for parsing
        self.game_site = bs4.BeautifulSoup(requests.get(self.game_url).text)
        #Get teams from the page, then make self.team1site and team2site from them
        
        self.team1_url = ''
        self.team2_url = ''
        self.team1_site = bs4.BeautifulSoup(requests.get(self.team1_url).text)
        self.team2_site = bs4.BeautifulSoup(requests.get(self.team2_url).text)

    # this is for later
    @staticmethod
    def teams_on_day(date):
        url = 'https://plaintextsports.com/nba/' + date
