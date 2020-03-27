# main imports
import os
import time
import numpy as np
import pickle
import sys

from datetime import datetime

# django imports
from django.conf import settings

# module imports
from ..utils import api

from ..utils.processing import crop_images
from .. import config as cfg

# expe imports
from .classes.quest_plus import QuestPlus
from .classes.quest_plus import psychometric_fun

# other imports 
from ipfml import utils
from pprint import pprint

from PIL import Image, ImageDraw

lang = settings.LANGUAGE_CODE

def example_quest_one_image(request, expe_name, scene_name):
    
    example_number = request.GET.get('example')
    
    # get expected image qualities indices (load noisy and ref image)
    params_image = cfg.expes_configuration[expe_name]['text']['examples']['images'][int(example_number)]
    qualities = api.get_scene_qualities(scene_name)

    noisy_quality = qualities[params_image[0]]
    ref_quality = qualities[params_image[1]]

    noisy_image = api.get_image(scene_name, noisy_quality)
    ref_image = api.get_image(scene_name, ref_quality)

    # get crop params from configuration
    crop_params = cfg.expes_configuration[expe_name]['text']['examples']['crop_params'][int(example_number)]

    img_merge, percentage, orientation, position = crop_images(noisy_image,     
                                                                ref_image, 
                                                                per=crop_params[0], 
                                                                orien=crop_params[1], 
                                                                swap_img=crop_params[2])
    width, height = img_merge.size
    if orientation==0:
        left, top, right, bottom = percentage*width, 0, percentage*width, height   #vertical
    else:
        left, top, right, bottom = 0, percentage*height, width, percentage*height   #horizontal
    if  int(example_number) % 2 != 0 :
        if noisy_quality != qualities[-1]:#-noisy_quality > qualities[-1]-(10*qualities[-1])/100 :
            draw = ImageDraw.Draw(img_merge) 
            draw.line((left, top, right, bottom), fill='black', width=5)
    example_sentence = cfg.expes_configuration[expe_name]['text']['examples']['sentence'][lang][int(example_number)]

    example_sentence = example_sentence.format(cfg.expes_configuration[expe_name]['text']['examples']['cut_name'][lang][orientation], str(percentage*100))
    
    
    # Temporary save of image
    tmp_folder = os.path.join(settings.MEDIA_ROOT, cfg.output_tmp_folder)

    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)

    # generate tmp merged image (pass as BytesIO was complicated..)
    filepath_img = os.path.join(tmp_folder, 'example_' + scene_name + '' + expe_name + '.png')
    
    # replace img_merge if necessary (new iteration of expe)
    if img_merge is not None:
        img_merge.save(filepath_img)

    data_example = {
        'example_sentence': example_sentence,
        'example': filepath_img
    }

    return data_example

    

def run_quest_one_image(request, model_filepath, output_file):

    # 1. get session parameters
    #qualities = request.session.get('qualities')
    scene_name = request.session.get('scene')
    expe_name = request.session.get('expe')

    checked = request.GET.get('check')

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
        elif iteration > cfg.expes_configuration[expe_name]['params']['max_iterations']:
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
    #thresholds = np.arange(50, 10000, 50)
    #stim_space = np.asarray(qualities)
    threshold_range = cfg.expes_configuration[expe_name]['params']['thresholds'][scene_name]
    stim_space = np.arange(threshold_range[0], threshold_range[1], threshold_range[2]) 
    stim_space = np.append(stim_space, threshold_range[1])
    
    slope_range = cfg.expes_configuration[expe_name]['params']['slopes'][scene_name]
    slopes = np.arange(slope_range[0], slope_range[1], slope_range[2]) 
    #slopes = np.arange(0.0001, 0.001, 0.00003) # contemporary
    #slopes = np.arange(0.0005, 0.01, 0.0003) # bathroom
    #slopes = np.arange(1.995,19.95,0.5985)
    
    # TODO : update norm slopes
    # stim_space = np.asarray(qualities)
    # slopes = np.arange(0.0001, 0.001, 0.00003)

    # # normalize stim_space and slopes for this current scene
    # stim_space_norm = np.array(utils.normalize_arr_with_range(stim_space, stim_space.min(), stim_space.max()))
    # slopes_norm = slopes * (slopes.max() - slopes.min()) 

    # check if necessary to construct `quest` object
    if not os.path.exists(model_filepath):
        print('Creation of `qp` model')
        #print(slopes_norm)
        #qp = QuestPlus(stim_space_norm, [stim_space_norm, slopes_norm], function=psychometric_fun)
        qp = QuestPlus(stim_space, [stim_space, slopes], function=psychometric_fun)

    else:
        print('Load `qp` model')
        filehandler = open(model_filepath, 'rb') 
        qp = pickle.load(filehandler)
        pprint(qp)
    
    #initialize entropy
    entropy = np.inf
    last_entropy = 0
    crit_entropy = cfg.expes_configuration[expe_name]['params']['entropy']
    min_iter = cfg.expes_configuration[expe_name]['params']['min_iterations']
    max_iter = cfg.expes_configuration[expe_name]['params']['max_iterations']
    
    threshold = None
    
    # 4. If expe started update and save experiments information and model
    # if experiments is already began
    if request.session.get('expe_started'):

        # TODO : update norm slopes
        #previous_stim_norm = (int(previous_stim) - stim_space.min()) / (stim_space.max() - stim_space.min() + sys.float_info.epsilon)

        print(previous_stim)
        #print(previous_stim_norm)

        qp.update(int(previous_stim), answer) 
        threshold = qp.get_fit_params(select='mode')[0]
        
        entropy = qp.get_entropy()
        print('chosen entropy', entropy)

        line = str(previous_stim) 
        line += ";" + scene_name 
        line += ";" + str(previous_percentage)
        line += ";" + str(previous_orientation) 
        line += ";" + str(previous_position) 
        line += ";" + str(answer) 
        line += ";" + str(expe_answer_time) 
        line += ";" + str(entropy) 
        line += ";" + str(checked)
        line += '\n'

        output_file.write(line)
        output_file.flush()
        
        entropies = np.loadtxt(output_file.name, delimiter=";", usecols=7, skiprows=1)

        if len(entropies.shape) > 0 and entropies.shape[0] >= 11:
            last_entropy = entropies[-11]
        else:
            last_entropy = np.nan

    # check time
    current_time = datetime.utcnow()
    current_time = time.mktime(current_time.timetuple())
    started_time = request.session.get('timestamp')
    started_time = time.mktime(datetime.strptime(started_time, "%Y-%m-%d_%Hh%Mm%Ss").timetuple())
    max_time = cfg.expes_configuration[expe_name]['params']['max_time'] * 60
    if current_time - started_time >= max_time:
        request.session['expe_finished'] = True
        timeout = { 'timeout' : True }
        return timeout
    
    # 5. Contruct new image and save it
    # construct image 
    if iteration < min_iter or ((last_entropy is np.nan or np.abs(entropy - last_entropy) >= crit_entropy) and iteration < max_iter):
        # process `quest`
        if iteration <= 4:
            next_stim_id = int(iteration * len(stim_space)/10)
            next_stim = stim_space[next_stim_id]
        else:
            next_stim = qp.next_contrast()
        print(next_stim)
        #next_stim_img = int(next_stim*(stim_space.max()-stim_space.min())+stim_space.min())
    
        print('-------------------------------------------------')
        print('Iteration', iteration)
        print(next_stim)
        #print('denorm', next_stim_img)
        print('-------------------------------------------------')

        #noisy_image = api.get_image(scene_name, next_stim_img)
        noisy_image = api.get_image(scene_name, next_stim)


        # reconstruct reference image from list stored into session
        ref_image = api.get_image(scene_name, 'max')
        img_merge, percentage, orientation, position = crop_images(noisy_image, ref_image)
    else:
        request.session['expe_finished'] = True
        if threshold < stim_space[-1]/3:
            end_message = { 'end_message' : cfg.expes_configuration[expe_name]['text']['end_text']['results'][lang][0]}
        elif threshold < 2*stim_space[-1]/3:
            end_message = { 'end_message' : cfg.expes_configuration[expe_name]['text']['end_text']['results'][lang][1]}
        else:
            end_message = { 'end_message' : cfg.expes_configuration[expe_name]['text']['end_text']['results'][lang][2]}
            
        return end_message
    
    

    # save image using user information
    # create output folder for tmp files if necessary
    tmp_folder = os.path.join(settings.MEDIA_ROOT, cfg.output_tmp_folder)

    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)

    print(request.session.get('id'))
    # generate tmp merged image (pass as BytesIO was complicated..)
    filepath_img = os.path.join(tmp_folder, request.session.get('id') + '_' + scene_name + '' + expe_name + '.png')
    
    # replace img_merge if necessary (new iteration of expe)
    if img_merge is not None:
        img_merge.save(filepath_img)

    # save qp model at each iteration
    file_pi = open(model_filepath, 'wb') 
    pickle.dump(qp, file_pi)

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