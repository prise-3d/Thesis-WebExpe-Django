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
from .expes.quest_plus import QuestPlus
from .expes.quest_plus import psychometric_fun

from .expes.run import run_quest_one_image

# image processing imports
import io
from PIL import Image

# module imports
from .utils import api
from .utils import functions

from .utils.processing import crop_images
from . import config as cfg


def expe_list(request):

    # get all scenes from dataset
    scenes = api.get_scenes()

    # get list of experiences
    expes = cfg.expe_name_list

    return render(request, 'expe/expe_list.html', {'scenes': scenes, 'expes': expes})

def indications(request):

    # get param 
    expe_name = request.GET.get('expe')

    # expe parameters
    data = {
        'expe_name': expe_name,
        'question': cfg.expes_configuration[expe_name]['text']['question'],
        'indication': cfg.expes_configuration[expe_name]['text']['indication']
    }

    return render(request, 'expe/expe_indications.html', data)


# Create your views here.
def expe(request):
    
    # get param 
    expe_name = request.GET.get('expe')
    scene_name = request.GET.get('scene')
    
    # default filepath name
    filepath_img = ''

    # unique user ID during session (user can launch multiple exeperiences)
    if 'id' not in request.session:
        request.session['id'] = functions.uniqueID()

    # first time expe is launched add expe information
    if 'expe' not in request.session or expe_name != request.session.get('expe'):
        refresh_data(request, expe_name, scene_name)

    # refresh if scene_name changed
    if 'scene' not in request.session or scene_name != request.session.get('scene'):
        refresh_data(request, expe_name, scene_name)

    # create output folder for expe_result
    current_day = datetime.strftime(datetime.utcnow(), "%Y-%m-%d")
    results_folder = os.path.join(settings.MEDIA_ROOT, cfg.output_expe_folder.format(current_day))

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
    models_folder = os.path.join(settings.MEDIA_ROOT, cfg.model_expe_folder.format(current_day))

    if not os.path.exists(models_folder):
        os.makedirs(models_folder)

    model_filename = result_filename.replace('.csv', '.obj')
    model_filepath = os.path.join(models_folder, model_filename)

    # run `quest` expe
    img_merge = run_quest_one_image(request, model_filepath, output_file)

    if not request.session.get('expe_finished'):
        # create output folder for tmp files if necessary
        tmp_folder = os.path.join(settings.MEDIA_ROOT, cfg.output_tmp_folder)

        if not os.path.exists(tmp_folder):
            os.makedirs(tmp_folder)

        # generate tmp merged image (pass as BytesIO was complicated..)
        # TODO : add crontab task to erase generated img
        filepath_img = os.path.join(tmp_folder, request.session.get('id') + '_' + scene_name + '' + expe_name + '.png')
        img_merge.save(filepath_img)
    else:
        # reinit session as default value
        del request.session['expe']
        del request.session['scene']
        del request.session['qualities']
        del request.session['timestamp']

    # expe parameters
    data = {
        'expe_name': expe_name,
        'img_merged_path': filepath_img,
        'end_text': cfg.expes_configuration[expe_name]['text']['end_text']
    }

    return render(request, 'expe/expe.html', data)


def refresh_data(request, expe_name, scene_name):

    request.session['expe'] = expe_name
    request.session['scene'] = scene_name

    request.session['expe_started'] = False
    request.session['expe_finished'] = False

    request.session['qualities'] = api.get_scene_qualities(scene_name)
    # update unique timestamp each time new experience is launched
    request.session['timestamp'] = datetime.strftime(datetime.utcnow(), "%Y-%m-%d_%Hh%Mm%Ss")

    # TODO : add in cache ref_image
    # get reference image
    #ref_image = api.get_image(scene_name, 'max')
    # save ref image as list (can't save python object)
    #request.session['ref_img'] = np.array(ref_image).tolist()