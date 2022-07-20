import sys
import pyautogui
import time
import keyboard
import mouse
import static
import os

import numpy as np
import cv2
import pytesseract
import re

class BotUtils:
    def __init__(self):
        self.Support_files_path = "Support_files\\" if sys.platform == "win32" else "Support_files/"

        # defining the paths to the images needed in the bot
        self.__levelup_path = f"{self.Support_files_path}{str(self.height)}_levelup.png"
        self.__victory_path = f"{self.Support_files_path}{str(self.height)}_victory.png"
        self.__defeat_path = f"{self.Support_files_path}{str(self.height)}_defeat.png"
        self.__main_menu_path = f"{self.Support_files_path}{str(self.height)}_menu.png"
        self.__insta_monkey_path = f"{self.Support_files_path}{str(self.height)}_instamonkey.png"
        self.__collection_event_path = f"{self.Support_files_path}{str(self.height)}_diamond_case.png"
        

        self.__hero_path = lambda self, herostring : f"{self.Support_files_path}{str(self.height)}_{herostring}.png"

        self.__set_target_path = f"{self.Support_files_path}{str(self.height)}_set_target_path.png"

        # Resolutions for for padding
        self.reso_16 = [
            { "width": 1280, "height": 720  },
            { "width": 1920, "height": 1080 },
            { "width": 2560, "height": 1440 },
            { "width": 3840, "height": 2160 }
        ]

        self.width, self.height = pyautogui.size()


    def getRound(self):
        # Change to https://stackoverflow.com/questions/66334737/pytesseract-is-very-slow-for-real-time-ocr-any-way-to-optimise-my-code 
        # or https://www.reddit.com/r/learnpython/comments/kt5zzw/how_to_speed_up_pytesseract_ocr_processing/

        top, left = self._scaling([1850, 35])
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

    def __move_mouse(self, location):
        pyautogui.moveTo(location)
        time.sleep(0.1)

    def click(self, location: tuple | tuple, amount=1):
        """
            Method to click on a specific location on the screen
        """

        # If location is a string then assume that its a static button
        if isinstance(location, str):
            location = static.button_positions[location]
        
        # Move mouse to location
        self.__move_mouse(self._scaling(location))

        for _ in range(amount):
            mouse.click(button="left")
            time.sleep(0.1)

        time.sleep(0.5)

    def press_key(self, key, timeout=0.1, amount=1):
        for _ in range(amount):
            keyboard.send(key)

        time.sleep(timeout)

    # TODO: Stop using pyautogui
    # Generic function to see if something is present on the screen
    def __find(self, path, confidence=0.9, return_cords=False):
        if return_cords:
            cords = pyautogui.locateOnScreen(path, confidence=confidence)
            if cords is not None:
                left, top, width, height = cords
                return (left + width // 2, top + height // 2) # Return middle of found image   
            else:
                return None

        return True if pyautogui.locateOnScreen(path, confidence=confidence) is not None else False

    # Different methods for different checks all wraps over __find()
    def menu_check(self):
        return self.__find(self.__main_menu_path)

    def insta_monkey_check(self):
        return self.__find(self.__insta_monkey_path)

    def victory_check(self):
        return self.__find(self.__victory_path)

    def defeat_check(self):
        return self.__find(self.__defeat_path)

    def levelup_check(self):
        return self.__find(self.__levelup_path)

    def hero_check(self, heroString):
        return self.__find( self.__hero_path(heroString) )

    def collection_event_check(self):
        return self.__find(self.__collection_event_path)

    def locate_static_target_button(self):
        return self.__find(self.__set_target_path, return_cords=True)


    # Scaling functions for different resolutions support
    def _scaling(self, pos_list):
        """
            This function will dynamically calculate the differance between current resolution and designed for 2560x1440
            it will also add any padding needed to positions to account for 21:9 

            do_padding -- this is used during start 
        """

        reso_21 = False
        for x in self.reso_16: 
            if self.height == x['height']:
                if self.width != x['width']:
                    reso_21 = True
                    x = pos_list[0]
                    break

        if reso_21 != True:
            x = pos_list[0]/2560 
            x = x * self.width
        
        y = pos_list[1]/1440
        y = y * self.height
        x = x + self.__padding() # Add's the pad to to the curent x position variable

        return (x, y)

    def __padding(self):
        """
            Get's width and height of current resolution
            we iterate through reso_16 for heights, if current resolution height matches one of the entires 
            then it will calulate the difference of the width's between current resolution and 16:9 (reso_16) resolution
            divides by 2 for each side of padding

            Variables Used
            width -- used to referance current resolution width
            height -- used to referance current resolution height
            pad -- used to output how much padding we expect in different resolutions
            reso_16 -- list that  
        """

        padding = 0
        for x in self.reso_16: 
            if self.height == x['height']:
                padding = (self.width - x['width'])/2

        return padding

    def get_resource_file(path):
        return os.path.join(os.path.dirname(__file__), path)
