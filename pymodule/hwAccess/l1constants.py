"""
module to store l1 constants used throughout pymodule
"""
import json
import sys
sys.path.append("/usr/spirent/bin/pysysmgr")
import phxhal
boardFamily = phxhal.getBoardFamilyName()
LAYER1_PATH = "/usr/spirent/stcl1"
LOGFILE_PATH = LAYER1_PATH + "/logs"
LOGFILE = LOGFILE_PATH + "/hwaccess.log"
JSON_INPUT_PATH = LAYER1_PATH + "/json/"
JS_SCRIPT_PATH = LAYER1_PATH + "/js/"
JPG_PATH = LAYER1_PATH + "/jpg/"
HTML_PATH = LAYER1_PATH + "/html/"
PROCNAME = "hwmgrd"

def findJsonFile(bf):
    json_file = ""
    if bf == "COLOSSUS":
        json_file = "colossus_qsfp28.json"

    elif bf == "PROTEUS":
        json_file = "proteus_qsfp28.json"

    return json_file

def bit(shift):
    return 1 << shift

def invert(val):
    # basically implementing c style NOT
    # python does not have unsigned values
    # therefore built in NOT actually returns negative value
    mask = (1 << val.bit_length()) - 1
    return (val ^ mask)

with open(JSON_INPUT_PATH + findJsonFile(boardFamily)) as f:
    json_data = json.load(f)

