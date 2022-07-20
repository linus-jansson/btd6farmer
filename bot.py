import pyautogui
import time
import cv2
import re
import numpy as np
import sys
import os
import csv

# Temporary until handleInstrucion is fixed
import mouse
import keyboard

import pytesseract

if sys.platform == "win32":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import Log
import static

from BotCore import BotCore

class Bot(BotCore):
    def __init__(self, instruction_path, debug_mode=False, verbose_mode=False):
        super().__init__(instruction_path)
        
        # Change to current Directory
        # Change to: https://github.com/rr-/screeninfo
        self.width, self.height = pyautogui.size()

        self.start_time = time.time()
        self.running = True
        self.DEBUG = debug_mode
        self.VERBOSE = verbose_mode

        # When mouse is moved to (0, 0)
        pyautogui.FAILSAFE = True

    def getRound(self):
        # Change to https://stackoverflow.com/questions/66334737/pytesseract-is-very-slow-for-real-time-ocr-any-way-to-optimise-my-code 
        # or https://www.reddit.com/r/learnpython/comments/kt5zzw/how_to_speed_up_pytesseract_ocr_processing/

        top, left = self.scaling([1850, 35])
        width, height = [225, 65]
        img = pyautogui.screenshot(region=(top, left, width, height))

        numpyImage = np.array(img)

        # Make image grayscale using opencv
        greyImage = cv2.cvtColor(numpyImage, cv2.COLOR_BGR2GRAY)

        # Threasholding
        final_image = cv2.threshold(greyImage, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
        # Get current round from image with tesseract
        text = pytesseract.image_to_string(final_image,  config='--psm 7').replace("\n", "")

        # if self.DEBUG:
            # print(f"Found round text: {text}")

        # regex to look for format [[:digit:]]/[[:digit:]] if not its not round, return None
        if re.search(r"(\d+/\d+)", text):
            return int(text.split("/")[0])
        else:
            return None

    def initilize(self):
        if self.DEBUG:
            print("RUNNING IN DEBUG MODE, DEBUG FILES WILL BE GENERATED")

        self.press_key("alt")


    def ingame_loop(self):

        current_round = -1
        ability_one_timer = time.time()
        ability_two_timer = time.time()
        game_start_time = time.time()
        
        finished = False

        middle_of_screen = self.width//2, self.height//2

        # main ingame loop
        while not finished:

            # Check for levelup or insta monkey (level 100)
            if self.check_levelup() or self.insta_monkey_check():
                self.click(middle_of_screen, amount=2)

            # Check for finished or failed game
            if self.defeat_check() or self.victory_check():
                # DEBUG
                if self.DEBUG:
                    if self.defeat_check():
                        print("Defeat detected on round {}; exiting level".format(current_round))
                        Log.log_stats(did_win=False, match_time=(time.time()-game_start_time))
                    elif self.victory_check():
                        print("Victory detected; exiting level") 
                        Log.log_stats(did_win=True, match_time=(time.time()-game_start_time))
                
                self.exit_level()
                finished = True
                self.reset_game_plan()
                continue

            current_round = self.getRound()

            if current_round != None:
                # Saftey net; use abilites
                # TODO: Make this more general to support more gameplans
                if current_round >= 39 and self.abilityAvaliabe(ability_one_timer, 35):
                    self.press_key("1")
                    ability_one_timer = time.time()
                
                if current_round >= 51 and self.abilityAvaliabe(ability_two_timer, 90):
                    self.press_key("2")
                    ability_two_timer = time.time()

                # Check for round in game plan
                if str(current_round) in self.game_plan:
                    
                    # Handle all instructions in current round
                    for instruction in self.game_plan[str(current_round)]:
                        if not "DONE" in instruction:
                            self.handleInstruction(instruction)
                            instruction["DONE"] = True

                    if self.DEBUG:
                        Log.log("Current round", current_round)

    def exit_bot(self): 
        self.running = False

    def place_tower(self, tower_position, keybind):
        self.press_key(keybind) # press keybind
        self.click(tower_position) # click on decired location

    def upgrade_tower(self, tower_position, upgrade_path):
        self.click(tower_position)
        
        # Convert upgrade_path to something usable
        upgrade_path = upgrade_path.split("-")
        top, middle, bottom = tuple(map(int, upgrade_path))
        
        for _ in range(top):
            self.press_key(static.upgrade_keybinds["top"])

        for _ in range(middle):
            self.press_key(static.upgrade_keybinds["middle"])

        for _ in range(bottom):
            self.press_key(static.upgrade_keybinds["bottom"])
        
        self.press_key("esc")

    def change_target(self, tower_name, tower_position, targets):
        # target_array = targets.split(", ")
        
        self.click(tower_position)

        current_target_index = 0

        # for each target in target list
        for i in targets:
            
            # Math to calculate the difference between current target index and next target index
            if "SPIKE" in tower_name:
                target_diff = abs((static.target_order_spike.index(i)) - current_target_index)
            else:
                target_diff = abs((static.target_order_regular.index(i)) - current_target_index)
                # print("Target diff", target_diff)

            # Change target until on correct target
            for n in range(1, target_diff + 1):
                current_target_index = n
                self.press_key("tab")

            # Used for microing if length of target array is longer than 1 
            # and the last item of the array is not == to current target
            if len(targets) > 1 and targets[-1] != i:
                time.sleep(3) # TODO: specify this in the game plan

        self.press_key("esc")

    def set_static_target(self, tower_position, target_pos):
        pyautogui.moveTo(self.scaling(tower_position))
        time.sleep(0.5)
        mouse.click(button="left")

        time.sleep(1)

        pyautogui.moveTo(self.scaling(static.button_positions["TARGET_BUTTON_MORTAR"]))
        
        time.sleep(1)
        mouse.press(button='left')
        time.sleep(0.5)
        mouse.release(button='left')

        time.sleep(1)

        pyautogui.moveTo(self.scaling(target_pos))
        time.sleep(0.5)
        mouse.press(button='left')
        time.sleep(0.5)
        mouse.release(button='left')

        time.sleep(1)

        self.press_key("esc")

    def handleInstruction(self, instruction):
        upgrade_path = instruction["UPGRADE_DIFF"]
        monkey_position = instruction["POSITION"]
        target = instruction["TARGET"]
        keybind = static.tower_keybinds[instruction["TOWER"]]

        # if upgrade_path is None the tower isn't placed yet, so place it
        if upgrade_path is None:
            self.place_tower(monkey_position, keybind)

            if self.DEBUG:
                Log.log("Tower placed:", instruction["TOWER"])
            
        else:
            self.upgrade_tower(monkey_position, upgrade_path)

            if self.DEBUG:
                Log.log("Upgrading {} to {}; change {}".format(instruction['TOWER'], instruction['UPGRADE'], instruction['UPGRADE_DIFF']))

        # If target position is not None
        # Special case for mortars and towers with static targeting
        if instruction["TARGET_POS"]:
            self.set_static_target(monkey_position, instruction["TARGET_POS"])
            
            if self.DEBUG:
                Log.log("Monkey static target change", instruction["TOWER"])

        if instruction["ROUND_START"]:
            print("Starting first round")
            self.press_key("space")
            self.press_key("space")

        # Change monkey to target (eg strong)
        if target:
            self.change_target(instruction["TOWER"], monkey_position, target)

            if self.DEBUG:
                Log.log(f"{instruction['TOWER']} target change to {target}")

    def abilityAvaliabe(self, last_used, cooldown, fast_forward=True):
        # TODO: Store if the game is speeded up or not. If it is use the constant (true by default)
        m = 1
        if fast_forward:
            m = 3

        return (time.time() - last_used) >= (cooldown / m)
  
    def collections_event_check(self):
        if self.collection_event_check:
            if self.DEBUG:
                Log.log("easter collection detected")

            self.click("EASTER_COLLECTION") #DUE TO EASTER EVENT:
            time.sleep(1)
            self.click("LEFT_INSTA") # unlock insta
            time.sleep(1)
            self.click("LEFT_INSTA") # collect insta
            time.sleep(1)
            self.click("RIGHT_INSTA") # unlock r insta
            time.sleep(1)
            self.click("RIGHT_INSTA") # collect r insta
            time.sleep(1)
            self.click("F_LEFT_INSTA")
            time.sleep(1)
            self.click("F_LEFT_INSTA")
            time.sleep(1)
            self.click("MID_INSTA") # unlock insta
            time.sleep(1)
            self.click("MID_INSTA") # collect insta
            time.sleep(1)
            self.click("F_RIGHT_INSTA")
            time.sleep(1)
            self.click("F_RIGHT_INSTA")
            time.sleep(1)

            time.sleep(1)
            self.click("EASTER_CONTINUE")

            # awe try to click 3 quick times to get out of the easter mode, but also if easter mode not triggered, to open and close profile quick
            self.click("EASTER_EXIT")
            time.sleep(1)
            
    # select hero if not selected
    def hero_select(self):
        if not self.hero_check(self.settings["HERO"]):
            print(f"Selecting {self.settings['hero']}")
            self.click("HERO_SELECT")
            self.click(self.settings["HERO"])
            self.click("CONFIRM_HERO")
            self.press_key("esc")

    def exit_level(self):
        self.click("VICTORY_CONTINUE")
        time.sleep(2)
        self.click("VICTORY_HOME")
        time.sleep(4)

        self.collections_event_check()
        time.sleep(2)

    def select_map(self):
        map_page = static.maps[self.settings["MAP"]][0]
        map_index = static.maps[self.settings["MAP"]][1]
        
        #map_page, map_index, difficulty, gamemode
        time.sleep(1)

        self.click("HOME_MENU_START")
        self.click("EXPERT_SELECTION")
        
        self.click("BEGINNER_SELECTION") # goto first page

        # click to the right page
        self.click("RIGHT_ARROW_SELECTION", amount=(map_page - 1))

        self.click("MAP_INDEX_" + str(map_index)) # Click correct map
        self.click(self.settings["DIFFICULTY"]) # Select Difficulty
        self.click(self.settings["GAMEMODE"]) # Select Gamemode
        self.click("OVERWRITE_SAVE")

        time.sleep(3) # wait for loading screen
        self.click(self.settings["DIFFICULTY"])
        self.click("CONFIRM_CHIMPS")