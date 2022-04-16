import json
import mouse, keyboard
import os
import time
from collections import defaultdict
from pprint import pprint

"""
    Record mouse x,y cordinates to json file

    f1 - capture position

    shift+alt+z - redo
    shift+alt+p - print current positions
    shift+alt+s - save to file
    shift+alt+l - simulate mouse positions

    ctrl+q - exit
"""

# monkey target right arrow - (486, 500)


def writeToFile(data):
    with open("positions.json", "w+", encoding="utf-8") as file:
        json.dump(data, file)
        # Kolla ifall filen är tom eller inte

def simulatePositions(posObj):
    for key, value in posObj.items():
        mouse.move(value[0], value[1])
        time.sleep(1)


def main():
    if os.stat("positions.json").st_size == 0:
        file = open("positions.json", "w")
        file.writelines("{}") # Skicka in en tom json bracket så att skiten inte crashar
        file.close()

    positions = defaultdict(dict)

    currentPlacementKey = 1
    # currentJsonFile = json.load(file)

    while True:
        currentPos = mouse.get_position()
        # print(currentPos)

        if keyboard.is_pressed("F1"):
            print("True", currentPos)
            positions[str(currentPlacementKey)] = currentPos
            currentPlacementKey += 1
            time.sleep(1)
        elif keyboard.is_pressed("shift+alt+z"):
            print("DEL")
            positions.pop(str(currentPlacementKey - 1), None)
            currentPlacementKey -= 1
            time.sleep(2)
        elif keyboard.is_pressed("shift+alt+p"):
            pprint(positions)
            time.sleep(1)
        elif keyboard.is_pressed("shift+alt+s"):
            print("Saved")
            writeToFile(positions)
            time.sleep(2)
        elif keyboard.is_pressed("shift+alt+l"):
            simulatePositions(positions)
        elif keyboard.is_pressed("ctrl+q"):
            break


if __name__ == "__main__":
    main()
        