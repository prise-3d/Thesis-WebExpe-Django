# main imports
import os
import time
import numpy as np
import pickle

# django imports
from django.conf import settings

# module imports
from ..utils import api

from ..utils.processing import crop_images
from .. import config as cfg

# expe imports
from .classes.quest_plus import QuestPlus
from .classes.quest_plus import psychometric_fun


def run_quest_one_image(request, model_filepath, output_file):

    # 1. get session parameters
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

    # 2. Get expe information if started
    # first time only init `quest`
    # if experiments is started we can save data
    if request.session.get('expe_started'):

         # does not change expe parameters
        if request.session['expe_data']['expe_previous_iteration'] == iteration:
            return None
        else:
            current_expe_data = request.session['expe_data']
            answer = int(request.GET.get('answer'))
            expe_answer_time = time.time() - current_expe_data['expe_answer_time']
            previous_percentage = current_expe_data['expe_percentage']
            previous_orientation = current_expe_data['expe_orientation']
            previous_position = current_expe_data['expe_position']
            previous_stim = current_expe_data['expe_stim']

            print("Answer time is ", expe_answer_time)

    # 3. Load or create Quest instance
    # default params
    # TODO : add specific thresholds information for scene
    thresholds = np.arange(50, 10000, 50)
    stim_space = np.asarray(qualities)
    slopes = np.arange(0.0001, 0.001, 0.00003)

    # check if necessary to construct `quest` object
    if not os.path.exists(model_filepath):
        qp = QuestPlus(stim_space, [thresholds, slopes], function=psychometric_fun)
    else:
        print('Load `qp` model')
        filehandler = open(model_filepath, 'rb') 
        qp = pickle.load(filehandler)
    
    # 4. If expe started update and save experiments information and model
    # if experiments is already began
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
        line += ";" + str(expe_answer_time) 
        line += ";" + str(entropy) 
        line += '\n'

        output_file.write(line)
        output_file.flush()

    # save `quest` model
    file_pi = open(model_filepath, 'wb') 
    pickle.dump(qp, file_pi)

    # 5. Contruct new image and save it
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

    # save image using user information
    # create output folder for tmp files if necessary
    tmp_folder = os.path.join(settings.MEDIA_ROOT, cfg.output_tmp_folder)

    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)

    # generate tmp merged image (pass as BytesIO was complicated..)
    filepath_img = os.path.join(tmp_folder, request.session.get('id') + '_' + scene_name + '' + expe_name + '.png')
    
    # replace img_merge if necessary (new iteration of expe)
    if img_merge is not None:
        img_merge.save(filepath_img)

    # 6. Prepare experiments data for current iteration and data for view
    
    # here you can save whatever you need for you experiments
    data_expe = {
        'image_path': filepath_img,
        'expe_percentage': percentage,
        'expe_orientation': orientation,
        'expe_position': position,
        'expe_answer_time': time.time(),
        'expe_previous_iteration': iteration,
        'expe_stim': str(next_stim)
    }
    
    # expe is now started
    request.session['expe_started'] = True

    return data_expe