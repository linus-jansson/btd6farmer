from ast import arg
import os, csv, re, time
from pstats import Stats
from pydoc import cli
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import cv2
import numpy as np

import pyautogui, mouse, keyboard
pyautogui.FAILSAFE = True # When mouse is moved to top left, program will exit



current_directory = os.getcwd() + "\\"
width, height = pyautogui.size()
levelup_path = current_directory + "Support_Files\\" + str(height) + "_levelup.png"
victory_path = current_directory + "Support_Files\\" + str(height) + "_victory.png"
defeat_path = current_directory + "Support_Files\\" + str(height) + "_defeat.png"
menu_path = current_directory + "Support_Files\\" + str(height) + "_menu.png"
easter_path = current_directory + "Support_Files\\" + str(height) + "_easter.png"
obyn_hero_path = current_directory + "Support_Files\\" + str(height) + "_obyn.png"
insta_monkey = current_directory + "Support_Files\\" + str(height) + "_instamonkey.png"

DEBUG = True
start_time = time.time()
running = True

button_positions = { # Creates a dictionary of all positions needed for monkeys (positions mapped to 2160 x 1440 resolution)
    "HOME_MENU_START" : [1123, 1248],
    "EXPERT_SELECTION" : [1778, 1304],
    "RIGHT_ARROW_SELECTION" : [2193, 582],
    "DARK_CASTLE" : [1420, 350], # changed to (x=1941, y=513) in latest patch
    "HARD_MODE" : [1729, 562],
    "CHIMPS_MODE" : [2139, 980],
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
    "ABILLITY_ONE": [253, 1379],
    "ABILLITY_TWO": [369, 1377],
    "FREEPLAY" : [1611, 1112],
    "OK_MIDDLE" : [1280, 1003],
    "RESTART": [1413, 1094],
    "CONFIRM_CHIMPS" : [1481, 980]

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

reso_16 = [
    {
        "width": 1280,
        "height": 720        
    },
    {
        "width": 1920,
        "height": 1080
    },
    {
        "width": 2560,
        "height": 1440
    },
    {
        "width": 3840,
        "height": 2160
    }
]

statDict = {
    "Current_Round": None,
    "Last_Upgraded": None,
    "Last_Target_Change": None,
    "Last_Placement": None,
    "Uptime": 0
}

def handle_time(ttime):
    """
        Converts seconds to appropriate unit
    """
    if ttime >= 60: # Minutes
        return (ttime / 60, "min")
    elif (ttime / 60) >= 60: # Hours
        return (ttime / 3600, "hrs")
    elif (ttime / 3600) >= 24: # days
        return (ttime / 86400, "d")
    elif (ttime / 86400) >= 7: # Weeks
        return (ttime / 604800, "w")
    else: # No sane person will run this bokk for a week
        return (ttime, "s")

import json
def log_stats(did_win: bool = None, match_time: int | float = 0):
    # Standard dict which will be used if json loads nothing
    data = {"wins": 0, "loses": 0, "winrate": "0%", "average_matchtime": "0 s", "total_time": 0, "average_matchtime_seconds": 0}
    
    # Try to read the file
    try:
        with open("stats.json", "r") as infile:
            try:
                # Read json file
                str_file = "".join(infile.readlines())
                data = json.loads(str_file)
            # Catch if file format is invalid for json (eg empty file)
            except json.decoder.JSONDecodeError:
                print("invalid stats file")
    # Catch if the file does not exist
    except IOError:
        print("file does not exist")

    # Open as write
    with open("stats.json", "w") as outfile:        
        if did_win:
            data["wins"] += 1
        else:
            data["loses"] += 1
        
        total_matches = (data["wins"] + data["loses"])
        # winrate = total wins / total matches
        winrate = data["wins"] / total_matches

        # Convert to procent
        procentage = (round(winrate * 100, 4))
        
        # Push procentage to winrate
        data["winrate"] = f"{procentage}%"

        data["average_matchtime_seconds"] = (data["total_time"]  + match_time) / total_matches
        
        # new_total_time = old_total_time + current_match_time in seconds
        data["total_time"] += match_time
        
        # average = total_time / total_matches_played
        average_converted, unit = handle_time(data["average_matchtime_seconds"])
        
        # Push average to dictionary
        data["average_matchtime"] = f"{round(average_converted, 3)} {unit}"

        outfile.write(json.dumps(data, indent=4))

# import random
# for i in range(5):

#     start_time = time.time()
#     # random sleep between 10 and 20 seconds
#     time.sleep(random.randint(150, 250))

#     log_stats(did_win=random.randint(0, 1), match_time=(time.time()-start_time))

# exit()




def printStats(stats):
    os.system("cls")
    print("="*6)
    if round(time.time() - start_time, 2) >= 60.0:
        stats["Uptime"] = "{} minutes".format(round( (time.time() - start_time) / 60, 2)  )
    elif round(time.time() - start_time, 2) / 60 >= 60.0:
        stats["Uptime"] = "{} hours".format(round( (time.time() - start_time) / 60 / 60, 2) )
    else:
        stats["Uptime"] = "{} seconds".format(round(time.time() - start_time, 2))
    
    for key, value in stats.items():
        print(f"{key.replace('_', ' ')}\t{value}")
    print("="*6)

def padding():
# Get's width and height of current resolution
# we iterate through reso_16 for heights, if current resolution height matches one of the entires 
# then it will calulate the difference of the width's between current resolution and 16:9 (reso_16) resolution
# divides by 2 for each side of padding

# Variables Used
#   width -- used to referance current resolution width
#   height -- used to referance current resolution height
#   pad -- used to output how much padding we expect in different resolutions
#   reso_16 -- list that  
    width, height = pyautogui.size()
    pad = 0
    for x in reso_16: 
        if height == x['height']:
            pad = (width - x['width'])/2
    #print("I have been padding -- " + str(pad))

    # DEBBUGGING
    return pad

def scaling(pos_list):
# This function will dynamically calculate the differance between current resolution and designed for 2560x1440
# it will also add any padding needed to positions to account for 21:9 

# do_padding -- this is used during start 
    reso_21 = False
    width, height = pyautogui.size()
    for x in reso_16: 
        if height == x['height']:
            if width != x['width']:
                reso_21 = True
                x = pos_list[0]
                break
    if reso_21 != True:
        x = pos_list[0]/2560 
        x = x * width
    y = pos_list[1]/1440
    y = y * height
    #print(" Me wihout padding " + str([x]))
    x = x + padding() # Add's the pad to to the curent x position variable
    #print(" Me with padding -- " + str([x]))
    return (x, y)



def move_mouse(location):
    pyautogui.moveTo(location)
    time.sleep(0.1)

def click(location): #pass in x and y, and it will click for you
    #print(location)
    # mouse.move(*scaling(button_positions[location]))
    # x, y = location
    # mouse.move(*location)
    move_mouse(scaling(location))
    mouse.click(button="left") # performs the pyautogui click function while passing in the variable from button_positions that matches button
    time.sleep(0.5)

def button_click(btn):
    #print(location)
    # x, y = location
    # mouse.move(*location)
    move_mouse(scaling(button_positions[btn]))
    mouse.click(button="left") # performs the pyautogui click function while passing in the variable from button_positions that matches button
    time.sleep(0.5)

def press_key(key):
    keyboard.send(key)
    time.sleep(0.1)

def getRound():
    top, left = scaling([1850, 35])
    width, height = scaling([225, 65])
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
    upgrade_path = instruction["UPGRADE_DIFF"]
    
    monkey_position = instruction["POSITION"]
    target = instruction["TARGET"]
    keybind = instruction["KEYCODE"]


    # OM det inte finns någon upgrade så finns inte tornet placera ut
    if upgrade_path == "-":
        press_key(keybind)

        click(monkey_position)
        statDict["Last_Placement"] = instruction["MONKEY"]
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
        
        statDict["Last_Upgraded"] = "Upgrading {} to {}; change {}".format(instruction['MONKEY'], instruction['UPGRADE'], instruction['UPGRADE_DIFF'])
        press_key("esc")


    # Om target är - så låt vara
    # Special case för mortar 
    if instruction["TARGET_POS"] != "-":
        pyautogui.moveTo(scaling(monkey_position))
        time.sleep(0.5)
        mouse.click(button="left")

        time.sleep(1)

        pyautogui.moveTo(scaling(button_positions["TARGET_BUTTON_MORTAR"]))
        
        time.sleep(1)
        mouse.press(button='left')
        time.sleep(0.5)
        mouse.release(button='left')

        time.sleep(1)

        pyautogui.moveTo(scaling(instruction["TARGET_POS"]))
        time.sleep(0.5)
        mouse.press(button='left')
        time.sleep(0.5)
        mouse.release(button='left')

        time.sleep(1)

        press_key("esc")

        # Print info
        statDict["Last_Target_Change"] = instruction["MONKEY"]

    if instruction["ROUND_START"] == "TRUE":
        press_key("space")
        press_key("space")


        # Om den har en specifik target
    if target != "-":
        splitTarget = target.split(", ")

        # special cases
        if target == "STRONG":
            click(monkey_position)
            press_key("tab")
            press_key("tab")
            press_key("tab")
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
        
        # Print info
        statDict["Last_Target_Change"] = instruction["MONKEY"]


def check_levelup():

    found = pyautogui.locateOnScreen(levelup_path, confidence=0.9)

    if found:
        print("level up detected")
        return True
    else:
        return False
        
    

def easter_event_check():
    found = pyautogui.locateOnScreen(easter_path, confidence=0.9)
    if found != None:
        print("easter collection detected")
        button_click("EASTER_COLLECTION") #DUE TO EASTER EVENT:
        time.sleep(1)
        button_click("LEFT_INSTA") # unlock insta
        time.sleep(1)
        button_click("LEFT_INSTA") # collect insta
        time.sleep(1)
        button_click("RIGHT_INSTA") # unlock r insta
        time.sleep(1)
        button_click("RIGHT_INSTA") # collect r insta
        time.sleep(1)
        button_click("F_LEFT_INSTA")
        time.sleep(1)
        button_click("F_LEFT_INSTA")
        time.sleep(1)
        button_click("MID_INSTA") # unlock insta
        time.sleep(1)
        button_click("MID_INSTA") # collect insta
        time.sleep(1)
        button_click("F_RIGHT_INSTA")
        time.sleep(1)
        button_click("F_RIGHT_INSTA")
        time.sleep(1)

        time.sleep(1)
        button_click("EASTER_CONTINUE")


        # awe try to click 3 quick times to get out of the easter mode, but also if easter mode not triggered, to open and close profile quick
        button_click("EASTER_EXIT")
        time.sleep(1)
        
def hero_obyn_check():
    found = pyautogui.locateOnScreen(obyn_hero_path, confidence=0.9)
    if not found:
        button_click("HERO_SELECT")
        button_click("SELECT_OBYN")
        button_click("CONFIRM_HERO")
        press_key("esc")

def victory_check():
    found = pyautogui.locateOnScreen(victory_path, confidence=0.9)
    #jprint(victory_path)
    if found:
        return True
    else:
        return False

def defeat_check():     
    #jprint(defeat_path)
    found = pyautogui.locateOnScreen(defeat_path, confidence=0.9)
    if found:
        return True
    else:
        return False

def exit_level():
    button_click("VICTORY_CONTINUE")
    time.sleep(2)
    button_click("VICTORY_HOME")
    time.sleep(4)

    easter_event_check()
    time.sleep(2)

def select_map():
    time.sleep(2)

    button_click("HOME_MENU_START") # Move Mouse and click from Home Menu, Start
    button_click("EXPERT_SELECTION") # Move Mouse to expert and click
    button_click("RIGHT_ARROW_SELECTION") # Move Mouse to arrow and click
    button_click("DARK_CASTLE") # Move Mouse to Dark Castle
    button_click("HARD_MODE") # Move Mouse to select easy mode
    button_click("CHIMPS_MODE") # Move mouse to select Standard mode
    button_click("OVERWRITE_SAVE") # Move mouse to overwrite save if exists
    time.sleep(3)
    button_click("CONFIRM_CHIMPS")

def menu_check():
    #jprint(menu_path)
    found = pyautogui.locateOnScreen(menu_path, confidence=0.9)
    if found:
        return True
    else:
        return False

def insta_monkey_check():
    found = pyautogui.locateOnScreen(insta_monkey, confidence=0.9)
    if found: 
        return True
    else:
        return False

def abilityAvaliabe(last_used, cooldown, fast_forward=True):
    # Möjlighet att välja beroende på ifall fast_forward är på eller ej
    m = 1
    if fast_forward:
        m = 3

    return (time.time() - last_used) >= (cooldown / m)

def main_game(instructions):
    
    current_round = -1
    ability_one_timer = time.time()
    ability_two_timer = time.time()
    
    finished = False

    width, height = pyautogui.size()
    middle_of_screen = width//2, height//2

    inst_idx = 0
    
    # main ingame loop
    while not finished:
        # time.sleep(0.2)
        if inst_idx < len(instructions):
            current_instruction = instructions[inst_idx]
        
        # Check for levelup or insta monkey (level 100)
        if check_levelup() or insta_monkey_check():
            click(middle_of_screen)
            click(middle_of_screen)

        # Check for finished or failed game
        if defeat_check() or victory_check():
            # DEBUG
            if defeat_check():
                print("Defeat detected on round {}; exiting level".format(current_round))
                if DEBUG:
                    log_stats(did_win=False)
            elif victory_check():
                print("Victory detected; exiting level")    
                if DEBUG:
                    log_stats(did_win=True)
            
            exit_level()
            finished = True
            continue

        if getRound():
            current_round, _ = getRound()
            statDict["Current_Round"] = current_round

        # Saftey net; use abilites
        if current_round >= 39 and abilityAvaliabe(ability_one_timer, 35):
            press_key("1")
            ability_one_timer = time.time()
        
        if current_round >= 51 and abilityAvaliabe(ability_two_timer, 90):
            press_key("2")
            ability_two_timer = time.time()

        # handle current instruction when current round is equal to instruction round
        if int(current_instruction['ROUND']) == current_round and inst_idx < len(instructions):
            handleInstruction(current_instruction)
            inst_idx += 1

def exit_bot():
    global running
    print("Exit key pressed. Goodbye!")
    printStats(statDict)
    running = False
    exit()


def main():

    print("waiting for 5 seconds, please select the btd 6 window")
    time.sleep(5)
    # Check for obyn
    fixed_instructions = formatData()

    keyboard.add_hotkey("f11", printStats, args=[statDict])
    keyboard.add_hotkey("ctrl+q", exit_bot) # Not working use pyautogui failsafe instead

    while running:
        print("selecting map")
        
        # Prevent alt+tab bug from happening
        press_key("alt")

        # Choose map
        select_map()   

        print("Game start")
        # main game
        main_game(fixed_instructions)
        # statDict["Won_Games"] += won
        # statDict["Lost_Games"] += lost



if __name__ == "__main__":
    main()