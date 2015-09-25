from mmap import *
import mmap2        

class mmap_spirent(mmap):
    def __init__(self, *args, **kwargs):
       mmap.__init__(self, *args, **kwargs )
       
    def write32(self,data):
        """writes 32 bit data in fpga register"""
        return mmap2.write32(self,data)
    
    def read32(self):
        """read 32 bit data from fpga register"""
        return mmap2.read32(self)

