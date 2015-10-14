"""
module to store l1 constants used throughout pymodule
"""
import json
import sys
sys.path.append("/usr/spirent/pymodule/pyhal")
from hwinfo import HWINFO
boardFamily = HWINFO.getBoardFamilyName()
modelName = HWINFO.getModelName()
ccpuno = int(HWINFO.getCpuId())
LAYER1_PATH = "/usr/spirent/stcl1"
LOGFILE_PATH = LAYER1_PATH + "/logs"
LOGFILE = LOGFILE_PATH + "/hwaccess.log"
JSON_INPUT_PATH = LAYER1_PATH + "/json/"
JS_SCRIPT_PATH = LAYER1_PATH + "/js/"
JPG_PATH = LAYER1_PATH + "/jpg/"
HTML_PATH = LAYER1_PATH + "/html/"

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

def getVmIndexFromCcpu(bf, model_name, cookie_num):
    """
    mapping function of cookie number to vm instance
    needed by httpd to start on the correct port
    """
    if bf == "COLOSSUS":
        if model_name == "DX2-100G-P4":
            # staggered 1, 9, 17, 25
            return (cookie_num - 1) * 8 + 1
    if bf in ["WRAITH", "ROGUE", "CYLCOPS"]:
        if "40G0" not in model_name:
            # staggered 1, 5, 9, 13, 17
            return (cookie_num - 1) * 4 + 1
    if bf == "ICEMAN":
        if "100GO" not in model_name and "P2" not in model_name:
            # Iceman OG staggered 1, 3
            return (cookie_num - 1) * 2 + 1

    return cookie_num

vm_num = getVmIndexFromCcpu(boardFamily, modelName, ccpuno)

with open(JSON_INPUT_PATH + findJsonFile(boardFamily)) as f:
    json_data = json.load(f)

