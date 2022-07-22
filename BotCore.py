import json
import copy
from BotLog import BotLog
from BotUtils import BotUtils

class BotCore(BotLog, BotUtils):
    def __init__(self, instruction_path=r".\Instructions\Dark_Castle_Hard_Standard", game_plan_filename="instructions.json", game_settings_filename="setup.json"):
        self.settings = self._load_settings(instruction_path + "\\" + game_settings_filename)
        self.game_plan = self._load_plan(instruction_path + "\\" + game_plan_filename)
        
        self._game_plan_copy = copy.deepcopy(self.game_plan)

        self._game_plan_version = self.game_plan.pop("VERSION")

        BotLog.__init__(self)
        BotUtils.__init__(self)

    def _load_settings(self, path):
        """
            Will read the @file_path as a json file load into a dictionary
        """
        data = []
        with open(path, 'r', encoding="utf-8") as game_setup:
            data = json.load(game_setup)
        return data

    def _load_plan(self, path):
        """
            Will read the @file_path as a json file load into a dictionary
        """
        data = []
        with open(path, 'r', encoding="utf-8") as game_plan:
            data = json.load(game_plan)
        
        # data.sort()

        return data
    
    def reset_game_plan(self):
        self.game_plan = copy.deepcopy(self._game_plan_copy)