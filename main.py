import time
import sys
from pathlib import Path
from Bot import Bot
 
if __name__ == "__main__":

    def usage():
        raise Exception("No valid argument for directory.. 'python main.py <directory to gameplan>'")

    # Verify that a valid path was fed to the script to find instructions
    if len(sys.argv) != 1:
        usage()
    # Verify that the first argument is a directory
    directory = Path(sys.argv[0])
    # Verify that the first argument is a directory.
    if not directory.is_dir():
        usage()
    # Verify directory exist.
    if not directory.exists():
        usage()

    current_directory = directory
    
    # TODO: Move all these prints to verbose only mode

    bot = Bot(instruction_path=current_directory, debug_mode=("--debug" in sys.argv), verbose_mode=("--verbose" in sys.argv))

    print("Setting up Bot...")
    
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

