# btd6farmer
[![Python application](https://github.com/linus-jansson/btd6farmer/actions/workflows/check_bot.yml/badge.svg?branch=main)](https://github.com/linus-jansson/btd6farmer/actions/workflows/check_bot.yml)
\
v1.0.0
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
1. Open up BTD 6 and run the main.py script in the command line with `py <location of script>/main.py <directory to gameplan>` or run `run.bat` to run with the default settings and gameplan.
2. Navigate to the homescreen of BTD 6 within 5 seconds of starting the script.

# Stats
[Experience points per level](https://bloons.fandom.com/wiki/Experience_Point_Farming)
|Rounds|Beginner|Intermediate|Advanced|Expert|
|--|--|--|--|--|
|1-40 (Easy)|21 400|23 540|25 680|27 820|
|31-60 (Deflation)|45 950|50 545|55 140|59 735|
|1-60 (Medium)|56 950|62 645|68 340|74 035|
|3-80 (Hard)|126 150|138 765|151 380|163 995|
|6-100 (Impoppable/CHIMPS)|231 150|254 265|277 380|300 495|

## Issues
If you find any bugs or have any suggestions for improvements please create an issue or pull request!

## Creating your own gameplans
You are really welcome to create your own gameplan using your stratergies. You are also welcome to make a pull request with that gameplan and I will add it to the repository after testing!

__*NOTE: AS THIS IS STILL A WORK IN PROGRESS I MAY CHANGE THE GUIDE AND LAYOUT IN THE FUTURE FOR EASE OF USE.*__

### setup.py
The setup file is used for the bot to know which hero, map, difficulty and gamemode it should use.

```json
{
    "VERSION": 1,
    "HERO": "OBYN",
    "MAP": "DARK_CASTLE",
    "DIFFICULTY": "HARD_MODE",
    "GAMEMODE": "STANDARD_GAME_MODE"
}
```


### Creating the gameplan
The gameplan is a json file that contains the round as a key and the value as an array with instructions. The instructions is also a json object:
<!--
May be used in the future to make it easier
 ```json
{
    "INSTRUCTION": "MOVE_TO",
    "ARGUMENTS": [
        "x",
        "y"
    ]
}
``` -->
#### instructions.json example
```json
{
  "3": [
    {
      "TOWER": "TESTMONKEY",
      "UPGRADE": "2-0-3",
      "UPGRADE_DIFF": null,
      "TARGET": null,
      "TARGET_POS": null,
      "POSITION": [1454, 578],
      "ROUND_START": false
    },
  ]
}

```
>`3` - is the round number that the instruction is supposed to be executed on\
> `TOWER` - Tower name in file \
> `UPGRADE` - Which path to upgrade `top-middle-bottom` the monkey \
> `TARGET` - What target the tower should use `[ "FIRST", "LAST", "CLOSE", "STRONG" ]` for regular towers and `[ "NORMAL", "CLOSE", "FAR", "SMART" ]` for the spike factory \
> `TARGET_POS` - The position of a static target like a Mortar  \
> `POSITION` - The position of the monkey is placed eg `[1454, 578]` \
> `ROUND_START` - If the round should start with this instruction [can be `true` or `false`]

An instruction array in a round can have multiple objects that will be executed after each other. for example:
```json
{
...
  "92": [
    {
      "TOWER": "GLUE",
      "UPGRADE": null,
      "UPGRADE_DIFF": null,
      "TARGET": ["STRONG"],
      "TARGET_POS": null,
      "POSITION": [899, 481],
      "ROUND_START": false
    },
    {
      "TOWER": "GLUE",
      "UPGRADE": "2-1-4",
      "UPGRADE_DIFF": "2-1-4",
      "TARGET": null,
      "TARGET_POS": null,
      "POSITION": [899, 481],
      "ROUND_START": false
    }
  ]
...
}

```

#### Getting the target position or the position of the placed tower.
An easy way to get the position of the tower or the target you want, is to use the following code:
```py
import mouse, time

while True:
    print(mouse.get_position())
    time.sleep(0.1)
```

#### Maps
|Monkey|Keyword in file|
|--|--|
|Monkey Meadow|MONKEY_MEADOW|
|Tree Stump|TREE_STUMP|
|Town Center|TOWN_CENTER|
|Scrapyard|SCRAPYARD|
|The Cabin|THE_CABIN|
|Resort|RESORT|
|Skates|SKATES|
|Lotus Island|LOTUS_ISLAND|
|Candy Falls|CANDY_FALLS|
|Winter Park|WINTER_PARK|
|Carved|CARVED|
|Park Path|PARK_PATH|
|Alpine Run|ALPINE_RUN|
|Frozen Over|FROZEN_OVER|
|In The Loop|IN_THE_LOOP|
|Cubism|CUBISM|
|Four Circles|FOUR_CIRCLES|
|Hedge|HEDGE|
|End Of The Road|END_OF_THE_ROAD|
|Logs|LOGS|
|Quiet Street|QUIET_STREET|
|Bloonarius Prime|BLOONARIUS_PRIME|
|Balance|BALANCE|
|Encrypted|ENCRYPTED|
|Bazaar|BAZAAR|
|Adora's Temple|ADORAS_TEMPLE|
|Spring Spring|SPRING_SPRING|
|KartsNDarts|KARTSNDARTS|
|Moon Landing|MOON_LANDING|
|Haunted|HAUNTED|
|Downstream|DOWNSTREAM|
|Firing Range|FIRING_RANGE|
|Cracked|CRACKED|
|Streambed|STREAMBED|
|Chutes|CHUTES|
|Rake|RAKE|
|Spice Islands|SPICE_ISLANDS|
|Sunken Columns|SUNKEN_COLUMNS|
|X Factor|XFACTOR|
|Mesa|MESA|
|Geared|GEARED|
|Spillway|SPILLWAY|
|Cargo|CARGO|
|Pat's Pond|PATS_POND|
|Peninsula|PENINSULA|
|High Finance|HIGH_FINANCE|
|Another Brick|ANOTHER_BRICK|
|Off The Coast|OFF_THE_COAST|
|Cornfield|CORNFIELD|
|Underground|UNDERGROUND|
|Sanctuary|SANCTUARY|
|Ravine|RAVINE|
|Flooded Valley|FLOODED_VALLEY|
|Infernal|INFERNAL|
|Bloody Puddles|BLOODY_PUDDLES|
|Workshop|WORKSHOP|
|Quad|QUAD|
|Dark Castle|DARK_CASTLE|
|Muddy Puddles|MUDDY_PUDDLES|
|#Ouch||

#### Heros
|Monkey|Keyword in setupfile|
|--|--|
|Obyn|OBYN|
|Monkey|MONKEY|
|Monkey|MONKEY|
#### Monkeys
|Monkey|Keyword in instruction|
|--|--|
|Hero|HERO|
|Dart Monkey|DART|
|Boomerang Monkey|BOOMERANG|
|Bomb Shooter|BOMB|
|Tack Shooter|TACK|
|Ice Monkey|ICE|
|Glue Gunner|GLUE|
|Sniper Monkey|SNIPER|
|Monkey Sub|SUBMARINE|
|Monkey Buccaneer|BUCCANEER|
|Monkey Ace|ACE|
|Heli Pilot|HELI|
|Mortar Monkey|MORTAR|
|Dartling Gunner|DARTLING|
|Wizard Monkey|WIZARD|
|Super Monkey|SUPER|
|Ninja Monkey|NINJA|
|Alchemist|ALCHEMIST|
|Druid|DRUID|
|Banana Farm|BANANA|
|Spike factory|SPIKE|
|Monkey Village|VILLAGE|
|Engineer Monkey|ENGINEER|

