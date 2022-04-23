import pyautogui
import time
import mouse
import keyboard
import csv
import static


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



def padding():
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

    
    width, height = pyautogui.size()
    pad = 0
    for x in reso_16: 
        if height == x['height']:
            pad = (width - x['width'])/2
    #print("I have been padding -- " + str(pad))

    # DEBBUGGING
    return pad

def scaling(pos_list):
    """
        This function will dynamically calculate the differance between current resolution and designed for 2560x1440
        it will also add any padding needed to positions to account for 21:9 

        do_padding -- this is used during start 
    """

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
    move_mouse(scaling(static.button_positions[btn]))
    mouse.click(button="left") # performs the pyautogui click function while passing in the variable from button_positions that matches button
    time.sleep(0.5)

def press_key(key, timeout=0.1):
    # print(key)
    keyboard.send(key)
    time.sleep(timeout)