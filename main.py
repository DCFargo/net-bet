import game
import curses_usage
import webscrape
from curses import wrapper

def main(stdscr):
  curses_usage.init(stdscr)
wrapper(main)
print("Hello, world!")
