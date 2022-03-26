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

# Select game

print("\n")


# Webscrape all info

# Show users hint info

# Player bets


# Play out game
def main(stdscr):
  curses_usage.init(stdscr)
wrapper(main)
