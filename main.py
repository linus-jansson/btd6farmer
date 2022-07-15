import os
import time
import sys
import pathlib

import l_utils
import static
from bot import Bot
 
if __name__ == "__main__":
    current_directory = ""

    # Small code cleanup for debug

    # Verify that a valid path was fed to the script to find instructions
    if len(sys.argv) >= 1:
        # Verify that one of the arguments is a directory
        for arguments in sys.argv:
            directory = str(pathlib.Path().resolve()) + arguments
            if os.path.isdir(directory):
                current_directory = directory

    # Verify directory exist, if not close the program with Exception
    if current_directory == "":
        raise Exception("No valid argument for directory.. 'python main.py <directory to gameplan>'")
    
    # TODO: Move all these prints to verbose only mode

    print("Setting up Bot...")
    
    bot = Bot(instruction_path=current_directory, debug_mode=("--debug" in sys.argv), verbose_mode=("--verbose" in sys.argv))

    print("Setup Complete.")

    print("Waiting for 5 seconds... Please select the Bloons TD 6 window during this time.")
    time.sleep(5)

    # Check for obyn
    print("Selecting obyn if not selected")
    bot.hero_select()

    # Make sure we haven't exited by using the stop key.
    while bot.running:
        print("selecting map")

        # Prevent alt+tab bug from happening
        l_utils.press_key("alt")

        # Choose map
        bot.select_map()   

        print("Game start")
        # main game
        bot.ingame_loop()

