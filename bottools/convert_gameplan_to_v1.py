
import json
from _ctypes import PyObj_FromPtr
import re
# from pprint import pprint

inputFile = r"C:\Users\limpan\Documents\GitHub\btd6farmer\Instructions\Dark_Castle_Hard_Standard\instructions.json"

# https://stackoverflow.com/questions/13249415/how-to-implement-custom-indentation-when-pretty-printing-with-the-json-module

class NoIndent(object):
    """ Value wrapper. """
    def __init__(self, value):
        self.value = value


class MyEncoder(json.JSONEncoder):
    FORMAT_SPEC = '@@{}@@'
    regex = re.compile(FORMAT_SPEC.format(r'(\d+)'))

    def __init__(self, **kwargs):
        # Save copy of any keyword argument values needed for use here.
        self.__sort_keys = kwargs.get('sort_keys', None)
        super(MyEncoder, self).__init__(**kwargs)

    def default(self, obj):
        return (self.FORMAT_SPEC.format(id(obj)) if isinstance(obj, NoIndent)
                else super(MyEncoder, self).default(obj))

    def encode(self, obj):
        format_spec = self.FORMAT_SPEC  # Local var to expedite access.
        json_repr = super(MyEncoder, self).encode(obj)  # Default JSON.

        # Replace any marked-up object ids in the JSON repr with the
        # value returned from the json.dumps() of the corresponding
        # wrapped Python object.
        for match in self.regex.finditer(json_repr):
            # see https://stackoverflow.com/a/15012814/355230
            id = int(match.group(1))
            no_indent = PyObj_FromPtr(id)
            json_obj_repr = json.dumps(no_indent.value, sort_keys=self.__sort_keys)

            # Replace the matched id string with json formatted representation
            # of the corresponding Python object.
            json_repr = json_repr.replace(
                            '"{}"'.format(format_spec.format(id)), json_obj_repr)

        return json_repr

def convert_json_gameplan_to_v1(inputFile):
    data = {}
    with open(inputFile, 'r') as f:
        data = json.load(f)

    # pprint(data)

    output = {} # main instruction object

    for _round, instructions in data.items():
        output[str(_round)] = []

        for instruction in instructions:

            # Tower placement
            if instruction["UPGRADE"] == None and instruction["UPGRADE_DIFF"] == None:
                new_instruction = PLACE_TOWER(instruction)
                output[str(_round)].append(new_instruction)

            # Tower upgrade
            if instruction["UPGRADE"] != None and instruction["UPGRADE_DIFF"] != None:
                new_instruction = UPGRADE_TOWER(instruction)
                output[str(_round)].append(new_instruction)

            # change target
            if instruction["TARGET"] != None:
                new_instruction = CHANGE_TARGET(instruction)
                output[str(_round)].append(new_instruction)

            # set static target
            if instruction["TARGET_POS"] != None:
                new_instruction = SET_STATIC_TARGET(instruction)
                # print(new_instruction)
                output[str(_round)].append(new_instruction)

            # Round start
            if instruction["ROUND_START"] == True:
                new_instruction = ROUND_START()
                output[str(_round)].append(new_instruction)

    
    with open("output_gameplan.json", 'w') as outfile:
        json.dump(output, outfile, indent=4)
        

def SET_STATIC_TARGET(instruction):
    new_instruction = {}

    new_instruction["INSTRUCTION_TYPE"] = "SET_STATIC_TARGET"
    new_instruction["ARGUMENTS"] = {
        "LOCATION": instruction["POSITION"],
        "TARGET": instruction["TARGET_POS"]
    }

    return new_instruction

def UPGRADE_TOWER(instruction):
    new_instruction = {}

    new_instruction["INSTRUCTION_TYPE"] = "UPGRADE_TOWER"
    new_instruction["ARGUMENTS"] = {
        "LOCATION": instruction["POSITION"],
        "UPGRADE_PATH": list(map(int, instruction["UPGRADE_DIFF"].split("-"))) # Convert old format to new
    }

    return new_instruction

def PLACE_TOWER(instruction):
    new_instruction = {}
    
    new_instruction["INSTRUCTION_TYPE"] = "PLACE_TOWER"
    new_instruction["ARGUMENTS"] = {
        "MONKEY": instruction["TOWER"],
        "POSITION": instruction["POSITION"]
    }
    
    return new_instruction


def ROUND_START():
    new_instruction = {}

    new_instruction["INSTRUCTION_TYPE"] = "START"
    new_instruction["ARGUMENTS"] = {"FAST_FORWARD": True}

    return new_instruction

def CHANGE_TARGET(instruction):
    new_instruction = {}

    # print("INSTRUCTION CHANGE TARGET")
    new_instruction["INSTRUCTION_TYPE"] = "CHANGE_TARGET"

    if len(instruction["TARGET"]) > 1:
        new_instruction["ARGUMENTS"] = {
            "LOCATION": instruction["POSITION"],
            "TARGET": instruction["TARGET"],
            "TYPE": "SPIKE" if instruction["TOWER"] == "SPIKE" else "REGULAR",  
            "DELAY": 3
        }
    else:
        new_instruction["ARGUMENTS"] = {
            "LOCATION": instruction["POSITION"],
            "TARGET": instruction["TARGET"][0],
            "TYPE": "SPIKE" if any(target in instruction["TARGET"] for target in [ "FAR", "SMART" ]) else "REGULAR"
        }

    return new_instruction


convert_json_gameplan_to_v1(inputFile)