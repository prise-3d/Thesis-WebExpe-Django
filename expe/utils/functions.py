import random

def uniqueID():
    '''
    Return unique identifier for current user and 
    '''
    return str(random.uniform(0, 1))[2:15]