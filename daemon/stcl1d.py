import sys
import os
import time
import gc
import params
import mps.client as mpsClient
import mps.conn as mpsConn
import mps.logger as logger
sys.path.append("/usr/spirent/stcl1/pymodule/pyweb")
import httpd
import traceback
import psutil
import threading 

MODULE_NAME = 'stcl1d'

class ServerThread(threading.Thread):
    def __init__(self):
        super(ServerThread, self).__init__()

    def run(self):
        httpd.run()

class StcL1Application(object):
    def __init__(self):
        self.serverThread = {}
        try:
            serverThread = ServerThread()
            serverThread.start()
            self.serverThread[0] = serverThread
        except:
            logger.log(logger.ERROR, "Failed to start server thread")

    def stop(self):
        logger.log(logger.Info, "Stopping server thread")
        for thread in self.serverThread:
            thread.exit()


class stcl1d(object):
    """
    stcl1 daemon
    """
    def __init__(self, name, param):
        self.params = param
        self.name = name

    def init_logger(self):
        redirect_stdout = (self.params.redirect_to == 'stdout')
        redirect_file = (self.params.redirect_to, None)[redirect_stdout]
        logger.init(self.name, redirect_stdout, redirect_file)
        logger.setLevel(self.params.log_level)

    def signal_startup(self):
        if self.params.startup_fifo:
            f = open(self.params.startup_fifo, 'w')
            print >>f, "OK",

    def run(self):
        self.init_logger()

        # Join the MPS Network
        logger.log(logger.INFO, "Starting MPS")
        if not mpsClient.start(self.name, self.params.tcp_port):
            raise SystemExit

        app = StcL1Application()
        # Force garbage collection post-initialization
        gc.collect()

        # Signal successful daemon startup
        self.signal_startup()
        logger.log(logger.INFO, "Signaled startup, entering main loop")

        # This is the main loop of the daemon -- it runs forever or until we interrupt the daemon (when running interactively)
        while True:
            try:
                mpsClient.run()
            except KeyboardInterrupt:
                break
            except:
                traceback.print_exc()

        # Shutdown MPS
        logger.log(logger.INFO, "Stopping MPS")
        app.stop()
        mpsClient.stop()

def main():

    for proc in psutil.process_iter():
        if proc.name == "hwmgrd":
            proc.suspend()
            time.sleep(0.5)
            break

    param = params.Params()
    try:
        stcl1_daemon = stcl1d(MODULE_NAME, param)
        stcl1_daemon.run()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
    for proc in psutil.process_iter():
        if proc.name == "hwmgrd":
            #proc.resume()
            time.sleep(0.5)
            break

if __name__ == '__main__':
    main()
