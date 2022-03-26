import requests, bs4, pandas

class Scraper:
    #date should be in format of '2022-03-16'
    def __init__(self, date, teams):
        self.game_url = 'https://plaintextsports.com/nba/' + date + '/' + teams
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
        import pandas

        data = pandas.DataFrame(columns=["Events"])
        data_list = []

        not_done = True
        quarter = 1
        play_num = 0
        while(not_done):
            curr = self.main_site.select('#play-q{}-{} + div'.format(quarter, play_num))
            if curr == None and quarter < 4:
                quarter += 1
            elif quarter == 4 and curr == None:
                not_done = False
            else:
                play_num += 1
                data_list.append(curr)
                lol = curr[0].getText()
                print(lol)
                data.append(pandas.DataFrame({'Events':[lol]}), ignore_index=True)
    def get_team_record(self):
        # calculates the team record before the game
        pass
    def get_winner(self):
        self.scores = self.game_site.select(".container.text-center").get_text()
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
        for link in teams_site.find_all('a.text-fg.no-underline'):
            text = link.get_text()
            # FIXME: 6 may be wrong value
            teams.append(text[text.length - 6::])
        return teams
        
