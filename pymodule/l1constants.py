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
global json_data
with open(JSON_INPUT_PATH) as f:
    json_data = json.load(f)
