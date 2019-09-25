# django imports
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404

# main imports
import os
import json
import base64
import random
import numpy as np
from datetime import datetime
import pickle 
import time
import zipfile
from io import BytesIO


# expe imports
from .expes.classes.quest_plus import QuestPlus
from .expes.classes.quest_plus import psychometric_fun

from .expes import run as run_expe

# image processing imports
import io
from PIL import Image

# module imports
from .utils import api
from .utils import functions

from .utils.processing import crop_images
from . import config as cfg


def get_base_data(expe_name=None):
    '''
    Used to store default data to send for each view
    '''
    data = {}

    data['BASE'] = settings.WEBEXPE_PREFIX_URL

    # if expe name is used
    if expe_name is not None:
        data['js'] = cfg.expes_configuration[expe_name]['js']

    return data


def expe_list(request):

    # get all scenes from dataset
    scenes = api.get_scenes()

    # get list of experiences
    expes = cfg.expe_name_list

    # by default user restart expe
    request.session['expe_started'] = False

    # get base data
    data = get_base_data()
    # expe data
    data['scenes'] = scenes
    data['expes']  = expes

    return render(request, 'expe/expe_list.html', data)


def indications(request):

    # get param 
    expe_name = request.GET.get('expe')

    # get base data
    data = get_base_data()
    # expe parameters
    data['expe_name']  = expe_name
    data['question']   = cfg.expes_configuration[expe_name]['text']['question']
    data['indication'] = cfg.expes_configuration[expe_name]['text']['indication']

    return render(request, 'expe/expe_indications.html', data)


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
        refresh_data(request, expe_name, scene_name)

    # refresh if scene_name changed
    if 'scene' not in request.session or scene_name != request.session.get('scene'):
        refresh_data(request, expe_name, scene_name)

    # create output folder for expe_result
    current_day = datetime.strftime(datetime.utcnow(), "%Y-%m-%d")
    results_folder = os.path.join(settings.MEDIA_ROOT, cfg.output_expe_folder_name_day.format(expe_name, current_day))

    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    result_filename = scene_name + '_' + request.session.get('id') + '_' + request.session.get('timestamp') +".csv"
    results_filepath = os.path.join(results_folder, result_filename)

    if not os.path.exists(results_filepath):
        output_file = open(results_filepath, 'w')
        functions.write_header_expe(output_file, expe_name)
    else:
        output_file = open(results_filepath, 'a')

    # TODO : add crontab task to erase generated img and model data
    # create `quest` object if not exists    
    models_folder = os.path.join(settings.MEDIA_ROOT, cfg.model_expe_folder.format(expe_name, current_day))

    if not os.path.exists(models_folder):
        os.makedirs(models_folder)

    model_filename = result_filename.replace('.csv', '.obj')
    model_filepath = os.path.join(models_folder, model_filename)

    # run expe method using `expe_name`
    function_name = 'run_' + expe_name

    try:
        run_expe_method = getattr(run_expe, function_name)
    except AttributeError:
        raise NotImplementedError("Run expe method `{}` not implement `{}`".format(run_expe.__name__, function_name))

    expe_data = run_expe_method(request, model_filepath, output_file)

    if request.session.get('expe_finished'):
        # reinit session as default value
        # here generic expe params
        del request.session['expe']
        del request.session['scene']
        del request.session['qualities']
        del request.session['timestamp']
        del request.session['answer_time']

        # specific current expe session params (see `config.py`)
        for key in cfg.expes_configuration[expe_name]['session_params']:
            del request.session[key]

    # get base data
    data = get_base_data(expe_name)
    # expe parameters
    data['expe_name']       = expe_name
    data['expe_data']       = expe_data
    data['end_text']        = cfg.expes_configuration[expe_name]['text']['end_text']

    return render(request, cfg.expes_configuration[expe_name]['template'], data)


@login_required(login_url="login/")
def list_results(request, expe=None):
    """
    Return all results obtained from experiences
    """

    if expe is None:
        folders = cfg.expe_name_list

        return render(request, 'expe/expe_results.html', {'expe': expe, 'folders': folders})

    else:
        if expe in cfg.expe_name_list:

            folder_path = os.path.join(settings.MEDIA_ROOT, cfg.output_expe_folder, expe)

            # init folder dictionnary
            folders = {}

            if os.path.exists(folder_path):
            
                days = sorted(os.listdir(folder_path), reverse=True)

                for day in days:
                    day_path = os.path.join(folder_path, day)
                    filenames = os.listdir(day_path)
                    folders[day] = filenames
        else:
            raise Http404("Expe does not exists")

    # get base data
    data = get_base_data()
    # expe parameters
    data['expe']    = expe
    data['folders'] = folders
    data['infos']   = cfg.expes_configuration[expe]['text']

    return render(request, 'expe/expe_results.html', data)


@login_required(login_url="login/")
def download_result(request):
    
    path = request.POST.get('path')
    folder_path = os.path.join(settings.MEDIA_ROOT, cfg.output_expe_folder, path)

    # Folder is required
    if os.path.exists(folder_path):

        # Open BytesIO to grab in-memory ZIP contents
        s = BytesIO()

        # check if file or folder
        if os.path.isdir(folder_path):
            
            # get files from a specific day
            filenames = os.listdir(folder_path)

            # Folder name in ZIP archive which contains the above files
            # E.g [thearchive.zip]/somefiles/file2.txt
            # FIXME: Set this to something better
            zip_subdir = folder_path.split('/')[-1]
            zip_filename = "%s.zip" % zip_subdir

            # The zip compressor
            zf = zipfile.ZipFile(s, "w")

            for fpath in filenames:
                
                fpath = os.path.join(folder_path, fpath)

                # Calculate path for file in zip
                fdir, fname = os.path.split(fpath)
                zip_path = os.path.join(zip_subdir, fname)

                # Add file, at correct path
                zf.write(fpath, zip_path)

            # Must close zip for all contents to be written
            zf.close()

            output_filename = zip_filename
            content = s.getvalue()

        else:
            
            with open(folder_path, 'rb') as f:
                content = f.readlines()

            # filename only
            fdir, fname = os.path.split(path)
            output_filename = fname

        # Grab ZIP file from in-memory, make response with correct MIME-type
        resp = HttpResponse(content, content_type="application/gzip")
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % output_filename

        return resp

    else:
        return Http404("Path does not exist")



def refresh_data(request, expe_name, scene_name):
    '''
    Utils method to refresh data from session
    '''
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


