from multiprocessing.sharedctypes import Value
import game
import curses_usage
from webscrape import Scraper
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
  players.append(game.Player(1000))  

# Select date
print("\n")
while True:
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
      if (month <= 4 or month >= 10) and month > 0 and month < 13:
        break
      print("Please enter a month from this season (Oct 2021, Apr 2022)")
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

  game_date = str(year) + "-" + (str(month) if month > 9 else "0" + str(month)) + "-" + (str(day) if day > 9 else "0" + str(day))
  print(game_date)
  # List game teams

  team_array = Scraper.teams_on_day(game_date)
  if len(team_array) != 0:
    break
  else:
    print ("No games on this day. Please try again.")
    
for i in range(len(team_array)):
  matchup = team_array[i].split('-')
  matchup = Scraper.get_full_name(matchup[0]) + " vs. " + Scraper.get_full_name(matchup[1])
  print(str(i + 1) + ": " + matchup)
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

scraper = Scraper(game_date, team_str)

# Show users hint info

print("\n" + "-" * 80)
print(scraper.get_team_record())

# Player bets

for i in range (len(players)):
  print("\n\nPlayer " + str(i + 1) + " balance: " + str(players[i].balance) + "\n")
  print("These are the betting categories:")
  for j in range(len(game.Player.category)):
    print(str(j + 1) + ": " + game.Player.category[j])
  print("\n")
  while True:
    try:
      bet_category = int(input("Enter betting category (number): "))
      if bet_category > 0 and bet_category <= len(game.Player.category):
        break
      print("Please enter a valid category. 1-" + str(len(game.Player.category)))
    except ValueError:
      print("Please enter a number.")
  bet_category -= 1
  match bet_category:
    case 0: #winner
      print("Selected winner category.")
      for team in range(0, len(scraper.get_team_arr_from_teams())):
        print(str(team + 1) + ": " + scraper.get_team_arr_from_teams()[team])
      while True:
        try:
          bet_prediction = int(input("Enter prediction (number): ")) - 1
          if bet_prediction >= 0 and bet_prediction < len(scraper.get_team_arr_from_teams()):
            break
          print("Please enter a valid prediction. 1-" + str(len(scraper.get_team_arr_from_teams())))
        except ValueError:
          print("Please enter a number.")
        
    case 1: #mvp
      print("Selected MVP category.")
      k = 1
      for player in scraper.players:
        print(str(k) + ": " + player) 
        k += 1
      print("\n")
      while True:
        try:
          bet_prediction = int(input("Enter prediction (number): ")) - 1
          if bet_prediction >= 0 and bet_prediction <= (len(scraper.players) + len(scraper.players)):
            break
          print("Please enter a valid prediction. 1-" + str(len(scraper.players) + len(scraper.players)))
        except ValueError:
          print("Please enter a number.")
      
    case 2: #lvp
      print("Selected LVP category.")
      k = 1
      for player in scraper.players:
        print(str(k) + ": " + player) 
        k += 1
      print("\n")
      while True:
        try:
          bet_prediction = int(input("Enter prediction (number): ")) - 1
          if bet_prediction >= 0 and bet_prediction <= (len(scraper.players) + len(scraper.players)):
            break
          print("Please enter a valid prediction. 1-" + str(len(scraper.players) + len(scraper.players)))
        except ValueError:
          print("Please enter a number.")
    case 3: #final score
      print("Selected final score category.")
      while True:
        try:
          winner_score = int(input("Enter winner score prediction (number): "))
          break
        except ValueError:
          print("Please enter a number.")
      while True:
        try:
          loser_score = int(input("Enter loser score prediction (number): "))
          break
        except ValueError:
          print("Please enter a number.")
      bet_prediction = [winner_score, loser_score]
    case 4: #lead changes
      print ("Selected lead changes category.")
      while True:
        try:
          bet_prediction = int(input("Enter lead changes prediction (number): "))
          break
        except ValueError:
          print("Please enter a number.")
    case 5: #times tied
      print("Selected times tied category.")
      while True:
        try:
          bet_prediction = int(input("Enter times tied prediction (number): "))
          break
        except ValueError:
          print("Please enter a number.")
    case 6: #biggest lead
      print("Selected biggest lead category.")
      for team in range(0, len(scraper.get_team_arr_from_teams())):
        print(str(team + 1) + ": " + scraper.get_team_arr_from_teams()[team])
      while True:
        try:
          bet_prediction = int(input("Enter prediction (number): ")) - 1
          if bet_prediction >= 0 and bet_prediction < len(scraper.get_team_arr_from_teams()):
            break
          print("Please enter a valid prediction. 1-" + str(len(scraper.get_team_arr_from_teams())))
        except ValueError:
          print("Please enter a number.")
  # how much to bet
  if players[i].balance == 0:
    print("You do not have enough money left to bet.")
    bet_amount = 0
  else:
    while True:
      try:
        bet_amount = float(input("Enter bet amount ("+ str(players[i].balance) +"$ left): "))
        # check for valid money bet, and only 2 decimal places
        if bet_amount > players[i].balance or bet_amount <= 0 or int(bet_amount * 100) != bet_amount * 100:
          print("You can't bet money you don't have.")
          bet_amount = input("Please enter a valid number: ")
          continue
        else:
          players[i].balance -= bet_amount
          break
      except ValueError:
        bet_amount = input("Please enter a valid number: ")
        

  players[i].bet = [bet_category, bet_prediction, bet_amount] 
  
# Play out game
#def main(stdscr):
#  curses_usage.init(stdscr)
#wrapper(main)

# HACK: text print version for debug


# Calc results

for player in players:
  player.calc_results()