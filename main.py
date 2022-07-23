import time
import sys
from pathlib import Path
from Bot import Bot
 
if __name__ == "__main__":

    def no_gameplan_exception():
        raise Exception("No valid argument for directory.. 'python main.py --gameplan_path <directory to gameplan>'")

    # Retrives the gameplan from the command line and makes a Path object out of it
    gameplan_path = (Path(__file__).resolve().parent/sys.argv[sys.argv.index("--gameplan_path") + 1]) if "--gameplan_path" in sys.argv else no_gameplan_exception()

    # Verify directory exist.
    if not gameplan_path.exists():
        print("No directory found at: " + str(gameplan_path))
        no_gameplan_exception()
    # Verify that it is a directory
    if not gameplan_path.is_dir():
        print("Not a directory")
        no_gameplan_exception()
    
    bot = Bot(instruction_path=gameplan_path, debug_mode=("--debug" in sys.argv), verbose_mode=("--verbose" in sys.argv))
    print("Setting up Bot...")
    print("Using gameplan located in: " + str(gameplan_path))
    
    bot.initilize() # Initialize the bot (presses alt, etc)

    print("Waiting for 5 seconds... Please select the Bloons TD 6 window during this time.")
    time.sleep(5)

    # Check for obyn
    bot.hero_select()

    # Make sure we haven't exited by using the stop key.
    while bot.running:
        bot.check_for_collection_crates()

        print("selecting map")
        # Choose map
        bot.select_map()   

        print("Game start")

        # main game loop
        bot.ingame_loop()

