# main imports
import random

def uniqueID():
    '''
    Return unique identifier for current user and 
    '''
    return str(random.uniform(0, 1))[2:15]


def write_header_expe(f, expe_name):
    '''
    Write specific header into file
    '''

    if expe_name == 'quest_one_image':
        f.write('stimulus' + ";" + "name_stimulus" + ";" + 'cropping_percentage' + ";" + 'orientation' + ';' 
            + 'image_ref_position' + ';' + 'answer' + ';' + 'time_reaction' + ';' + 'entropy' + '\n')