# main imports
import os
import time
import numpy as np
import pickle

# module imports
from ..utils import api

from ..utils.processing import crop_images
from .. import config as cfg

# expe imports
from .quest_plus import QuestPlus
from .quest_plus import psychometric_fun


def run_quest_one_image(request, model_filepath, output_file):

    # get parameters
    qualities = request.session.get('qualities')
    scene_name = request.session.get('scene')
    expe_name = request.session.get('expe')

    # by default
    iteration = 0

    # used to stop when necessary
    if 'iteration' in request.GET:
        iteration = int(request.GET.get('iteration'))
    else:
        request.session['expe_started'] = False

    # first time only init `quest`
    # if experience is started we can save data
    if request.session.get('expe_started'):

         # does not change expe parameters
        if request.session['expe_previous_iteration'] == iteration:
            return None
        else:
            answer = int(request.GET.get('answer'))
            answer_time = time.time() - request.session['answer_time']
            print("Answer time is ", answer_time)
            previous_percentage = request.session.get('expe_percentage')
            previous_orientation = request.session.get('expe_orientation')
            previous_position = request.session.get('expe_position')
            previous_stim = request.session.get('expe_stim')

    # default params
    thresholds = np.arange(50, 10000, 50)
    stim_space=np.asarray(qualities)
    slopes = np.arange(0.0001, 0.001, 0.00003)

    # check if necessary to construct `quest` object
    if not os.path.exists(model_filepath):
        qp = QuestPlus(stim_space, [thresholds, slopes], function=psychometric_fun)
    else:
        print('Load `qp` model')
        filehandler = open(model_filepath, 'rb') 
        qp = pickle.load(filehandler)
    
    # if experience is already began
    if request.session.get('expe_started'):

        # TODO : check `i` variable 
        # update of `quest`
        # qp.update(qualities[i], answer)
        qp.update(qualities[iteration], answer) 
        entropy = qp.get_entropy()

        line = str(previous_stim) 
        line += ";" + scene_name 
        line += ";" + str(previous_percentage)
        line += ";" + str(previous_orientation) 
        line += ";" + str(previous_position) 
        line += ";" + str(answer) 
        line += ";" + str(answer_time) 
        line += ";" + str(entropy) 
        line += '\n'

        output_file.write(line)
        output_file.flush()

    # save `quest` model
    file_pi = open(model_filepath, 'wb') 
    pickle.dump(qp, file_pi)

    # construct image 
    if iteration < cfg.expes_configuration[expe_name]['params']['iterations']:
        # process `quest`
        next_stim = qp.next_contrast()
        print("Next quality ", next_stim)

        # construct new image
        noisy_image = api.get_image(scene_name, next_stim)

        # reconstruct reference image from list stored into session
        ref_image = api.get_image(scene_name, 'max')
        img_merge, percentage, orientation, position = crop_images(noisy_image, ref_image)
    else:
        request.session['expe_finished'] = True
        return None

    # set current step data
    request.session['expe_percentage'] = percentage
    request.session['expe_orientation'] = orientation
    request.session['expe_position'] = position
    request.session['answer_time'] = time.time()
    request.session['expe_previous_iteration'] = iteration
    request.session['expe_stim'] = str(next_stim)
    
    # expe is now started
    request.session['expe_started'] = True

    return img_merge