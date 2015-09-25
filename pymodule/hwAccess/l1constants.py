"""
module to store l1 constants used throughout pymodule
"""
import json

LAYER1_PATH = "/usr/spirent/stcl1"
LOGFILE_PATH = LAYER1_PATH + "/logs"
LOGFILE = LOGFILE_PATH + "/hwaccess.log"
JSON_INPUT_PATH = LAYER1_PATH + "/json/colossus.json"
JS_SCRIPT_PATH = LAYER1_PATH + "/js/"
JPG_PATH = LAYER1_PATH + "/jpg/"
HTML_PATH = LAYER1_PATH + "/html/"
PROCNAME = "hwmgrd"
global json_data
with open(JSON_INPUT_PATH) as f:
    json_data = json.load(f)

def bit(x):
    return 1 << x

def invert(x):
    # basically implementing c style NOT
    # python does not have unsigned values
    # therefore built in NOT actually returns negative value
    mask = (1 << x.bit_length()) - 1
    return (x ^ mask)
