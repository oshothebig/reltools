import os
import sys 
import time
import json
import logging

class FlexPersonality (object):
    knobs = { 'asic'   : '',
              'distro' : '',
              'deviceMgmt' : '',
              'mgmtPort' : '',
              'mgmtIp' : '',
              'switchIp' : '',
              'switchMac' : '' 
            }

    def __init__ (self,  platform = None, asic = None, distro = None ):
        logging.basicConfig(stream=sys.stderr)
        self.log = logging.getLogger("System Personalisation")
        self.log.setLevel(logging.DEBUG)
	
    def performBuildTimeCustomization(self):
        self.log.debug(' Customizing ')
        return True

if __name__ == "__main__":
    pass


