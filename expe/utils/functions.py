# main imports
import random
from datetime import datetime

# module imports
from .. import config as cfg

def uniqueID():
    '''
    Return unique identifier for current user and 
    '''
    t = datetime.utcnow()
    t = t.timestamp()
    t = int(t*10**6)
    t = str(t)[4:] + str(random.uniform(0, 1))[2:4]
    return t


def write_header_expe(f, expe_name):
    '''
    Write specific header into file
    '''

    f.write(cfg.expes_configuration[expe_name]['output_header'])