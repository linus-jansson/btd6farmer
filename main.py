from dis import Instruction
import queue
from turtle import position
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import cv2
import numpy as np
import pyautogui
import time
import csv

import threading
import re

import mouse, keyboard
from collections import defaultdict

from pprint import pprint



"""
Bloons td 6 bot which farms datk castle on chimps mode

Made for 2560x1440

TODO: 
- 1080p support

"""

button_positions = { # Creates a dictionary of all positions needed for monkeys (positions mapped to 2160 x 1440 resolution)
    "HOME_MENU_START" : [1123, 1248],
    "EXPERT_SELECTION" : [1778, 1304],
    "RIGHT_ARROW_SELECTION" : [2193, 582],
    "DARK_CASTLE" : [1420, 350], # changed to (x=1941, y=513) in latest patch
    "HARD_MODE" : [],
    "CHIMPS_MODE" : [],
    "STANDARD_GAME_MODE" : [847,780],
    "OVERWRITE_SAVE" : [1520, 974],
    "VICTORY_CONTINUE" : [1283, 1215],
    "VICTORY_HOME" : [939, 1124],
    "EASTER_COLLECTION" : [1279, 911],
    "F_LEFT_INSTA" : [868, 722],
    "F_RIGHT_INSTA" : [1680, 722],
    "LEFT_INSTA" : [1074, 725],
    "RIGHT_INSTA" : [1479, 724],
    "MID_INSTA" : [1276, 727],
    "EASTER_CONTINUE" : [1280, 1330],
    "EASTER_EXIT" : [100, 93],
    "QUIT_HOME" : [1126, 1135],
    "HERO_SELECT" : [799, 1272],
    "SELECT_OBYN" : [],
    "CONFIRM_HERO" : [855, 893],
    "TARGET_BUTTON_MORTAR": [1909, 491],
}



monkeys = {
    "DART" : "q",
    "BOOMERANG" : "w",
    "BOMB" : "e",
    "TACK" : "r",
    "ICE" : "t",
    "GLUE" : "y",
    "SNIPER" : "z",
    "SUBMARINE" : "x",
    "BUCCANEER" : "c",
    "ACE" : "v",
    "HELI" : "b",
    "MORTAR" : "n",
    "DARTLING" : "m",
    "WIZARD" : "a",
    "SUPER" : "s",
    "NINJA" : "d",
    "ALCHEMIST" : "f",
    "DRUID" : "g",
    "BANANA" : "h",
    "ENGINEER" : "l",
    "SPIKE" : "j",
    "VILLAGE" : "k",
    "HERO" : "u"
}

upgrade_keybinds = {
    "top" : ",",
    "middle" : ".",
    "bottom" : "/"

}

def move_mouse(location):
    pyautogui.moveTo(location)
    time.sleep(0.1)

def click(location): #pass in x and y, and it will click for you
    #print(location)
    # mouse.move(*scaling(button_positions[location]))
    # x, y = location
    # mouse.move(*location)
    move_mouse(location)
    mouse.click(button="left") # performs the pyautogui click function while passing in the variable from button_positions that matches button
    time.sleep(0.5)

def press_key(key):
    keyboard.press_and_release(key)
    time.sleep(0.1)

def getRound():
    img = pyautogui.screenshot(region=(1900, 35, 175, 65))
    
    numpyImage = np.array(img)

    # Make image grayscale using opencv
    greyImage = cv2.cvtColor(numpyImage, cv2.COLOR_BGR2GRAY)

    # Threasholding
    final_image = cv2.threshold(greyImage, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
   
    # Get current round from image with tesseract
    text = pytesseract.image_to_string(final_image,  config='--psm 7').replace("\n", "")

    # regex to look for format [[:digit:]]/[[:digit:]] if not its not round, return None
    if re.search(r"(\d+/\d+)", text):
        return text
    else:
        return None


# Fixar om cordinater till sträng
def fixPositionFormated(posString):
    fixed = posString.split(", ")

    return tuple(map(int, fixed))


def formatData():
    formatedInstructions = []
    with open("instructions.csv") as file:
        csvreader = csv.DictReader(file)
        
        for row in csvreader:
            row["POSITION"] = fixPositionFormated(row["POSITION"])

            if row["TARGET_POS"] != "-":
                row["TARGET_POS"] = fixPositionFormated(row["TARGET_POS"])
            
            
            formatedInstructions.append(row)
    return formatedInstructions
    # pprint(formatedInstructions)

def handleInstruction(instruction):
    # print(instruction)
    upgrade_path = instruction["UPGRADE_DIFF"]
    
    monkey_position = instruction["POSITION"]
    target = instruction["TARGET"]
    keybind = instruction["KEYCODE"]


    # OM det inte finns någon upgrade så finns inte tornet placera ut
    if upgrade_path == "-":
        press_key(keybind)

        click(monkey_position)
        # press_key("esc")
    else:
        click(monkey_position)
        upgrade_path = upgrade_path.split("-")
        top, middle, bottom = tuple(map(int, upgrade_path))
        
        for _ in range(top):
            press_key(upgrade_keybinds["top"])

        for _ in range(middle):
            press_key(upgrade_keybinds["middle"])

        for _ in range(bottom):
            press_key(upgrade_keybinds["bottom"])

        
        print(instruction["MONKEY"], instruction["UPGRADE"], "diff -", instruction["UPGRADE_DIFF"])

        press_key("esc")


    # Om target är - så låt vara
    # Special case för mortar 
    if instruction["TARGET_POS"] != "-":
        print("clicka på mortar")
        
        pyautogui.moveTo(monkey_position)
        time.sleep(0.5)
        mouse.click(button="left")

        time.sleep(1)

        pyautogui.moveTo(button_positions["TARGET_BUTTON_MORTAR"])
        
        time.sleep(1)
        mouse.press(button='left')
        time.sleep(0.5)
        mouse.release(button='left')

        time.sleep(1)

        pyautogui.moveTo(instruction["TARGET_POS"])
        time.sleep(0.5)
        mouse.press(button='left')
        time.sleep(0.5)
        mouse.release(button='left')

        time.sleep(1)

        press_key("esc")

    if instruction["ROUND_START"] == "TRUE":
        press_key("space")
        press_key("space")


        # Om den har en specifik target
    if target != "-":
        splitTarget = target.split(", ")

        # special cases
        if target == "STRONG":
            click(monkey_position)
            press_key("ctrl+tab")
            press_key("esc")
        elif len(splitTarget) > 1:
            click(monkey_position)
            press_key("tab")
            time.sleep(3)
            press_key("ctrl+tab")
            press_key("ctrl+tab")
            press_key("esc")
        elif target == "CLOSE":
            click(monkey_position)
            press_key("tab")            
            press_key("esc")

        

def main_game(instructions):
    # uppdelade_upgrades_per_apa = defaultdict(dict)
    # # delar upp alla upgraderingar för sig per apa
    # for idx, instruction in enumerate(instructions):
    #     if instruction["UPGRADE"] != "-":
    #         if len(uppdelade_upgrades_per_apa[instruction["MONKEY"]]) > 0:
    #             uppdelade_upgrades_per_apa[instruction["MONKEY"]].append(instruction["UPGRADE"])
                
    #         else: 
    #             uppdelade_upgrades_per_apa[instruction["MONKEY"]] = [ instruction["UPGRADE"] ]

    # # För varje upgrade per apa
    # for monkey_upgrade in uppdelade_upgrades_per_apa.values():
    #     if len(monkey_upgrade) > 1: # Hoppa ifall det bara är en upgrade på den apan
    #         for index in range(len(monkey_upgrade)): # ifall index av listan är 0 hoppa
    #             if index != 0:
    #                 # Senaste och nuvarande uppgradeing splitar ut alla -
    #                 last_upgrade = monkey_upgrade[index -1].split("-")
    #                 upgrade = monkey_upgrade[index].split("-")

    #                 # mappar om str till int i upgrade listorna
    #                 top_last, middle_last, bottom_last = tuple(map(int, last_upgrade))
    #                 top, middle, bottom = tuple(map(int, upgrade))

    #                 # Hittar diffen mellan förra uppgradering och nuvarande uppgraderingen
    #                 diff = "{}-{}-{}".format(abs(top-top_last), abs(middle-middle_last), abs(bottom-bottom_last))
                    
    #                 print(last_upgrade, upgrade, diff)
                    
    #                 # Ändrar monkey_upgrade
    #                 monkey_upgrade[index] = diff

    # pprint(instructions)
    # pprint(uppdelade_upgrades_per_apa)
    # exit()
    # Loopa oändligt
    print(instructions)
    # tmp_instructions = instructions

    while True:
        current_round = None
        # if currentRound:
        #     currentRound = currentRound.split("/")[0]
        # Gå igenom alla instructions

        queue = []

        if len(instructions) <= 0:
            continue
        else:
            # instructions[:] 
           
            # for idx, inst in enumerate(instructions[:]):
            #     print(inst, len(instructions))
                
            #     while cr == getRound():
            #         print(cr, getRound())
            #         continue
            #     else:
                    
            #         cr = getRound()
            #         handleInstruction(inst)


            #     instructions.remove(inst)

            # VÄLDIGT VIKTIGT https://stackoverflow.com/questions/10665591/how-to-remove-list-elements-in-a-for-loop-in-python#10665602 
            for inst in instructions[:]:
                while f"{inst['ROUND']}/100" != current_round:
                    print("waiting", current_round)
                    time.sleep(0.2)
                    current_round = getRound()
                    continue
                else:
                    handleInstruction(inst)

                    if getRound() == "40/100":
                        press_key('1')
                    elif getRound == "50/100":
                        press_key('2')
                    


        # Sov en stund för att inte crasha allt
        time.sleep(1)

def main():

    print("waiting for 5 seconds, please select the btd 6 window")
    time.sleep(5)
    # Check for obyn

    # print(getRound())
    fixed_instructions = formatData()
    main_game(fixed_instructions)



if __name__ == "__main__":
    main()