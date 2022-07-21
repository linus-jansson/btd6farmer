import json
import copy
from BotLog import BotLog
from BotUtils import BotUtils

class BotCore(BotLog, BotUtils):
    def __init__(self, instruction_path=r".\Instructions\Dark_Castle_Hard_Standard", game_plan_filename="instructions.json", game_settings_filename="setup.json"):
        self.settings = self.__load_settings(instruction_path + "\\" + game_settings_filename)
        self.game_plan = self.__load_plan(instruction_path + "\\" + game_plan_filename)
        
        self.__game_plan_copy = copy.deepcopy(self.game_plan)

        super().__init__()

    def __load_settings(self, path):
        """
            Will read the @file_path as a json file load into a dictionary
        """
        data = []
        with open(path, 'r', encoding="utf-8") as game_setup:
            data = json.load(game_setup)
        return data

    def __load_plan(self, path):
        """
            Will read the @file_path as a json file load into a dictionary
        """
        data = []
        with open(path, 'r', encoding="utf-8") as game_plan:
            data = json.load(game_plan)
        
        # data.sort()

        return data
    
    def reset_game_plan(self):
        self.game_plan = copy.deepcopy(self.__game_plan_copy)