import game
import curses_usage
import webscrape
from curses import wrapper

# Preplay code begins
# Make players

print("Welcome to basket-watch [v0.1.0]!\n")
while True:
  try:
    num_players = int(input("How many players are playing? (number): "))
    break
  except ValueError:
    print("Please enter a number.")
    
players = []
for i in range(num_players):
  players.append(0)  

# Select date
print("\n")
while True:
  try:
    year = int(input("Enter year (YYYY): "))
    if year == 2021 or year == 2022:
      break
    print("Please enter a year from this season. (2021-2022)")
  except ValueError:
    print("Please enter a valid year. (YYYY)")

while True:
  try:
    month = int(input("Month (MM): "))
    if month <= 4 and month >= 10 and month > 0 and month < 13:
      break
    print("Please enter amonth from this season (Oct 2021, Apr 2022")
  except ValueError:
    print("Please enter a valid month. (MM)")

while True:
  try:
    day = int(input("Day (DD): "))
    if day > 0 and day < 32:
      break
    print("Please enter a valid day. (DD)")
  except ValueError:
    print("Please enter a valid day. (DD)")
    
game_date = str(year) + "-" + str(month) + "-" + str(day)

# List game teams

team_array = webscrape.teams_on_day(game_date)
for i in range(len(team_array)):
  print(str(i + 1) + ": " + team_array[i])
print("\n")

while True:
  try:
    team_index = int(input("Enter team index (number): "))
    if team_index >= 0 and team_index < len(team_array):
      break
    print("Please enter a valid team index. 1-" + str(len(team_array)))
  except ValueError:
    print("Please enter a number.")

team_str = team_array[team_index - 1]

# Webscrape all info

scraper = webscrape.Scraper(game_date, team_str)

# Show users hint info



# Player bets


# Play out game
def main(stdscr):
  curses_usage.init(stdscr)
wrapper(main)
