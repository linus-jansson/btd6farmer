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

# Stats
[Experience points per level](https://bloons.fandom.com/wiki/Experience_Point_Farming)
|Rounds|Beginner|Intermediate|Advanced|Expert|
|--|--|--|--|--|
|1-40 (Easy)|21400|23540|25680|27820|
|31-60 (Deflation)|45950|50545|55140|59735|
|1-60 (Medium)|56950|62645|68340|74035|
|3-80 (Hard)|126150|138765|151380|163995|
|6-100 (Impoppable/CHIMPS)|231150|254265|277380|300495|

## Dark castle chimps (instructions.csv)

The current strategy has a winrate of 99.9% (i've got 24 wins and 0 losses when testing). Each game has an average matchtime of 21.7 minutes.

|Stat|Data|
|--|--|
|Winrate|99.9% due to RNG|
|Average Matchtime|21.7 Minutes|
|Player XP per minute|13847.7|

Other gameplans that will be added, will have the same stats like above

*Note: The strat that is being used has RNG because of the Alchemist, so the results may differ to you from what I got*