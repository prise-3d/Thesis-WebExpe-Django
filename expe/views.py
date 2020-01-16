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
from PIL import Image, ImageDraw

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
        data['javascript'] = cfg.expes_configuration[expe_name]['javascript']

    return data


def expe_list(request):

    # get all scenes from dataset
    scenes = api.get_scenes()

    # get list of experimentss
    expes = cfg.expe_name_list
    data = get_base_data()

    # by default user restart expe
    request.session['expe_started'] = False

    # get base data
    data = get_base_data()
    # expe data
    data['scenes'] = scenes
    data['expes']  = expes
    
    #data['scenes'] = {}
    #for expe in expes:
    #    if 'scene' in cfg.expes_configuration[expe]:
    #        data['scenes'][expe] = cfg.expes_configuration[expe]['scenes']
    #    else:
    #        data['scenes'][expe] = scenes
            
    return render(request, 'expe/expe_list.html', data)


def indications(request):

    #random.seed(10)

    # get param 
    expe_name = request.GET.get('expe')
    

    
    scene_name = None
    if 'scene' in request.GET:
        scene_name = request.GET.get('scene')
    
    if scene_name is None or scene_name == 'null':
        scene_name = random.choice(cfg.expes_configuration[expe_name]['scenes'])
        
    example_number = request.GET.get('example')

    print(example_number)

    # get base data
    data = get_base_data()
    # expe parameters
    data['expe_name']  = expe_name
    data['scene_name'] = scene_name
    data['question']   = cfg.expes_configuration[expe_name]['text']['question']
    data['indication'] = cfg.expes_configuration[expe_name]['text']['indication']

    number_of_examples = len(cfg.expes_configuration[expe_name]['text']['examples']['images'])

    start_experiment = False
    if (int(example_number) >= number_of_examples):
        start_experiment = True
    else:
         # run expe method using `expe_name`
        function_name = 'example_' + expe_name
    
        try:
            run_example_method = getattr(run_expe, function_name)
        except AttributeError:
            raise NotImplementedError("Run expe method `{}` not implement `{}`".format(run_expe.__name__, function_name))
    
        data_example = run_example_method(request, expe_name, scene_name)
        data.update(data_example)
         
        # get expected image qualities indices (load noisy and ref image)
#        params_image = cfg.expes_configuration[expe_name]['text']['examples']['images'][int(example_number)]
#        qualities = api.get_scene_qualities(scene_name)
#
#        noisy_quality = qualities[params_image[0]]
#        ref_quality = qualities[params_image[1]]
#
#        noisy_image = api.get_image(scene_name, noisy_quality)
#        ref_image = api.get_image(scene_name, ref_quality)
#
#        # get crop params from configuration
#        crop_params = cfg.expes_configuration[expe_name]['text']['examples']['crop_params'][int(example_number)]
#
#        img_merge, percentage, orientation, position = crop_images(noisy_image,     
#                                                                    ref_image, 
#                                                                    per=crop_params[0], 
#                                                                    orien=crop_params[1], 
#                                                                    swap_img=crop_params[2])
#        width, height = img_merge.size
#        if orientation==0:
#            left, top, right, bottom = percentage*width, 0, percentage*width, height   #vertical
#        else:
#            left, top, right, bottom = 0, percentage*height, width, percentage*height   #horizontal
#        if  int(example_number) % 2 != 0 :
#            if noisy_quality != qualities[-1]:#-noisy_quality > qualities[-1]-(10*qualities[-1])/100 :
#                draw = ImageDraw.Draw(img_merge) 
#                draw.line((left, top, right, bottom), fill='black', width=5)
#        example_sentence = cfg.expes_configuration[expe_name]['text']['examples']['sentence'][int(example_number)]
#
#        if orientation == 0:
#            example_sentence = example_sentence.format('vertically', str(percentage*100))
#        else:
#            example_sentence = example_sentence.format('horizontally', str(percentage*100))
#
#        data['example_sentence'] = example_sentence
#
#
#        # Temporary save of image
#        tmp_folder = os.path.join(settings.MEDIA_ROOT, cfg.output_tmp_folder)
#
#        if not os.path.exists(tmp_folder):
#            os.makedirs(tmp_folder)
#
#        # generate tmp merged image (pass as BytesIO was complicated..)
#        filepath_img = os.path.join(tmp_folder, 'example_' + scene_name + '' + expe_name + '.png')
#        
#        # replace img_merge if necessary (new iteration of expe)
#        if img_merge is not None:
#            img_merge.save(filepath_img)
#
#        print(filepath_img)
#        data['example'] = filepath_img

    data['start'] = start_experiment

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

    user_identifier = request.session.get('id')
    experiment_id = request.session.get('experimentId')

    print("ExperimentId is : " + experiment_id)

    # check if experimentId is used or not
    if len(experiment_id) == 0:
        output_expe_folder = cfg.output_expe_folder_name_day.format(expe_name, current_day, user_identifier)
    else:
        output_expe_folder = cfg.output_expe_folder_name_id_day.format(expe_name, experiment_id, current_day, user_identifier)

    results_folder = os.path.join(settings.MEDIA_ROOT, output_expe_folder)
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    result_filename = scene_name + '_' + request.session.get('timestamp') +".csv"
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
        del request.session['experimentId']
        del request.session['qualities']
        del request.session['timestamp']

        # specific current expe session params (see `config.py`)
        for key in cfg.expes_configuration[expe_name]['session_params']:
            del request.session[key]

    # set expe current data into session (replace only if experiments data changed)
    if expe_data is not None:
        request.session['expe_data'] = expe_data

        # get base data
    data = get_base_data(expe_name)

    # other experimentss information
    data['expe_name']            = expe_name
    data['end_text']             = cfg.expes_configuration[expe_name]['text']['end_text']

    return render(request, cfg.expes_configuration[expe_name]['template'], data)


@login_required(login_url="login/")
def list_results(request, expe=None):
    """
    Return all results obtained from experimentss
    """

    if expe is None:
        folders = cfg.expe_name_list

        return render(request, 'expe/expe_results.html', {'expe': expe, 'folders': folders})

    else:
        if expe in cfg.expe_name_list:

            folder_date_path = os.path.join(settings.MEDIA_ROOT, cfg.output_expe_folder_date, expe)
            folder_id_path   = os.path.join(settings.MEDIA_ROOT, cfg.output_expe_folder_id, expe)

            # extract date files
            folders_date = {}

            if os.path.exists(folder_date_path):
            
                days = sorted(os.listdir(folder_date_path), reverse=True)

                # get all days
                for day in days:
                    day_path = os.path.join(folder_date_path, day)
                    users = os.listdir(day_path)

                    folders_user = {}
                    # get all users files
                    for user in users:
                        user_path = os.path.join(day_path, user)
                        filenames = os.listdir(user_path)
                        folders_user[user] = filenames
                    
                    # attach users to this day
                    folders_date[day] = folders_user

            # extract expe id files
            folders_id = {}

            if os.path.exists(folder_id_path):
                
                ids = sorted(os.listdir(folder_id_path), reverse=True)

                # get all days
                for identifier in ids:
                    id_path = os.path.join(folder_id_path, identifier)
                    days = sorted(os.listdir(id_path), reverse=True)

                    folder_days = {}
                    # get all days
                    for day in days:
                        day_path = os.path.join(id_path, day)
                        users = os.listdir(day_path)

                        folders_user = {}
                        # get all users files
                        for user in users:
                            user_path = os.path.join(day_path, user)
                            filenames = os.listdir(user_path)
                            folders_user[user] = filenames
                        
                        # attach users to this day
                        folder_days[day] = folders_user

                    folders_id[identifier] = folder_days

            folders = { 'date': folders_date, 'expeId': folders_id}
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
    # update unique timestamp each time new experiments is launched
    request.session['timestamp'] = datetime.strftime(datetime.utcnow(), "%Y-%m-%d_%Hh%Mm%Ss")

    # retrieve and store experimentId
    expe_id = request.GET.get('experimentId')
    request.session['experimentId'] = expe_id

    # TODO : add in cache ref_image
    # get reference image
    #ref_image = api.get_image(scene_name, 'max')
    # save ref image as list (can't save python object)
    #request.session['ref_img'] = np.array(ref_image).tolist()


