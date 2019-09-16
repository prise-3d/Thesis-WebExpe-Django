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
import datetime

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
    
    question_sentence  = "Do you see one image or a composition of more than one?"
    indication_sentence = "press left if you see one image, right if not"

    # get param 
    expe_name = request.GET.get('expe')
    scene_name = request.GET.get('scene')

    # first time expe is launched
    if 'expe' not in request.session:
        request.session['expe'] = expe_name
        request.session['begin'] = True
    else:
        request.session['begin'] = False

    # update ref img at first time or expe changed
    if 'ref_img' not in request.session or expe_name != request.session['expe']:
        request.session['begin'] = True
        request.session['qualities'] = api.get_scene_qualities(scene_name)
        request.session['id'] = functions.uniqueID()

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
    folder = os.path.join(settings.MEDIA_ROOT, cfg.output_tmp_folder)

    if not os.path.exists(folder):
        os.makedirs(folder)

    # generate tmp merged image (pass as BytesIO was complicated..)
    # TODO : add crontab task to erase generated img
    filepath_img = os.path.join(folder, request.session.get('id') + '_' + scene_name + '' + expe_name + '.png')
    img_merge.save(filepath_img)

    # create output folder for expe_result
    timestamp = datetime.strftime(datetime.utcnow(), "%Y-%m-%d_%Hh%Mm%Ss")
    filename += "online_ans" + timestamp +".csv"
    f = open(filename,"w")

    #orientation : 0 = vertical, 1 = horizontal
    #image_ref_position : 0 = right/bottom, 1 = left/up
    #answer : left = 1, right = 0
    f.write('stimulus' + ";" + "name_stimulus" + ";" + 'cropping_percentage' + ";" + 'orientation' + ';' 
            + 'image_ref_position' + ';' + 'answer' + ';' + 'time_reaction' + ';' + 'entropy' + '\n')
    
    # expe parameters
    data = {
        'expe_name': expe_name,
        'img_merged_path': filepath_img,
        'question': question_sentence,
        'indication': indication_sentence
    }

    return render(request, 'expe/expe.html', data)