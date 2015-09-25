"""
module to create json responses
main function will create three json files
each json file will have one object
{key = attributeName : value = attributeValue}
response will be board family json file and protocol json files
"""
import sys
sys.path.append("/usr/spirent/pymodule")
import json
import time
import threading
import logging
import logging.handlers
import os
sys.path.append("/usr/spirent/stcl1/pymodule/hwAccess")
from l1constants import *

def setupLogging(loglevel='INFO'):
    """
    Configures logging for hw access reads and writes
    """
    if not os.path.exists(LOGFILE_PATH):
        # create log path if first time calling script
        os.mkdir(LOGFILE_PATH)

    logLevelNum = getattr(logging, loglevel, None)
    logFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger.setLevel(logLevelNum)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.DEBUG)
    logger.addHandler(consoleHandler)

    fileHandler = logging.handlers.RotatingFileHandler(LOGFILE, maxBytes=0x10000, backupCount=4)
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.ERROR)
    logger.addHandler(fileHandler)

def get_hw_info(register_set, protocol, hw_access_handle):
    """
    main thread function to retrieve data
    @param protocol to filter
    @param json_data to indicate which registers to read
    """

    # initialize return operator dictionary
    # return types correspond to types specified in default value of bits
    return_operator_dict = {}
    return_operator_dict["AND"] = lambda data, bitMap: (data & bitMap) == bitMap
    return_operator_dict["EQ"] = lambda data, bitMap: data == bitMap
    return_operator_dict["READ"] = lambda data, bitMap: data
    return_operator_dict["AND_READ"] = lambda data, bitMap: (data & bitMap)

    for register in register_set:
        # get data from FPGA
        data = hw_access_handle.read(register)
        for attribute in register["values"]:
            if data is not None:
                # only apply return operator if data is valid
                return_operator = return_operator_dict[attribute["returnOperator"]]
                value = return_operator(data, attribute["bitMap"])
                logger.info("Attribute %s has value of %s" % (attribute["attribute"], value))
                attribute["actualValue"] = value
            else:
                # put some data in the value
                # key word none date with NONE attribute values
                attribute["actualValue"] = "NONE"
    rc = {}
    rc["setName"] = protocol
    rc["registers"] = register_set
    return rc

def createJsonResponse(data, hw_access_handle):
    """
    main function to create JSON response
    to HTTP GET requests

    -Implements retrieval of information from FPGA, PHY, and FrontEnd
    -There will be one thread per protocol (Bar1, MDIO, I2C)
    
    The http server will handle the suspension of hardware manager as well
    """
    global logger
    logger = logging.getLogger('hwaccess')
    if not logger.handlers:
        setupLogging()
    logger.info("Running createJsonResponse")

    threads = {}
    protocols = ['Bar1', 'MDIO', 'I2C']
    while True:
        # ensure that each thread starts succesfully
        for protocol in protocols:
            # start each protocol thread
            logger.info("Starting thread for protocol %s" % protocol)
            thread = get_hw_info_thread(protocol, data, hw_access_handle)
            thread.start()
            threads[protocol] = thread

        if len(threads) == len(protocols):
            break

    alive = len(threads)
    while alive:
        time.sleep(0.1)
        register_sets = [threads[protocol].join() for protocol in protocols]
        alive = sum(1 for protocol in protocols if threads[protocol].isAlive())

    encoder = json.JSONEncoder(sort_keys=True)
    ret_val = {}
    ret_val["boardFamily"] = data["boardFamily"]
    ret_val["memoryMap"] = register_sets
    rc = encoder.encode(ret_val)
    print rc
    return rc

class get_hw_info_thread(threading.Thread):
    """
    Thread class implementation for hardware access
    """
    def __init__(self, protocol, data, hw_access_handle):
        """
        Init thread with base class
        set protocol class member
        """
        threading.Thread.__init__(self)
        self.protocol = protocol
        self.register_set = self.get_register_set(data)
        self.handle = hw_access_handle
        self.ret_val = None


    def get_register_set(self, data):
        """
        parse json data to get protocol specific
        register set
        """
        memory_map = json_data["memoryMap"]
        for register_set in memory_map:
            if register_set["setName"] == self.protocol:
                return register_set["registers"]

    def run(self):
        """
        run method for thread
        goes to get hardware information for respective protocol
        """
        for attempts in xrange(0, 3):
            try:
                self.ret_val = get_hw_info(self.register_set, self.protocol, self.handle)
                if self.ret_val:
                    logger.info("Thread for protocol %s is finished!" % self.protocol)
                    break
            except ZeroDivisionError, e:
                logger.error("Caught error %s" % str(e))
                pass

            time.sleep(0.1)

    def join(self):
        """
        join method to return back modified register set
        """
        threading.Thread.join(self)
        return self.ret_val
