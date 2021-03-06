import curses
import game
import webscrape
from webscrape import Scraper

def update_anim_window(win, anim_index, teams, qstring):
  win.clear()
  win.addstr(0, 0, "-"*80)
  for i in range(24):
    win.addstr(i, 0, "|")
    #win.addstr(i, 79, "|")
  win.addstr(0, 6, "| Net Bet! v0.1.0 | " + teams + " | " + qstring + " |")
  match anim_index:
    case 0:
      for (i, line) in enumerate(game.dunk.splitlines(), 1):
        win.addstr(i, 1, line)
    case 1:
      for (i, line) in enumerate(game.jumpshot.splitlines(), 1):
        win.addstr(i, 1, line)
    case 2:
      for (i, line) in enumerate(game.layup.splitlines(), 1):
        win.addstr(i, 1, line)
    case 3:
      for (i, line) in enumerate(game.freethrow.splitlines(), 1):
        win.addstr(i, 1, line)
  win.refresh()

def update_play_window(win, score, text, playtext):
  win.clear()
  win.addstr(0, 0, "-"*80)
  #win.addstr(4, 0, "-"*80)
  
  for i in range(5):
    win.addstr(i, 0, "|")
    #win.addstr(i, 79, "|")
  win.addstr(0, 6, "| play information | press space to advance |")
  win.addstr(1, 3, score)
  #adds the string to the w indo w
  win.addstr(2, 3, text)
  win.addstr(3, 3, playtext)
  win.refresh()