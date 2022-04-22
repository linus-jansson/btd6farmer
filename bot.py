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

import log
import static
import l_utils as utils

class Bot():
    def __init__(self, debug=False):
        # Change to current Directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.width, self.height = pyautogui.size()

        self.start_time = time.time()
        self.running = True
        self.DEBUG = debug

        # When mouse is moved to (0, 0)
        pyautogui.FAILSAFE = True
        
        self.game_plan = self.__load_data("instructions.csv")
        
        ## Möjligtvis flytta dessa till där de behövs istället direkt
        self.levelup_path = f"Support_Files\\{str(self.height)}_levelup.png"
        self.victory_path = f"Support_Files\\{str(self.height)}_victory.png"
        self.defeat_path = f"Support_Files\\{str(self.height)}_defeat.png"
        self.menu_path = f"Support_Files\\{str(self.height)}_menu.png"
        self.easter_path = f"Support_Files\\{str(self.height)}_easter.png"
        self.obyn_hero_path = f"Support_Files\\{str(self.height)}_obyn.png"
        self.insta_monkey = f"Support_Files\\{str(self.height)}_instamonkey.png"

        self.statDict = {
            "Current_Round": None,
            "Last_Upgraded": None,
            "Last_Target_Change": None,
            "Last_Placement": None,
            "Uptime": 0
        }

    def getRound(self):
        # BYT TILL https://pypi.org/project/tesserocr/
        # https://stackoverflow.com/questions/66334737/pytesseract-is-very-slow-for-real-time-ocr-any-way-to-optimise-my-code
        # eller kanske inte  "I did some comparative tests between pytesseract and tesserocr, but the performance is not as different as said. – "
        # https://www.reddit.com/r/learnpython/comments/kt5zzw/how_to_speed_up_pytesseract_ocr_processing/

        top, left = utils.scaling([1850, 35])
        width, height = utils.scaling([225, 65])
        img = pyautogui.screenshot(region=(top, left, width, height))
        
        numpyImage = np.array(img)

        # Make image grayscale using opencv
        greyImage = cv2.cvtColor(numpyImage, cv2.COLOR_BGR2GRAY)

        # Threasholding
        final_image = cv2.threshold(greyImage, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
        # Get current round from image with tesseract
        text = pytesseract.image_to_string(final_image,  config='--psm 7').replace("\n", "")

        # regex to look for format [[:digit:]]/[[:digit:]] if not its not round, return None
        if re.search(r"(\d+/\d+)", text):
            text = text.split("/")
            text = tuple(map(int, text))
            return text
        else:
            return None


    def exit_bot(self):
        self.running = False

    def ingame_loop(self):
            
        current_round = -1
        ability_one_timer = time.time()
        ability_two_timer = time.time()
        game_start_time = time.time()
        
        finished = False

        middle_of_screen = self.width//2, self.height//2

        inst_idx = 0
        
        # main ingame loop
        while not finished:
            # time.sleep(0.2)
            if inst_idx < len(self.game_plan):
                current_instruction = self.game_plan[inst_idx]
            
            # Check for levelup or insta monkey (level 100)
            if self.check_levelup() or self.insta_monkey_check():
                utils.click(middle_of_screen)
                utils.click(middle_of_screen)

            # Check for finished or failed game
            if self.defeat_check() or self.victory_check():
                # DEBUG
                if self.DEBUG:
                    if self.defeat_check():
                        print("Defeat detected on round {}; exiting level".format(current_round))
                        log.log_stats(did_win=False, match_time=(time.time()-game_start_time))
                    elif self.victory_check():
                        print("Victory detected; exiting level") 
                        log.log_stats(did_win=True, match_time=(time.time()-game_start_time))
                
                self.exit_level()
                finished = True
                continue

            roundRes = self.getRound()
            if isinstance(roundRes, tuple):
                current_round, _ = roundRes 


                self.statDict["Current_Round"] = current_round

            # Saftey net; use abilites
            if current_round >= 39 and self.abilityAvaliabe(ability_one_timer, 35):
                utils.press_key("1")
                ability_one_timer = time.time()
            
            if current_round >= 51 and self.abilityAvaliabe(ability_two_timer, 90):
                utils.press_key("2")
                ability_two_timer = time.time()

            # handle current instruction when current round is equal to instruction round
            if int(current_instruction['ROUND']) == current_round and inst_idx < len(self.game_plan):
                self.handleInstruction(current_instruction)
                inst_idx += 1
                if self.DEBUG:
                    log.log("Current round", current_round)

    def handleInstruction(self, instruction):
        upgrade_path = instruction["UPGRADE_DIFF"]
    
        monkey_position = instruction["POSITION"]
        target = instruction["TARGET"]
        keybind = instruction["KEYCODE"]


        # OM det inte finns någon upgrade så finns inte tornet placera ut
        if upgrade_path == "-":
            utils.press_key(keybind)

            utils.click(monkey_position)
            self.statDict["Last_Placement"] = instruction["MONKEY"]

            if self.DEBUG:
                log.log("Tower placed:", instruction["MONKEY"])
            # press_key("esc")
        else:
            
            utils.click(monkey_position)
            upgrade_path = upgrade_path.split("-")
            top, middle, bottom = tuple(map(int, upgrade_path))
            
            for _ in range(top):
                utils.press_key(static.upgrade_keybinds["top"])

            for _ in range(middle):
                utils.press_key(static.upgrade_keybinds["middle"])

            for _ in range(bottom):
                utils.press_key(static.upgrade_keybinds["bottom"])
            
            upgrade_change = "Upgrading {} to {}; change {}".format(instruction['MONKEY'], instruction['UPGRADE'], instruction['UPGRADE_DIFF'])
            
            if self.DEBUG:
                log.log(upgrade_change)
            
            self.statDict["Last_Upgraded"] = upgrade_change
            
            utils.press_key("esc")


        # Om target är - så låt vara
        # Special case för mortar 
        if instruction["TARGET_POS"] != "-":
            pyautogui.moveTo(utils.scaling(monkey_position))
            time.sleep(0.5)
            mouse.click(button="left")

            time.sleep(1)

            pyautogui.moveTo(utils.scaling(static.button_positions["TARGET_BUTTON_MORTAR"]))
            
            time.sleep(1)
            mouse.press(button='left')
            time.sleep(0.5)
            mouse.release(button='left')

            time.sleep(1)

            pyautogui.moveTo(utils.scaling(instruction["TARGET_POS"]))
            time.sleep(0.5)
            mouse.press(button='left')
            time.sleep(0.5)
            mouse.release(button='left')

            time.sleep(1)

            utils.press_key("esc")

            # Print info
            self.statDict["Last_Target_Change"] = instruction["MONKEY"]

            if self.DEBUG:
                log.log("Monkey static target change", instruction["MONKEY"])

        if instruction["ROUND_START"] == "TRUE":
            utils.press_key("space")
            utils.press_key("space")

        # Om den har en specifik target
        if target != "-":

            if self.DEBUG:
                log.log(f"{instruction['MONKEY']} target change to {target}")

            target_array = target.split(", ")
            
            utils.click(monkey_position)

            for i in target_array:
                # press tab for the correct num of times
                for n in range(static.target_order.index(i)[0] + 1):
                    utils.press_key("tab")

                # Used for microing
                if target_array >= 1:
                    time.sleep(3) # Gör att detta specifieras i gameplan

            utils.press_key("esc")
            # special cases
            # if target == "STRONG":
            #     utils.press_key("tab")
            #     utils.press_key("tab")
            #     utils.press_key("tab")
            #     time.sleep(0.1)
            # elif len(target_array) > 1:
            #     utils.press_key("tab")
            #     time.sleep(3)
            #     utils.press_key("ctrl+tab")
            #     utils.press_key("ctrl+tab")
            # elif target == "CLOSE":
            #     utils.press_key("tab")
            
            # Print info
            self.statDict["Last_Target_Change"] = instruction["MONKEY"]

    def abilityAvaliabe(self, last_used, cooldown, fast_forward=True):
        # Möjlighet att välja beroende på ifall fast_forward är på eller ej
        m = 1
        if fast_forward:
            m = 3

        return (time.time() - last_used) >= (cooldown / m)

    
    def check_levelup(self):

        found = pyautogui.locateOnScreen(self.levelup_path, confidence=0.9)

        if found:
            print("level up detected")
            return True
        else:
            return False
        
    

    def easter_event_check(self):
        found = pyautogui.locateOnScreen(self.easter_path, confidence=0.9)
        if found != None:
            if self.DEBUG:
                log.log("easter collection detected")

            utils.button_click("EASTER_COLLECTION") #DUE TO EASTER EVENT:
            time.sleep(1)
            utils.button_click("LEFT_INSTA") # unlock insta
            time.sleep(1)
            utils.button_click("LEFT_INSTA") # collect insta
            time.sleep(1)
            utils.button_click("RIGHT_INSTA") # unlock r insta
            time.sleep(1)
            utils.button_click("RIGHT_INSTA") # collect r insta
            time.sleep(1)
            utils.button_click("F_LEFT_INSTA")
            time.sleep(1)
            utils.button_click("F_LEFT_INSTA")
            time.sleep(1)
            utils.button_click("MID_INSTA") # unlock insta
            time.sleep(1)
            utils.button_click("MID_INSTA") # collect insta
            time.sleep(1)
            utils.button_click("F_RIGHT_INSTA")
            time.sleep(1)
            utils.button_click("F_RIGHT_INSTA")
            time.sleep(1)

            time.sleep(1)
            utils.button_click("EASTER_CONTINUE")


            # awe try to click 3 quick times to get out of the easter mode, but also if easter mode not triggered, to open and close profile quick
            utils.button_click("EASTER_EXIT")
            time.sleep(1)
        
    def hero_obyn_check(self):
        found = pyautogui.locateOnScreen(self.obyn_hero_path, confidence=0.9)
        if not found:
            utils.button_click("HERO_SELECT")
            utils.button_click("SELECT_OBYN")
            utils.button_click("CONFIRM_HERO")
            utils.press_key("esc")

    def victory_check(self):
        found = pyautogui.locateOnScreen(self.victory_path, confidence=0.9)
        #jprint(victory_path)
        if found:
            return True
        else:
            return False

    def defeat_check(self):     
        #jprint(defeat_path)
        found = pyautogui.locateOnScreen(self.defeat_path, confidence=0.9)
        if found:
            return True
        else:
            return False

    def exit_level(self):
        utils.button_click("VICTORY_CONTINUE")
        time.sleep(2)
        utils.button_click("VICTORY_HOME")
        time.sleep(4)

        self.easter_event_check()
        time.sleep(2)

    def select_map(self):
        time.sleep(2)

        utils.button_click("HOME_MENU_START") # Move Mouse and click from Home Menu, Start
        utils.button_click("EXPERT_SELECTION") # Move Mouse to expert and click
        utils.button_click("RIGHT_ARROW_SELECTION") # Move Mouse to arrow and click
        utils.button_click("DARK_CASTLE") # Move Mouse to Dark Castle
        utils.button_click("HARD_MODE") # Move Mouse to select easy mode
        utils.button_click("CHIMPS_MODE") # Move mouse to select Standard mode
        utils.button_click("OVERWRITE_SAVE") # Move mouse to overwrite save if exists
        time.sleep(3)
        utils.button_click("CONFIRM_CHIMPS")

    def menu_check(self):
        #jprint(menu_path)
        found = pyautogui.locateOnScreen(self.menu_path, confidence=0.9)
        if found:
            return True
        else:
            return False

    def insta_monkey_check(self):
        found = pyautogui.locateOnScreen(self.insta_monkey, confidence=0.9)
        if found: 
            return True
        else:
            return False

    def __fixCordinates(self, posString):
        """
            Converts x, y, ... to a tuple with an int
        """
        fixed = posString.split(", ")

        return tuple(map(int, fixed))

    def __load_data(self, file_path):
        formatedInstructions = []
        with open(file_path) as file:
            csvreader = csv.DictReader(file)
            
            for row in csvreader:
                row["POSITION"] = self.__fixCordinates(row["POSITION"])

                if row["TARGET_POS"] != "-":
                    row["TARGET_POS"] = self.__fixCordinates(row["TARGET_POS"])
                
                
                formatedInstructions.append(row)
        return formatedInstructions
        # pprint(formatedInstructions)


