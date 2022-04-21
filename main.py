from bot import Bot
import l_utils
import time
import sys

if __name__ == "__main__":

    debug = True if ("--debug" in sys.argv) else False

    bot = Bot(debug)

    print("waiting for 5 seconds, please select the btd 6 window")
    time.sleep(5)
    # Check for obyn

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
