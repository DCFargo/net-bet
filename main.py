from multiprocessing.sharedctypes import Value
import game
import curses_usage, curses
from webscrape import Scraper
from curses import wrapper

# Preplay code begins
# Make players
print("All data courtesy of plaintextsports.com, thanks! :)\n")
print("Welcome to Net Bet!!\n")
while True:
  try:
    num_players = int(input("How many players are playing? (number): "))
    break
  except ValueError:
    print("Please enter a number.")

#coding stuff
while True:
  try:
    starting_money = int(input('Please enter a whole number amount of money to start with: '))
    if starting_money > 0:
      break
    else:
      print("Invalid input.")
  except:
    print("Invalid input.")
players = []
for i in range(num_players):
  players.append(game.Player(starting_money))  
cont = True
while cont:
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

    #loop
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
      if team_index >= 0 and team_index <= len(team_array):
        break
      print("Please enter a valid team index. 1-" + str(len(team_array)))
    except ValueError:
      print("Please enter a number.")

  team_str = team_array[team_index - 1]

  # Webscrape all info

  scraper = Scraper(game_date, team_str)

  # Show users hint info

  print("\n" + "-" * 80)
  
  # Player bets
  for i in range(len(players)):
    while True:
      print("\n\nPlayer " + str(i + 1) + " balance: " + str(players[i].balance) + "\n")
      print("These are the betting categories:")
      for j in range(len(game.Player.category)):
        print(str(j + 1) + ": " + game.Player.category[j])
      print("\n")
      while True:
        try:
          bet_category = int(input("Enter betting category (number): "))
          if bet_category > 0 and bet_category <= len(game.Player.category) + 2:
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
              #make variable
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
          #loop
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
          #k is 1
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
              #reprimand user for their stupidity
              print("Please enter a number.")
          while True:
            try:
              loser_score = int(input("Enter loser score prediction (number): "))
              break
            except ValueError:
              print("Please enter a number.")
          bet_prediction = (winner_score, loser_score)
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
        case 7:
          break #our sanity
        case 8:
          exit()
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
              continue
            else:
              #forcefully remove the human's money
              players[i].balance -= bet_amount
              break
          except ValueError:
            bet_amount = input("Please enter a valid number: ")
            
      players[i].bets.append((bet_category, bet_prediction, bet_amount))
    
  # Play out game
  #def main(stdscr):
  #  curses_usage.init(stdscr)
  #wrapper(main)

  # HACK: text print version for debug
 
  print("Heads up, please resize your terminal to be > 80x24 if you haven't already!") 
  input("Press enter to continue...")
  init = game.Game(scraper.plays, scraper.teams)
  final_score = scraper.get_final_score()
  winner = scraper.get_winner()
  print("Winner is.... " + Scraper.get_full_name(winner) + "!\n\n")

  for i, player in enumerate(players):
    player.calc_results(winner, scraper.win_loss_ratio, scraper.get_mvp(), scraper.get_lvp(), final_score, scraper.lead_changes, scraper.times_tied, scraper.biggest_biggest_lead)
    player.update_balance()
    print("Player {} has ${} remaining. ".format(i+1, player.balance))
    if player.balance > starting_money:
      print("They made money! Congratulations!\n")
    else:
      print("They unfortunately didn't make money... Maybe next time!\n")
   
  cont = input("Continue? (y/n): ").lower() == 'y'
  if cont:
    print("Starting next game.\n\n\n")

print('Thanks for playing Net Bet!')