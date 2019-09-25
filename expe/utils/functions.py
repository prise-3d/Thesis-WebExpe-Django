# main imports
import random

# module imports
from .. import config as cfg

def uniqueID():
    '''
    Return unique identifier for current user and 
    '''
    return str(random.uniform(0, 1))[2:15]


def write_header_expe(f, expe_name):
    '''
    Write specific header into file
    '''

    f.write(cfg.expes_configuration[expe_name]['output_header'])