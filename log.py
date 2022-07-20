import json
import os
from l_utils import __handle_time

class Log:
    def __init__(self):
        self.statDict = {
            "Current_Round": None,
            "Last_Upgraded": None,
            "Last_Target_Change": None,
            "Last_Placement": None,
            "Uptime": 0
        }

    def __handle_time(self, ttime):
        """
            Converts seconds to appropriate unit
        """
        if ttime >= 60: # Minutes
            return (ttime / 60, "min")
        elif (ttime / 60) >= 60: # Hours
            return (ttime / 3600, "hrs")
        elif (ttime / 3600) >= 24: # days
            return (ttime / 86400, "d")
        elif (ttime / 86400) >= 7: # Weeks
            return (ttime / 604800, "w")
        else: # No sane person will run this bokk for a week
            return (ttime, "s")

    def log_stats(self, did_win: bool = None, match_time: int | float = 0):
        # Standard dict which will be used if json loads nothing
        data = {"wins": 0, "loses": 0, "winrate": "0%", "average_matchtime": "0 s", "total_time": 0, "average_matchtime_seconds": 0}
        
        # Try to read the file
        try:
            with open("stats.json", "r") as infile:
                try:
                    # Read json file
                    str_file = "".join(infile.readlines())
                    data = json.loads(str_file)
                # Catch if file format is invalid for json (eg empty file)
                except json.decoder.JSONDecodeError:
                    print("invalid stats file")
        # Catch if the file does not exist
        except IOError:
            print("file does not exist")

        # Open as write
        with open("stats.json", "w") as outfile:        
            if did_win:
                data["wins"] += 1
            else:
                data["loses"] += 1
            
            total_matches = (data["wins"] + data["loses"])
            # winrate = total wins / total matches
            winrate = data["wins"] / total_matches

            # Convert to procent
            procentage = (round(winrate * 100, 4))
            
            # Push procentage to winrate
            data["winrate"] = f"{procentage}%"

            data["average_matchtime_seconds"] = (data["total_time"]  + match_time) / total_matches
            
            # new_total_time = old_total_time + current_match_time in seconds
            data["total_time"] += match_time
            
            # average = total_time / total_matches_played
            average_converted, unit = self.__handle_time(data["average_matchtime_seconds"])
            
            # Push average to dictionary
            data["average_matchtime"] = f"{round(average_converted, 3)} {unit}"

            outfile.write(json.dumps(data, indent=4))
        
        return data

    def log(self, *kargs):
        print(*kargs)


    def printStats(self, stats):
        os.system("cls")
        print("="*6)
        if round(time.time() - start_time, 2) >= 60.0:
            stats["Uptime"] = "{} minutes".format(round( (time.time() - start_time) / 60, 2)  )
        elif round(time.time() - start_time, 2) / 60 >= 60.0:
            stats["Uptime"] = "{} hours".format(round( (time.time() - start_time) / 60 / 60, 2) )
        else:
            stats["Uptime"] = "{} seconds".format(round(time.time() - start_time, 2))
        
        for key, value in stats.items():
            print(f"{key.replace('_', ' ')}\t{value}")
        print("="*6)


