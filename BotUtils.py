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
import mss

import ctypes

class BotUtils:
    def __init__(self):
        # Gets the main monitor resolution
        try:
            if sys.platform == "win32":
                self.width, self.height = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
            else:
                raise Exception("Platform not supported yet")
        except Exception as e:
            raise Exception("Could not retrieve monitor resolution the system")
        # finally: 
        #     if self.DEBUG:
        #         self.log(f"Monitor resolution: {self.width}x{self.height}")
        

        self.Support_files_path = "Support_files\\" if sys.platform == "win32" else "Support_files/"
        
        self.support_dir = self.get_resource_dir(self.Support_files_path)

        # Defing a lamda function that can be used to get a path to a specific image
    
        self._image_path = lambda image, root_dir=self.support_dir, height=self.height : f"{root_dir}{height}_{image}.png" if sys.platform == "win32" else f"{root_dir}{height}_{image}.png"

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

        # The screen part to capture
        top, left = self._scaling([35, 1850])
        width, length = [225, 65]
        
        monitor = {'top': top, 'left': left, 'width': width, 'height': length}
        # print("region", monitor)

        # Take Screenshot
        with mss.mss() as sct:
            screenshot = np.array(sct.grab(monitor), dtype=np.uint8)
            
            # Load the image as a opencv object
            gray_scale_image = self._load_img(screenshot) 

            # https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
            # We do this to hopefully improve the OCR accuracy
            final_image = cv2.threshold(gray_scale_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            # Get current round from screenshot with tesseract
            found_text = pytesseract.image_to_string(final_image,  config='--psm 7').replace("\n", "")

            if self.DEBUG:
                print(f"Found round text: {found_text}")  
                # cv2.imshow("Screenshot image", screenshot)


            if re.search(r"(\d+/\d+)", found_text):
                return int(found_text.split("/")[0])
            else:
                return None

    def _move_mouse(self, location):
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
        self._move_mouse(self._scaling(location))

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

    # Different methods for different checks all wraps over _find()
    def menu_check(self):
        return self._find( self._image_path("menu") )

    def insta_monkey_check(self):
        return self._find( self._image_path("instamonkey") )

    def victory_check(self):
        return self._find( self._image_path("victory") )

    def defeat_check(self):
        return self._find( self._image_path("defeat") )

    def levelup_check(self):
        return self._find( self._image_path("levelup") )

    def hero_check(self, heroString):
        return self._find( self._image_path(heroString)  )

    def collection_event_check(self):
        return self._find(self._image_path("diamond_case") )

    def locate_static_target_button(self):
        return self._find(self._image_path("set_target_button"), return_cords=True)

    # Generic function to see if something is present on the screen
    def _find(self, path, confidence=0.9, return_cords=False):
        try:
            if return_cords:
                cords = self._locate(path, confidence=confidence)
                if cords is not None:
                    left, top, width, height = cords
                    return (left + width // 2, top + height // 2) # Return middle of found image   
                else:
                    return None

            return True if self._locate(path, confidence=confidence) is not None else False
        except Exception as e:
            raise Exception(e)

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
        x = x + self._padding() # Add's the pad to to the curent x position variable

        return (int(x), int(y))
        # return (x,y)


    def _padding(self):
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

    def _load_img(self, img):
        """
        TODO
        """
        # load images if given filename, or convert as needed to opencv
        # Alpha layer just causes failures at this point, so flatten to RGB.
        # RGBA: load with -1 * cv2.CV_LOAD_IMAGE_COLOR to preserve alpha
        # to matchTemplate, need template and image to be the same wrt having alpha
        
        if isinstance(img, (str)):
            # The function imread loads an image from the specified file and
            # returns it. If the image cannot be read (because of missing
            # file, improper permissions, unsupported or invalid format),
            # the function returns an empty matrix
            # http://docs.opencv.org/3.0-beta/modules/imgcodecs/doc/reading_and_writing_images.html
            img_cv = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
            if img_cv is None:
                raise IOError(f"Failed to read {img} because file is missing, has improper permissions, or is an unsupported or invalid format")
        elif isinstance(img, np.ndarray):
            img_cv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # don't try to convert an already-gray image to gray
            # if grayscale and len(img.shape) == 3:  # and img.shape[2] == 3:
            # else:
            #     img_cv = img
        elif hasattr(img, 'convert'):
            # assume its a PIL.Image, convert to cv format
            img_array = np.array(img.convert('RGB'))
            img_cv = img_array[:, :, ::-1].copy()  # -1 does RGB -> BGR
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        else:
            raise TypeError('expected an image filename, OpenCV numpy array, or PIL image')
        
        return img_cv


    def _locate_all(self, template_path, confidence=0.9, limit=100, region=None):
        """
            Template matching a method to match a template to a screenshot taken with mss.
            
            @template_path - Path to the template image
            @confidence - A threshold value between {> 0.0f & < 1.0f} (Defaults to 0.9f)

            credit: https://github.com/asweigart/pyscreeze/blob/b693ca9b2c964988a7e924a52f73e15db38511a8/pyscreeze/__init__.py#L184

            Returns a list of cordinates to where openCV found matches of the template on the screenshot taken
        """

        monitor = {'top': 0, 'left': 0, 'width': self.width, 'height': self.height} if region is None else region

        if  0.0 > confidence <= 1.0:
            raise ValueError("Confidence must be a value between 0.0 and 1.0")

        with mss.mss() as sct:

            # Load the taken screenshot into a opencv img object
            img = np.array(sct.grab(monitor))
            screenshot = self._load_img(img) 

            if region:
                screenshot = screenshot[region[1]:region[1]+region[3],
                                        region[0]:region[0]+region[2]
                                        ]
            else:
                region = (0, 0)
            # Load the template image
            template = self._load_img(template_path)

            confidence = float(confidence)

            # width & height of the template
            templateHeight, templateWidth = template.shape[:2]

            # Find all the matches
            # https://stackoverflow.com/questions/7670112/finding-a-subimage-inside-a-numpy-image/9253805#9253805
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)    # heatmap of the template and the screenshot"
            match_indices = np.arange(result.size)[(result > confidence).flatten()]
            matches = np.unravel_index(match_indices[:limit], result.shape)
            
            # Defining the coordinates of the matched region
            matchesX = matches[1] * 1 + region[0]
            matchesY = matches[0] * 1 + region[1]

            # for x, y in zip(matchesX, matchesY):
            #     cv2.rectangle(screenshot, (x, y), (x + templateWidth, y + templateHeight), (0, 0, 255), 10)
            # cv2.imshow("Image", screenshot)
            # cv2.imshow("Template", template)
            # cv2.waitKey()
            # cv2.destroyAllWindows()

            if len(matches[0]) == 0:
                return None
            else:
                return [ (x, y, templateWidth, templateHeight) for x, y in zip(matchesX, matchesY) ]

    def _locate(self, template_path, confidence=0.9, tries=1):
        """
            Locates a template on the screen.
        """
        result = self._locate_all(template_path, confidence)
        return result[0] if result is not None else None


if __name__ == "__main__":
    import time

    inst = BotUtils()
    print("sleeping for 2 secs")
    time.sleep(2)
    

    res = inst._locate(inst._image_path("obyn"), confidence=0.9)
    print(res)