import json

class Game:
    def __init__(self, instruction_path=r".\Instructions\Dark_Castle_Hard_Standard", game_plan_filename="instructions.json", game_settings_filename="setup.json"):
        self.settings = self.__load_settings(instruction_path + "\\" + game_settings_filename)
        self.game_plan = self.__load_plan(instruction_path + "\\" + game_plan_filename)
        self.first_round = self.__get_first_round()

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
        return data

    def __get_first_round(self):
        """
            Will return the first round number in the gameplan
        """
        tmp = []
        for key in self.game_plan.keys():
            tmp.append(int(key))
        tmp.sort()
        return tmp[0]



if __name__ == "__main__":
    from pprint import pprint

    instance = Game()
    pprint(instance.game_plan)
    print(instance.first_round)