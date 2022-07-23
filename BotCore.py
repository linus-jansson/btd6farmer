import json
import copy
from pathlib import Path
from BotLog import BotLog
from BotUtils import BotUtils

class BotCore(BotLog, BotUtils):
    def __init__(self, instruction_path=Path.cwd()/"Instructions"/"Dark_Castle_Hard_Standard", game_plan_filename="instructions.json", game_settings_filename="setup.json"):
        
        # TODO: ADD FAILSAFE
        # When mouse is moved to (0, 0)
        # pyautogui.FAILSAFE = True

        self.settings = self._load_json(instruction_path / game_settings_filename)
        self.game_plan = self._load_json(instruction_path / game_plan_filename)
        
        self._game_plan_copy = copy.deepcopy(self.game_plan)

        self._game_plan_version = self.settings.pop("VERSION")

        BotLog.__init__(self)
        BotUtils.__init__(self)

    def _load_json(self, path):
        """
            Will read the @path as a json file load into a dictionary.
        """
        data = {}
        with path.open('r', encoding="utf-8") as f:
            data = json.load(f)
        return data
    
    def reset_game_plan(self):
        self.game_plan = copy.deepcopy(self._game_plan_copy)
