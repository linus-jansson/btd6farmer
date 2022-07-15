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
    bot = Bot("--debug" in sys.argv)

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
        
    print("Setting up automation...")
    
    data = None
    with open(current_directory + "\setup.txt") as file:
        data = file.read().split()

    hero = data[0].lower()
    current_map = data[1]
    map_page = static.maps[current_map][0]
    map_index = static.maps[current_map][1]
    difficulty = data[2]
    gamemode = data[3]

    print("Setup Complete.")

    print("Waiting for 5 seconds, please select the btd 6 window")
    time.sleep(5)
    # Check for obyn
    print("Selecting obyn if not selected")
    bot.hero_select(hero)

    # Make sure we haven't exited by using the stop key.
    while bot.running:
        print("selecting map")

        # Prevent alt+tab bug from happening
        l_utils.press_key("alt")

        # Choose map
        bot.select_map(map_page, map_index, difficulty, gamemode)   

        bot.load_instructions(current_directory + "\instructions.csv")

        print("Game start")
        # main game
        bot.ingame_loop()

