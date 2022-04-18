# btd6farmer
v0.1
## Inspired from [RavingSmurfGB](https://github.com/RavingSmurfGB/Py_AutoBloons), some functions is taken from that repo


This python bot will farm dark castle on chimps mode in BTD 6. It uses tesseract to find the current level and is able to navigate autonomously after start.

*The script is made for 1440p screen resolutions but should also work with 1080p thanks to RacingSmurfGB* =)

*Should work on linux using proton but the bot is made for Windows*

Feel free to make a pull request if you find any improvements or create a issue if something isn't working correctly
## Requrements
- Tesseract v5.0+
- Python 3.10+

## Dependencies:
- keyboard==0.13.5
- mouse==0.7.1
- numpy==1.22.3
- opencv_python==4.5.5.64
- pyautogui==0.9.53
- pytesseract==0.3.9

## Instalation
The script relies on tesseract which can be installed using this [this](https://github.com/UB-Mannheim/tesseract/wiki) guide. 
(*If by any chance the tesseract installation directory is different from the directory specified in main.py you need to manually change that in the script. Otherwise the script will not work!*)

default path:
```py
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

After installing tesseract the python requirments can be installed with\
`python -m pip install -r requirements.txt`

## Running the bot
Open up BTD 6 run main.py in cmd\
`py main.py`

Navigate to the homescreen of BTD 6 within 5 seconds of starting the script.

Press f11 to get printed infromation on how the bot is doing

## Ingame monkey requirments

|Monkey|Upgrade|
|--|--|
|Monkey Submarine|2-0-3|
|Dart Monkey|0-0-2|
|Sniper| 4-0-2 |
|Spike factory| 0-2-5 & 4-2-0|
|Monkey village|2-0-2|
|Boomerang|0-2-4|
|Glue Gunner|0-2-3|
|Mortar Monkey|0-0-4|
|Alchemist|4-2-0|


## Issues
Currently there is a bug in BTD 6 where the keybinds stop working if alt+tab is pressed. If by some reason this bug occurs. Please press alt ingame after starting the script otherwise the script wont be able to place towers.

