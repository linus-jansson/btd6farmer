# btd6farmer - a bot for Bloons Td 6
#### Inspired from [RavingSmurfGB](https://github.com/RavingSmurfGB/Py_AutoBloons), some functions is taken from that repository.
[![Python application](https://github.com/linus-jansson/btd6farmer/actions/workflows/check_bot.yml/badge.svg?branch=main)](https://github.com/linus-jansson/btd6farmer/actions/workflows/check_bot.yml)
\
v1.0.0

This python bot will farm a level (dark castle on hard mode by default) in Bloons TD 6. It uses tesseract to find the current level and is able to navigate autonomously after starting it.

*The script is made for 1440p screen resolutions but should also work with 1080p thanks to RacingSmurfGB* =)

*Currently there is no support for linux and proton*

Feel free to make a pull request if you find any improvements or create a issue if something isn't working correctly!

## Table Of Contents
- [Dependencies](#dependenices) 
- [Installation](#installation)
- [Running the bot](#running)
- [Having issues?](#issues)
- [Creating your own gameplan](#contributing)
    - [Setup file](#setup_file)
    - [Gameplan file](#gameplan_file)
    - [Stats](#stats)
    - [Keyword cheatsheet](#keywords)
        - [Gamemodes](#gamemodes)
        - [Difficulties](#difficulties)
        - [Maps](#maps)
        - [Heros](#heros)
        - [Monkeys](#monkeys)

<a name="dependenices"/>

## Requirements & Dependencies
- Windows
- Tesseract v5.0+
- Python 3.10+

```
keyboard==0.13.5
mouse==0.7.1
mss==6.1.0
numpy==1.22.3
opencv_python==4.5.5.64
pytesseract==0.3.9
```
<a name="installation"/>

## Installation of dependencies:
The script relies on tesseract which can be installed using this [this](https://github.com/UB-Mannheim/tesseract/wiki) guide. 
(*If by any chance the tesseract installation directory is different from the directory specified in bot.py you need to manually change that in the script. Otherwise the bot will not work!*)

default path:
```py
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

After installing tesseract the other requirments can be installed with\
`python -m pip install -r requirements.txt` \
or running `Install_Requirements.bat`

<a name="running"/>

## Running the bot
1. Open up BTD 6 and run the main.py script in the command line with `py <location of script>/main.py <directory to gameplan>` or run `run.bat` to run with the default settings and gameplan.
2. Navigate to the homescreen of BTD 6 within 5 seconds of starting the script.

###### Launch options
- `--debug` -
- `--verbose` -
- `--sandbox` -
- `--gameplan_path` -


<a name="issues"/>

## Having issues with the bot?
If you have any issues with the bot, find any bugs or have any suggestions for improvements, please create an issue or create a pull request!

<a name="contributing"/>

## Creating your own gameplans
You are really welcome to create your own gameplans using your own stratergies and submiting them to the repo with a pull request. I will add it to the repository after testing!

__*NOTE: AS THIS IS STILL A WORK IN PROGRESS I MAY CHANGE THE GUIDE AND LAYOUT OF THE GAMEPLAN IN THE FUTURE FOR EASE OF USE.*__

__*I also have plans for the future to make it easier to create gameplans so if you want to wait until you create yours you can wait too*__

<a name="setup_file"/>

### setup.py
The setup file is used for the bot to know which hero, map, difficulty and gamemode it should use.
It should be named `setup.py` and be placed in the same directory as the gameplan.

```json
{
    "VERSION": "1",
    "HERO": "OBYN",
    "MAP": "DARK_CASTLE",
    "DIFFICULTY": "HARD_MODE",
    "GAMEMODE": "STANDARD_GAME_MODE",
    "OPTIONS": { // TODO: Add options
        "COLLECT_BANANAS": true,
        "OPEN_CHEST": true,
    }
}
```
>`VERSION` - Use version 1 for now\
> `Hero` - Which hero to use *[list of avaliable heros](#heros)*  \
> `MAP` - Which map to use *[list of avaliable maps](#maps)* \
> `DIFFICULTY` - Which Difficulty to use *[list of avaliable difficultues](#difficulties)* \
> `GAMEMODE` - Which Gamemode to use *[list of avaliable Gamemodes](#gamemodes)* \
###### OPTIONS
> `COLLECT_BANANAS` - If the bot should automatically pick up bananas from traps and bananafarms \
> `OPEN_CHEST` - If the bot should automatically open chests if its unopened on the main menu

<a name="gameplan_file"/>

### instructions.json
#### Creating the gameplan 
The gameplan is a json file that contains the round as a key and the value as an array with instructions. The instructions is also a json object:

#### instructions.json example
```json
{
    "3": [
        {
            "INSTRUCTION_TYPE": "PLACE_TOWER",
            "ARGUMENTS": {
                "TOWER": "TOWER_TYPE",
                "POSITION": [ x, y ]
            }
        },
        {
            "INSTRUCTION_TYPE": "START",
            "ARGUMENTS": {
                "FAST_FORWARD": true,
            }
        }
    ]
}

```
##### instruction types
- `START` - Indicates the game
    - `FAST_FORWARD` - (true / false) Defaults to True. Should the bot play in fast forward mode?
- `PLACE_TOWER` - Place a tower on the map
    - `MONKEY` - Type of monkey to place 
    - `LOCATION` - [x, y] position of tower to be placed 
- `UPGRADE_TOWER` - Upgrade a tower on the map
    - `LOCATION` - [x, y]  position of tower to be upgraded
    - `UPGRADE_PATH` - [top, middle, bottom] array of upgrades eg [1, 0, 1]
- `CHANGE_TARGET` - changes target of a tower
    - `LOCATION` - [x, y] location of the tower
    - `TARGET` - target or targets eg [ "FIRST", "LAST", "STRONG" ]. Can be a string or a array of targets
    - `TYPE` - (SPIKE or REGULAR) # TODO: add support for Heli targets
    - `DELAY` - (optional) Defaults to 3 delay between each target change, can be one delay eg `2` for 2 seconds or multiple `[1, 3, 4]` to sleep for 1 second, 3 seconds and 4 seconds respectively for each target change.
- `REMOVE_TOWER` - Removes a tower
    - `LOCATION` - [x, y] location of the tower
- `SET_STATIC_TARGET`
    - `LOCATION` - [x, y] location of tower
    - `TARGET_LOCATION` - [x, y] location of target
- `END` - (OPTIONAL) Finished instructions


An instruction array in a round can have multiple objects that will be executed after each other. for example:
```json

```

#### Creating the gameplan in excel and converting to json
TODO
### Getting the position of a tower or the target position.
An easy way to get the position of the tower or the target you want, is to use the following code:
```py
import mouse, time

while True:
    print(mouse.get_position())
    time.sleep(0.1)
```
Run it in a terminal and copy the decired position into the gameplan.


### Stats
[Experience points per level](https://bloons.fandom.com/wiki/Experience_Point_Farming)
|Rounds|Beginner|Intermediate|Advanced|Expert|
|--|--|--|--|--|
|1-40 (Easy)|21 400|23 540|25 680|27 820|
|31-60 (Deflation)|45 950|50 545|55 140|59 735|
|1-60 (Medium)|56 950|62 645|68 340|74 035|
|3-80 (Hard)|126 150|138 765|151 380|163 995|
|6-100 (Impoppable/CHIMPS)|231 150|254 265|277 380|300 495|

<a name="keywords"/>

#### Keyword cheatsheet for the setup file and the gameplan

<a name="gamemodes"/>
<details>
<summary>Gamemodes</summary>
TODO
</details>

<a name="difficulties"/>
<details>
<summary>Difficulties</summary>
TODO
</details>

<a name="maps"/>
<details>
<summary>Maps</summary>

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
|#Ouch|OUCH|

</details>

<a name="heros"/>
<details>
<summary>Heros</summary>

|Monkey|Keyword in setupfile|
|--|--|
|Quincy|QUINCY|
|Gwendolin|GWENDOLIN|
|Striker Jones|STRIKER_JONES|
|Obyn Greenfoot|OBYN|
|Captain Churchill|MONKEY|
|Benjamin|BENJAMIN|
|Ezili|EZILI|
|Pat Fusty|PAT_FUSTY|
|Adora|ADORA|
|Admiral Brickell|ADMIRAL_BRICKELL|
|Etienne|ETIENNE|
|Sauda|SAUDA|
|Psi|PSI|
|Geraldo|GERALDO|

</details>

<a name="monkeys"/>
<details>
<summary>Monkeys</summary>

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

</details>


