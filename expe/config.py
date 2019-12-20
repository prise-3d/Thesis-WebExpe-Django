# main imports
import os

# env variables
WEB_API_PREFIX_URL_KEY         = 'WEB_API_PREFIX_URL'
WEB_API_PREFIX_URL             = os.environ.get(WEB_API_PREFIX_URL_KEY) \
                                 if os.environ.get(WEB_API_PREFIX_URL_KEY) is not None else 'api'

# api variables
DIRAN_DOMAIN_NAME              = "https://diran.univ-littoral.fr/"
GET_SCENE_QUALITIES_API_URL    = DIRAN_DOMAIN_NAME + WEB_API_PREFIX_URL + "/listSceneQualities?sceneName={0}"
GET_SCENE_IMAGE_API_URL        = DIRAN_DOMAIN_NAME + WEB_API_PREFIX_URL + "/getImage?sceneName={0}&imageQuality={1}"
GET_SCENES_API_URL             = DIRAN_DOMAIN_NAME + WEB_API_PREFIX_URL + "/listScenes"

# folder variables
# TODO : dispatch into day and experiment ID
model_expe_folder              = "expes_models/{0}/{1}"
output_expe_folder             = "expes_results"
output_expe_folder_date        = "expes_results/date"
output_expe_folder_id          = "expes_results/expeId"
output_expe_folder_name_id_day = "expes_results/expeId/{0}/{1}/{2}/{3}"
output_expe_folder_name_day    = "expes_results/date/{0}/{1}/{2}"
output_tmp_folder              = "tmp"

# expes list
expe_name_list                 = ["quest_one_image"]

# configure experiments labels
expes_configuration            = {

    # First experiments configuration
    'quest_one_image':{
        'scenes':['contemporary', 'bathroom'],
        'text':{
            'question': "Do you see one image or a composition of more than one?",
            'indication': "press RIGHT if you see 2 images, LEFT if not",
            'end_text': "Experience is finished. Thanks for your participation",
            'examples': {
                'sentence': ["First example of 2 images:\n This image is cropped {0}.\n {1}% on the left originating from a low-quality image and on the right originating from high quality. \n So, press RIGHT.", 
                             "Second example of 1 image: \n This image is cropped {0}. \n {1}% on the left originating from a high-quality image and on the right originating from high quality, too.\n So, press LEFT", 
                             "Third example of 2 images: \n This image is cropped {0}. \n {1}% on the upper part originating from a low-quality image and on the bottom originating from high quality. \n So, press RIGHT."],
                'crop_params': [
                    [0.3, 0, 0],
                    [0.3, 0, 0],
                    [0.7, 1, 0]
                ],
                'images': [
                    [2, -1],
                    [-3, -1],
                    [7, -1]
                ]
            }
        },
        'params':{
            'iterations': 100,
            'entropy': 5,
            'slopes':{
                'contemporary' : [0.0001, 0.001, 0.00003], #start, stop, step
                'bathroom' : [0.0005, 0.01, 0.0003], #start, stop, step
            },
        },
        
        # if others custom session param are directly set for experiments
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