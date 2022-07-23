import time

from numpy import isin
import static
from BotCore import BotCore

class Bot(BotCore):
    def __init__(self, instruction_path, debug_mode=False, verbose_mode=False):
        super().__init__(instruction_path)
        
        self.start_time = time.time()
        self.running = True
        self.DEBUG = debug_mode
        self.VERBOSE = verbose_mode
        self.game_start_time = time.time()
        self.fast_forward = True

    def initilize(self):
        if self.DEBUG:
            self.log("RUNNING IN DEBUG MODE, DEBUG FILES WILL BE GENERATED")

        self.press_key("alt")


    def ingame_loop(self):

        current_round = -1
        ability_one_timer = time.time()
        ability_two_timer = time.time()
        
        finished = False

        middle_of_screen = self.width//2, self.height//2

        # main ingame loop
        while not finished:

            # Check for levelup or insta monkey (level 100)
            if self.levelup_check() or self.insta_monkey_check():
                self.click(middle_of_screen, amount=2)
            elif self.monkey_knowledge_check():
                self.click(middle_of_screen, amount=1)

            # Check for finished or failed game
            if self.defeat_check():
                
                if self.DEBUG:
                    print("Defeat detected on round {}; exiting level".format(current_round))
                    self.log_stats(did_win=False, match_time=(time.time()-self.game_start_time))

                self.exit_level(won=False)
                finished = True
                self.reset_game_plan()
                continue

            elif self.victory_check():

                if self.DEBUG:
                    print("Victory detected; exiting level") 
                    self.log_stats(did_win=True, match_time=(time.time()-self.game_start_time))
                
                self.exit_level(won=True)
                finished = True
                self.reset_game_plan()
                continue
            
            current_round = self.getRound()

            if current_round != None:
                # Saftey net; use abilites
                # TODO: Make this more general to support more gameplans
                if current_round >= 39 and self.abilityAvaliabe(ability_one_timer, 35):
                    self.press_key("1")
                    ability_one_timer = time.time()
                
                if current_round >= 51 and self.abilityAvaliabe(ability_two_timer, 90):
                    self.press_key("2")
                    ability_two_timer = time.time()

                # Check for round in game plan
                if str(current_round) in self.game_plan:
                    
                    # Handle all instructions in current round
                    for instruction in self.game_plan[str(current_round)]:
                        if not "DONE" in instruction:

                            if self._game_plan_version == "1":
                                print(instruction)
                                self.v1_handleInstruction(instruction)
                                
                            else:
                                raise Exception("Game plan version {} not supported".format(self._game_plan_version))

                            instruction["DONE"] = True

                            if self.DEBUG:
                                self.log("Current round", current_round) # Only print current round once

    def exit_bot(self): 
        self.running = False

    def place_tower(self, tower_position, keybind):
        self.press_key(keybind) # press keybind
        self.click(tower_position) # click on decired location


    def upgrade_tower(self, tower_position, upgrade_path):
        if not any(isinstance(path, int) for path in upgrade_path) or len(upgrade_path) != 3:
            raise Exception("Upgrade path must be a list of integers", upgrade_path)

        self.click(tower_position)

        # Convert upgrade_path to something usable
        top, middle, bottom = upgrade_path
        
        for _ in range(top):
            self.press_key(static.upgrade_keybinds["top"])

        for _ in range(middle):
            self.press_key(static.upgrade_keybinds["middle"])

        for _ in range(bottom):
            self.press_key(static.upgrade_keybinds["bottom"])
        
        self.press_key("esc")

    def change_target(self, tower_type, tower_position, targets: str | list, delay: int | float | list | tuple = 3):
        if not isinstance(targets, (tuple, list)):
            targets = [targets]

        if isinstance(targets, (list, tuple)) and isinstance(delay, (tuple, list)):
            # check if delay and targets are the same length
            if len(targets) != len(delay):
                raise Exception("Number of targets and number of delays needs to be the same")

        self.click(tower_position)

        current_target_index = 0

        # for each target in target list
        for i in targets:
            
            # Math to calculate the difference between current target index and next target index
            if "SPIKE" in tower_type:
                target_diff = abs((static.target_order_spike.index(i)) - current_target_index)
            else:
                target_diff = abs((static.target_order_regular.index(i)) - current_target_index)
                # self.log("Target diff", target_diff)

            # Change target until on correct target
            for n in range(1, target_diff + 1):
                current_target_index = n
                self.press_key("tab")

            

            # If delay is an int sleep for delay for each target
            if isinstance(delay, (int, float)):
                # If the bot is on the last target  in targets list, dont sleep
                if targets[-1] != i: # 
                    time.sleep(delay)   
            # If delay is a list sleep for respective delay for each target
            elif isinstance(delay, (list, tuple)):
                time.sleep(delay.pop(-1))
            

        self.press_key("esc")

    def set_static_target(self, tower_position, target_pos):
        self.click(tower_position)
        
        target_button = self.locate_static_target_button()
        self.click(target_button)

        self.click(target_pos)

        self.press_key("esc")

    def remove_tower(self, position):
        self.click(position)
        self.press_key("backspace")
        self.press_key("esc")

    def v1_handleInstruction(self, instruction):
        """
            Handles instructions for version 1 of the game plan 
            
        """

        instruction_type = instruction["INSTRUCTION_TYPE"]

        if instruction_type == "PLACE_TOWER":
            tower = instruction["ARGUMENTS"]["MONKEY"]
            position = instruction["ARGUMENTS"]["LOCATION"]

            keybind = static.tower_keybinds[tower]

            self.place_tower(position, keybind)

            if self.DEBUG or self.VERBOSE:
                self.log("Tower placed:", tower)
            
        elif instruction_type == "REMOVE_TOWER":
            self.remove_tower(instruction["ARGUMENTS"]["LOCATION"])
            
            if self.DEBUG or self.VERBOSE:
                self.log("Tower removed on:", instruction["ARGUMENTS"]["LOCATION"])
        
        # Upgrade tower
        elif instruction_type == "UPGRADE_TOWER":
            position = instruction["ARGUMENTS"]["LOCATION"]
            upgrade_path = instruction["ARGUMENTS"]["UPGRADE_PATH"]

            self.upgrade_tower(position, upgrade_path)

            if self.DEBUG or self.VERBOSE:
                self.log("Tower upgraded at position:", instruction["ARGUMENTS"]["LOCATION"], "with the upgrade path:", instruction["ARGUMENTS"]["UPGRADE_PATH"])
        
        # Change tower target
        elif instruction_type == "CHANGE_TARGET":
            target_type = instruction["ARGUMENTS"]["TYPE"]
            position = instruction["ARGUMENTS"]["LOCATION"]
            target = instruction["ARGUMENTS"]["TARGET"]

            if "DELAY" in instruction["ARGUMENTS"]:
                delay = instruction["ARGUMENTS"]["DELAY"] 
                self.change_target(target_type, position, target, delay)
            else:
                self.change_target(target_type, position, target)
            

        # Set static target of a tower
        elif instruction_type == "SET_STATIC_TARGET":
            position = instruction["ARGUMENTS"]["LOCATION"]
            target_position = instruction["ARGUMENTS"]["TARGET"]

            self.set_static_target(position, target_position)
        
        elif instruction_type == "START":
            if "ARGUMENTS" in instruction and "FAST_FORWARD " in instruction["ARGUMENTS"]:
                self.fast_forward = instruction["ARGUMENTS"]["FASTFORWARD"]
                
            self.start_first_round()

            if self.DEBUG or self.VERBOSE:
                self.log("First Round Started")
        
        else:
            # Maybe raise exception or just ignore?
            raise Exception("Instruction type {} is not a valid type".format(instruction_type))

        if self.DEBUG or self.VERBOSE:
            self.log(f"executed instruction:\n{instruction}")


    def abilityAvaliabe(self, last_used, cooldown):
        # TODO: Store if the game is speeded up or not. If it is use the constant (true by default)
        m = 1

        if self.fast_forward:
            m = 3

        return (time.time() - last_used) >= (cooldown / m)

    def start_first_round(self):
        if self.fast_forward:
            self.press_key("space", amount=2)
        else:
            self.press_key("space", amount=1)

        self.game_start_time = time.time()

    def check_for_collection_crates(self):
        if self.collection_event_check():
            if self.DEBUG:
                self.log("easter collection detected")
                # take screenshot of loc and save it to the folder

            self.click("EASTER_COLLECTION") #DUE TO EASTER EVENT:
            time.sleep(1)
            self.click("LEFT_INSTA") # unlock insta
            time.sleep(1)
            self.click("LEFT_INSTA") # collect insta
            time.sleep(1)
            self.click("RIGHT_INSTA") # unlock r insta
            time.sleep(1)
            self.click("RIGHT_INSTA") # collect r insta
            time.sleep(1)
            self.click("F_LEFT_INSTA")
            time.sleep(1)
            self.click("F_LEFT_INSTA")
            time.sleep(1)
            self.click("MID_INSTA") # unlock insta
            time.sleep(1)
            self.click("MID_INSTA") # collect insta
            time.sleep(1)
            self.click("F_RIGHT_INSTA")
            time.sleep(1)
            self.click("F_RIGHT_INSTA")
            time.sleep(1)

            time.sleep(1)
            self.click("EASTER_CONTINUE")

            self.press_key("esc")
            
    # select hero if not selected
    def hero_select(self):
        if not self.hero_check(self.settings["HERO"]):
            self.log(f"Selecting {self.settings['HERO']}")
            self.click("HERO_SELECT")
            self.click(self.settings["HERO"], move_timeout=0.2)
            self.click("CONFIRM_HERO")
            self.press_key("esc")

    def exit_level(self, won=True):
        if won:
            self.click("VICTORY_CONTINUE")
            time.sleep(2)
            self.click("VICTORY_HOME")
        else:
            self.click("DEFEAT_HOME")
            time.sleep(2)
        
        self.wait_for_loading() # wait for loading screen

    def select_map(self):
        map_page = static.maps[self.settings["MAP"]][0]
        map_index = static.maps[self.settings["MAP"]][1]
        
        time.sleep(1)

        self.click("HOME_MENU_START")
        self.click("EXPERT_SELECTION")
        
        self.click("BEGINNER_SELECTION") # goto first page

        # click to the right page
        self.click("RIGHT_ARROW_SELECTION", amount=(map_page - 1), timeout=0.1)

        self.click("MAP_INDEX_" + str(map_index)) # Click correct map
        self.click(self.settings["DIFFICULTY"]) # Select Difficulty
        self.click(self.settings["GAMEMODE"]) # Select Gamemode
        self.click("OVERWRITE_SAVE")

        self.wait_for_loading() # wait for loading screen

        # Only need to press confirm button if we play chimps or impoppable
        if self.settings["GAMEMODE"] == "CHIMPS" or self.settings["GAMEMODE"] == "IMPOPPABLE":
            self.click(self.settings["DIFFICULTY"])
            self.click("CONFIRM_CHIMPS")
    
    def wait_for_loading(self):
        still_loading = True

        while still_loading:
            if self.DEBUG:
                self.log("Waiting for loading screen..")
            
            time.sleep(0.2)
            still_loading = self.loading_screen_check()

if __name__ == "__main__":
    # For testing purposes; open sandbox on dark castle and run Bot.py will place every tower
    import time, sys
    from pathlib import Path
    time.sleep(2)
    gameplan_path = (Path(__file__).resolve().parent/sys.argv[sys.argv.index("--gameplan_path") + 1]) if "--gameplan_path" in sys.argv else exit(0)
    b = Bot(instruction_path=gameplan_path)
    for round, instruction_list in b.game_plan.items():
        print(round, instruction_list)
        for instruction in instruction_list:
            b.v1_handleInstruction(instruction)    
            
        