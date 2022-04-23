
import time
import sys

import l_utils
from bot import Bot

if __name__ == "__main__":

    DEBUG = True if ("--debug" in sys.argv) else False

    bot = Bot(DEBUG)

    print("waiting for 5 seconds, please select the btd 6 window")
    time.sleep(5)
    # Check for obyn
    print("Selecting obyn if not selected")
    bot.hero_obyn_check()

    while bot.running:
        print("selecting map")

        # Prevent alt+tab bug from happening
        l_utils.press_key("alt")

        # Choose map
        bot.select_map()   

        print("Game start")
        # main game
        bot.ingame_loop()
        # statDict["Won_Games"] += won
        # statDict["Lost_Games"] += lost
