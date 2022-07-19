# btd6farmer
[![Python application](https://github.com/linus-jansson/btd6farmer/actions/workflows/check_bot.yml/badge.svg?branch=main)](https://github.com/linus-jansson/btd6farmer/actions/workflows/check_bot.yml)
\
v0.1
## Inspired from [RavingSmurfGB](https://github.com/RavingSmurfGB/Py_AutoBloons), some functions is taken from that repository.

This python bot will farm a level (dark castle on hard mode by default) in BTD 6. It uses tesseract to find the current level and is able to navigate autonomously after start.

*The script is made for 1440p screen resolutions but should also work with 1080p thanks to RacingSmurfGB* =)

*Should work on linux using proton but the bot is made for Windows*

Feel free to make a pull request if you find any improvements or create a issue if something isn't working correctly
## Requrements
- Tesseract v5.0+
- Python 3.10+

## Dependencies:
```
keyboard==0.13.5
mouse==0.7.1
numpy==1.22.3
opencv_python==4.5.5.64
pyautogui==0.9.53
pytesseract==0.3.9
```
## Instalation
The script relies on tesseract which can be installed using this [this](https://github.com/UB-Mannheim/tesseract/wiki) guide. 
(*If by any chance the tesseract installation directory is different from the directory specified in bot.py you need to manually change that in the script. Otherwise the bot will not work!*)

default path:
```py
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

After installing tesseract the other requirments can be installed with\
`python -m pip install -r requirements.txt`

## Running the bot
1. Open up BTD 6 and run the main.py script in the command line with `py <location of script>/main.py <directory to gameplan>` or run `run.bat` to run with the default settings
2. Navigate to the homescreen of BTD 6 within 5 seconds of starting the script.

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
|Super|3-0-2|


# Stats
[Experience points per level](https://bloons.fandom.com/wiki/Experience_Point_Farming)
|Rounds|Beginner|Intermediate|Advanced|Expert|
|--|--|--|--|--|
|1-40 (Easy)|21 400|23 540|25 680|27 820|
|31-60 (Deflation)|45 950|50 545|55 140|59 735|
|1-60 (Medium)|56 950|62 645|68 340|74 035|
|3-80 (Hard)|126 150|138 765|151 380|163 995|
|6-100 (Impoppable/CHIMPS)|231 150|254 265|277 380|300 495|

## Dark Castle Hard Mode Standard
|Stat|Data|
|--|--|
|Winrate|99.9% due to RNG|
|Average Matchtime|14 Minutes|
|Player XP per minute|11 713.9|
|Monkey Money per hour| ~ 686 |

Other gameplans that will be added, will have the same stats like above

*Note: The strat that is being used has RNG because of the Alchemist, so the results may differ to you from what I got*
<>