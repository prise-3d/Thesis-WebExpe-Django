# django imports
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# main imports
import os
import json
import base64
import random
import numpy as np
from datetime import datetime
import pickle 
import time

# expe imports
from .quest.quest_plus import QuestPlus
from .quest.expe import psychometric_fun

# image processing imports
import io
from PIL import Image

# api imports
from .utils import api
from .utils import functions

from .quest.processing import crop_images
from . import config as cfg


def expe_list(request):

    # get all scenes from dataset
    scenes = api.get_scenes()

    # get list of experiences
    expes = cfg.expe_name_list

    return render(request, 'expe/expe_list.html', {'scenes': scenes, 'expes': expes})


# Create your views here.
def expe(request):
    
    # get param 
    expe_name = request.GET.get('expe')
    scene_name = request.GET.get('scene')

    # unique user ID during session (user can launch multiple exeperiences)
    if 'id' not in request.session:
        request.session['id'] = functions.uniqueID()

    # first time expe is launched add expe information
    if 'expe' not in request.session or expe_name != request.session.get('expe'):
        request.session['expe'] = expe_name
        request.session['scene'] = scene_name

        request.session['begin'] = True
        request.session['qualities'] = api.get_scene_qualities(scene_name)
        # update unique timestamp each time new experience is launched
        request.session['timestamp'] = datetime.strftime(datetime.utcnow(), "%Y-%m-%d_%Hh%Mm%Ss")

    else:
        request.session['begin'] = False

    # refresh if scene_name changed
    if 'scene' not in request.session or scene_name != request.session.get('scene'):
        request.session['expe'] = expe_name
        request.session['scene'] = scene_name

        request.session['begin'] = True
        request.session['qualities'] = api.get_scene_qualities(scene_name)
        # update unique timestamp each time new experience is launched
        request.session['timestamp'] = datetime.strftime(datetime.utcnow(), "%Y-%m-%d_%Hh%Mm%Ss")

    else:
        request.session['begin'] = False

    # create output folder for expe_result
    current_day = datetime.strftime(datetime.utcnow(), "%Y-%m-%d")
    results_folder = os.path.join(cfg.output_expe_folder.format(current_day))

    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    result_filename = expe_name + '_' + scene_name + '_' + request.session.get('id') + '_' + request.session.get('timestamp') +".csv"
    results_filepath = os.path.join(results_folder, result_filename)

    if not os.path.exists(results_filepath):
        output_file = open(results_filepath, 'w')
        functions.write_header_expe(output_file, expe_name)
    else:
        output_file = open(results_filepath, 'a')

    # create `quest` object if not exists    
    models_folder = os.path.join(cfg.model_expe_folder.format(current_day))

    if not os.path.exists(models_folder):
        os.makedirs(models_folder)

    model_filename = result_filename.replace('.csv', '.obj')
    model_filepath = os.path.join(models_folder, model_filename)

    # run `quest` expe
    img_merge = run_quest_one_image(request, model_filepath, output_file)

    if img_merge is not None:
        # create output folder for tmp files if necessary
        tmp_folder = os.path.join(settings.MEDIA_ROOT, cfg.output_tmp_folder)

        if not os.path.exists(tmp_folder):
            os.makedirs(tmp_folder)

        # generate tmp merged image (pass as BytesIO was complicated..)
        # TODO : add crontab task to erase generated img
        filepath_img = os.path.join(tmp_folder, request.session.get('id') + '_' + scene_name + '' + expe_name + '.png')
        img_merge.save(filepath_img)

    # expe parameters
    data = {
        'expe_name': expe_name,
        'img_merged_path': filepath_img,
        'question': cfg.expe_questions[expe_name]['question'],
        'indication': cfg.expe_questions[expe_name]['indication']
    }

    return render(request, 'expe/expe.html', data)


def refresh_data(request, expe_name, scene_name):

    request.session['expe'] = expe_name
    request.session['scene'] = scene_name

    request.session['begin'] = True
    request.session['qualities'] = api.get_scene_qualities(scene_name)
    # update unique timestamp each time new experience is launched
    request.session['timestamp'] = datetime.strftime(datetime.utcnow(), "%Y-%m-%d_%Hh%Mm%Ss")

    # TODO : add in cache ref_image
    # get reference image
    #ref_image = api.get_image(scene_name, 'max')
    # save ref image as list (can't save python object)
    #request.session['ref_img'] = np.array(ref_image).tolist()


def run_quest_one_image(request, model_filepath, output_file):

    # get parameters
    qualities = request.session.get('qualities')
    scene_name = request.session.get('scene')
    # by default
    iteration = 0

    # first time only init `quest`
    # if experience is started we can save data
    if request.session.get('begin'):
        answer = int(request.GET.get('answer'))
        iteration = int(request.GET.get('iteration'))

        answer_time = time.time() - request.session['answer_time']
        previous_percentage = request.session.get('expe_percentage')
        previous_orientation = request.session.get('expe_orientation')
        previous_position = request.session.get('expe_percentage')
        previous_entropy = request.session.get('expe_entropy')

    # default params
    max_iteration = 10
    thresholds = np.arange(50, 10000, 50)
    stim_space=np.asarray(qualities)
    slopes = np.arange(0.0001, 0.001, 0.00003)

    # check if necessary to construct `quest` object
    if not os.path.exists(model_filepath):
        qp = QuestPlus(stim_space, [thresholds, slopes], function=psychometric_fun)
    else:
        filehandler = open(model_filepath, 'rb') 
        qp = pickle.load(filehandler)
    
    # construct image and update `quest` only if necessary
    if iteration < max_iteration:
        # process `quest`
        next_stim = qp.next_contrast()
        print(next_stim)

        # construct new image
        noisy_image = api.get_image(scene_name, next_stim)

        # reconstruct reference image from list stored into session
        ref_image = api.get_image(scene_name, 'max')
        img_merge, percentage, orientation, position = crop_images(noisy_image, ref_image)
    else:
        return None
    
    # if experience is started we can save data
    if request.session.get('begin'):

        # TODO : check `i` variable 
        # update of `quest`
        # qp.update(qualities[i], answer)
        qp.update(str(qualities[iteration]), answer) 
        entropy = qp.get_entropy()

        line = str(next_stim) 
        line += ";" + scene_name 
        line += ";" + str(previous_percentage)
        line += ";" + str(previous_orientation) 
        line += ";" + str(previous_orientation) 
        line += ";" + str(answer) 
        line += ";" + str(answer_time) 
        line += ";" + str(entropy) 
        line += '\n'
        # TODO : add answer time from javascript
        output_file.write(line)
        output_file.flush()


    # save `quest` model
    file_pi = open(model_filepath, 'wb') 
    pickle.dump(qp, file_pi)

    # set current step data
    request.session['expe_percentage'] = percentage
    request.session['expe_orientation'] = orientation
    request.session['expe_position'] = position
    request.session['answer_time'] = time.time()

    return img_merge