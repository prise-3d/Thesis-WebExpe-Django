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
    if 'expe' not in request.session:
        request.session['expe'] = expe_name
        request.session['begin'] = True
    else:
        request.session['begin'] = False

    print(request.session.get('begin'))

    # update ref img at first time or expe changed
    if expe_name != request.session.get('expe'):
    #if 'ref_img' not in request.session or expe_name != request.session.get('expe'):
        request.session['begin'] = True
        request.session['qualities'] = api.get_scene_qualities(scene_name)
        # update unique timestamp each time new experience is launched
        request.session['timestamp'] = datetime.strftime(datetime.utcnow(), "%Y-%m-%d_%Hh%Mm%Ss")

        # TODO : add in cache ref_image
        # get reference image
        #ref_image = api.get_image(scene_name, 'max')
        # save ref image as list (can't save python object)
        #request.session['ref_img'] = np.array(ref_image).tolist()

    # construct new image
    quality = random.choice(request.session.get('qualities'))
    noisy_image = api.get_image(scene_name, quality)

    # reconstruct reference image from list stored into session
    # ref_image = Image.fromarray(np.array(request.session.get('ref_img')))
    ref_image = api.get_image(scene_name, 'max')
    img_merge, per, orien, swap_img = crop_images(noisy_image, ref_image)

    # create output folder for tmp files if necessary
    tmp_folder = os.path.join(settings.MEDIA_ROOT, cfg.output_tmp_folder)

    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)

    # generate tmp merged image (pass as BytesIO was complicated..)
    # TODO : add crontab task to erase generated img
    filepath_img = os.path.join(tmp_folder, request.session.get('id') + '_' + scene_name + '' + expe_name + '.png')
    img_merge.save(filepath_img)

    # create output folder for expe_result
    current_day = datetime.strftime(datetime.utcnow(), "%Y-%m-%d")
    results_folder = os.path.join(cfg.output_expe_folder.format(current_day))

    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    result_filename = expe_name + '_' + request.session.get('id') + '_' + request.session.get('timestamp') +".csv"
    results_filepath = os.path.join(results_folder, result_filename)

    if not os.path.exists(results_filepath):
        f = open(results_filepath, 'w')
        functions.write_header_expe(f, expe_name)
    else:
        f = open(results_filepath, 'a')

    #orientation : 0 = vertical, 1 = horizontal
    #image_ref_position : 0 = right/bottom, 1 = left/up
    #answer : left = 1, right = 0

    print("here")
    
    # expe parameters
    data = {
        'expe_name': expe_name,
        'img_merged_path': filepath_img,
        'question': cfg.expe_questions[expe_name]['question'],
        'indication': cfg.expe_questions[expe_name]['indication']
    }

    return render(request, 'expe/expe.html', data)


def run_quest_one_image():
    pass