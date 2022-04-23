button_positions = { # Creates a dictionary of all positions needed for monkeys (positions mapped to 2160 x 1440 resolution)
    "HOME_MENU_START" : [1123, 1248],
    "EXPERT_SELECTION" : [1778, 1304],
    "RIGHT_ARROW_SELECTION" : [2193, 582],
    "DARK_CASTLE" : [1420, 350], # changed to (x=1941, y=513) in latest patch
    "HARD_MODE" : [1729, 562],
    "CHIMPS_MODE" : [2139, 980],
    "STANDARD_GAME_MODE" : [847,780],
    "OVERWRITE_SAVE" : [1520, 974],
    "VICTORY_CONTINUE" : [1283, 1215],
    "VICTORY_HOME" : [939, 1124],
    "EASTER_COLLECTION" : [1279, 911],
    "F_LEFT_INSTA" : [868, 722],
    "F_RIGHT_INSTA" : [1680, 722],
    "LEFT_INSTA" : [1074, 725],
    "RIGHT_INSTA" : [1479, 724],
    "MID_INSTA" : [1276, 727],
    "EASTER_CONTINUE" : [1280, 1330],
    "EASTER_EXIT" : [100, 93],
    "QUIT_HOME" : [1126, 1135],
    "HERO_SELECT" : [799, 1272],
    "SELECT_OBYN" : [106, 532],
    "CONFIRM_HERO" : [1505, 824],
    "TARGET_BUTTON_MORTAR": [1909, 491],
    "ABILLITY_ONE": [253, 1379],
    "ABILLITY_TWO": [369, 1377],
    "FREEPLAY" : [1611, 1112],
    "OK_MIDDLE" : [1280, 1003],
    "RESTART": [1413, 1094],
    "CONFIRM_CHIMPS" : [1481, 980]

}

monkeys = {
    "DART" : "q",
    "BOOMERANG" : "w",
    "BOMB" : "e",
    "TACK" : "r",
    "ICE" : "t",
    "GLUE" : "y",
    "SNIPER" : "z",
    "SUBMARINE" : "x",
    "BUCCANEER" : "c",
    "ACE" : "v",
    "HELI" : "b",
    "MORTAR" : "n",
    "DARTLING" : "m",
    "WIZARD" : "a",
    "SUPER" : "s",
    "NINJA" : "d",
    "ALCHEMIST" : "f",
    "DRUID" : "g",
    "BANANA" : "h",
    "ENGINEER" : "l",
    "SPIKE" : "j",
    "VILLAGE" : "k",
    "HERO" : "u"
}

upgrade_keybinds = {
    "top" : ",",
    "middle" : ".",
    "bottom" : "/"

}

# Index, regular targets, spike factory targets
target_order_regular = [ "FIRST", "LAST", "CLOSE", "STRONG" ]
target_order_spike   = [ "NORMAL", "CLOSE", "FAR", "SMART" ]
