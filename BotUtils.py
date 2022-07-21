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
        self.width, self.height = pyautogui.size()

        self.Support_files_path = "Support_files\\" if sys.platform == "win32" else "Support_files/"
        
        self.support_dir = self.get_resource_dir(self.Support_files_path)

        # Defing a lamda function that can be used to get a path to a specific image
    
        self.__image_path = lambda image, root_dir=self.support_dir, height=self.height : f"{root_dir}{height}_{image}.png" if sys.platform == "win32" else f"{root_dir}{height}_{image}.png"

        # Resolutions for for padding
        self.reso_16 = [
            { "width": 1280, "height": 720  },
            { "width": 1920, "height": 1080 },
            { "width": 2560, "height": 1440 },
            { "width": 3840, "height": 2160 }
        ]

    def get_resource_dir(self, path):
        return os.path.join(os.path.dirname(__file__), path)

    def getRound(self):
        # Change to https://stackoverflow.com/questions/66334737/pytesseract-is-very-slow-for-real-time-ocr-any-way-to-optimise-my-code 
        # or https://www.reddit.com/r/learnpython/comments/kt5zzw/how_to_speed_up_pytesseract_ocr_processing/

        top, left = self._scaling([1850, 35])
        width, height = [225, 65]
        
        # TODO: change to mss
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
            mouse.press(button='left')
            time.sleep(0.075) # https://www.reddit.com/r/AskTechnology/comments/4ne2tv/how_long_does_a_mouse_click_last/ TLDR; DONT CLICK TO FAST as shit will break
            mouse.release(button='left')
            # mouse.click(button="left")
            

        time.sleep(0.5)

    def press_key(self, key, timeout=0.1, amount=1):
        for _ in range(amount):
            keyboard.send(key)

        time.sleep(timeout)

    # TODO: Stop using pyautogui
    def locate(self, template_path, confidence=0.9, tries=1):
        """
            Method to match a template to a image.
            
            @template_path - Path to the template image
            @confidence - A threshold value between {> 0.0f & < 1.0f} (Defaults to 0.9f)

            Returns a list of cordinates to where openCV found matches of the template on the screenshot taken
        """
        # sc tool: https://pypi.org/project/mss/

        # Take a screenshot of the screen and save to a temporary variable
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        # using opencv, find the img on the screen using the template

        template = cv2.imread(template_path)
        template = np.array(template)
        
        # width & height of the template
        w = template.shape[0]
        h = template.shape[1]
        
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)    # heatmap of the template and the screenshot"

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result) # find the max value and location of the heatmap
        
        cv2.rectangle(screenshot, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 0, 255), 1) # draw on image for debugging

        # Find all the matches
        locations = np.where(result >= confidence) 
        
        print(f"max_loc {max_loc}, max_val {max_val}")
        # print(f"threshold {confidence}, template match result -> \n {result}")
        print(f"len(yloc) = {len(locations[0])}, \nlen(xloc) = {len(locations[1])}, \nlista på kordinater: {[ [x,y] for x, y in zip(*locations[::-1]) ]}") # längden och listan på resulterande kordinater
    
        # DBUG: ritar ut rektanglar på bild objektet
        # VARFÖR RITAR DEN BARA UT EN REKTANGEL? på fel ställe??????
        # for x, y in zip(*locations[::-1]):
        #     cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 0, 255), 1)

        # Visar bild objektet med utritad rektangel
        self.debug_result(screenshot, template, result)

        # return the cords of the image if found (middle by default) else None
        if locations is not None:
            return [ (x, y, w, h) for x, y, w, h in zip(*locations[::-1]) ]
        else:
            return None
    
    def debug_result(self, imgObj, templateObj, result):
        # cv2.imshow("resulting heatmap of image and template", result) # DEBUG

        cv2.imshow("Image", imgObj)
        # cv2.imshow("Template", templateObj)

        cv2.waitKey()
        cv2.destroyAllWindows()

    # Generic function to see if something is present on the screen
    def __find(self, path, confidence=0.9, return_cords=False):
        try:
            if return_cords:
                cords = pyautogui.locateOnScreen(path, confidence=confidence)
                if cords is not None:
                    left, top, width, height = cords
                    return (left + width // 2, top + height // 2) # Return middle of found image   
                else:
                    return None

            return True if pyautogui.locateOnScreen(path, confidence=confidence) is not None else False
        except Exception as e:
            raise Exception(e)

    # Different methods for different checks all wraps over __find()
    def menu_check(self):
        return self.__find( self.__image_path("menu") )

    def insta_monkey_check(self):
        return self.__find( self.__image_path("instamonkey") )

    def victory_check(self):
        return self.__find( self.__image_path("victory") )

    def defeat_check(self):
        return self.__find( self.__image_path("defeat") )

    def levelup_check(self):
        return self.__find( self.__image_path("levelup") )

    def hero_check(self, heroString):
        return self.__find( self.__image_path(heroString)  )

    def collection_event_check(self):
        return self.__find(self.__image_path("diamond_case") )

    def locate_static_target_button(self):
        return self.__find(self.__image_path("set_target_button"), return_cords=True)


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



if __name__ == "__main__":
    import time

    inst = BotUtils()
    print("sleeping for 5 secs")
    time.sleep(5)
    

    res = inst.locate(inst.print_hero('obyn'))
    print(res)