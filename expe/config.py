# main imports
import os

# env variables
WEB_API_PREFIX_URL_KEY       = 'WEB_API_PREFIX_URL'
WEB_API_PREFIX_URL           = os.environ.get(WEB_API_PREFIX_URL_KEY) \
                               if os.environ.get(WEB_API_PREFIX_URL_KEY) is not None else 'api'

# api variables
DIRAN_DOMAIN_NAME            = "https://diran.univ-littoral.fr/"
GET_SCENE_QUALITIES_API_URL  = DIRAN_DOMAIN_NAME + WEB_API_PREFIX_URL + "/listSceneQualities?sceneName={0}"
GET_SCENE_IMAGE_API_URL      = DIRAN_DOMAIN_NAME + WEB_API_PREFIX_URL + "/getImage?sceneName={0}&imageQuality={1}"
GET_SCENES_API_URL           = DIRAN_DOMAIN_NAME + WEB_API_PREFIX_URL + "/listScenes"

# folder variables
model_expe_folder            = "expes_models/{0}/{1}"
output_expe_folder           = "expes_results"
output_expe_folder_name_day  = "expes_results/{0}/{1}"
output_tmp_folder            = "tmp"

# expes list
expe_name_list              = ["quest_one_image"]

# configure experiences labels
expes_configuration         = {

    # First experience configuration
    'quest_one_image':{
        'text':{
            'question': "Do you see one image or a composition of more than one?",
            'indication': "press left if you see one image, right if not",
            'end_text': "Experience is finished. Thanks for your participation",
        },
        'params':{
            'iterations': 10
        },
       
        # if others custom session param are directly set for experience
        'session_params': [
            'expe_data',
        ],

        # template file used in django `expe` route
        'template': 'expe/expe.html',

        # javascript file used
        'javascript':[
            'loadImg.js',
            'keyEvents.js'
        ],
        'output_header': 
            "stimulus;name_stimulus;cropping_percentage;orientation;image_ref_position;answer;time_reaction;entropy\n"
    }
}