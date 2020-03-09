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
        # do not forget to add slopes and new scenes is added for this experiment
        'scenes':['contemporary', 'bathroom'], 
        'expected_duration': 30,
        'text':{
            'presentation' : "The computer generated images are widely used nowadays. \n We have designed an experiment that will allow you to find out at which level you are capable of detecting the aberration in a scene. \n \n The question that you have to answer is if you see one image with the same quality everywhere or  composition of more than one image with different qualities. \n \n The images were cut horizontally or vertically (always side to side) and merged with an image from a different or same quality.\n It can't be a square in the middle of the image, it is always from one end to the other.",
            'question': "Do you see one image with the same quality everywhere or composition of more than one image with different qualities? \n \n Please be aware that we do not ask you to detect if the image is blurred. All the images are blurred more or less and this is part of the difficulty of the task.",
            'indication': "press LEFT is you see the same quality, RIGHT if not",
            'end_text': "Experience is finished. Thanks for your participation!",
            'examples': {
                'sentence': ["Let's see some examples! \n Example 1 from 6 : ", 
                             "The answer is composition with different qualities! \n This image is cropped {0}.\n {1}% on the left originating from a low-quality image and on the right originating from high quality. \n So, press RIGHT.",
                             "Example 2 from 6 : ",
                             "The answer is the same quality! \n This image is cropped {0} but there is not any difference in the quality because \n {1}% on the left originating from a high-quality image and on the right originating from the same quality.\n Please be aware that even if the image is blurred, there is not a difference in the blur level! \n So, press LEFT.", 
                             "Example 3 from 6 : ",
                             "The answer is composition with different qualities! \n This image is cropped {0}. \n {1}% on the upper part originating from a low-quality image and on the bottom originating from high quality. \n So, press RIGHT.",
                             "Example 4 from 6 : ",
                             "The answer is composition with different qualities! \n This image is cropped {0}. \n {1}% on the upper part originating from a low-quality image and on the bottom originating from high quality. \n So, press RIGHT.",
                             "Example 5 from 6 : ",
                             "The answer is composition with different qualities! \n This image is cropped {0}. \n {1}% on the upper part originating from a high-quality image and on the bottom originating from a low-quality quality image.\n So, press RIGHT.",
                             "Example 6 from 6 : ",
                             "Even if it is more difficult to detect the difference the answer is composition with different qualities! \n Pay attention to the details ! \n This image is cropped {0}. \n {1}% on the left originating from a low-quality image and on the right originating from a high quality image.\n  \n So, press RIGHT.",
                             ],
                'crop_params': [
                    [0.3, 0, 0],
                    [0.3, 0, 0],
                    [0.3, 0, 0],
                    [0.3, 0, 0],
                    [0.7, 1, 0],
                    [0.7, 1, 0],
                    [0.2, 1, 0],
                    [0.2, 1, 0],
                    [0.8, 1, 1],
                    [0.8, 1, 1],
                    [0.2, 0, 0],
                    [0.2, 0, 0]
                ],
                'images': [
                    [1, -1],
                    [1, -1],
                    [-1, -1],
                    [-1, -1],
                    [15, -1],
                    [15, -1],
                    [25, -1],
                    [25, -1],
                    [40, -1],
                    [40, -1],
                    [50, -1],
                    [50, -1]
                ]
            }
        },
        'params':{
            'min_iterations': 15,
            'max_iterations': 20,
            'max_time': 90, #minutes
            'entropy': 0.2,
            'thresholds':{
                'contemporary' : [50, 20050, 50], #start, stop (non inclusive), step
                'bathroom' : [10, 2010, 10], #start, stop, step
            },
            'slopes':{
                'contemporary' : [0.0001, 0.001, 0.00003], #start, stop, step
                'bathroom' : [0.0005, 0.01, 0.0003], #start, stop, step
            },
        },
        
        # if others custom session param are directly set for experiments
        'session_params': [
            'expe_data',
        ],

        'checkbox': {
            # display checkbox every `n` iterations
            'frequency': 20, 
             # expected text to be develop
            'text': 'check the box and continue the experiment'
        },

        # template file used in django `expe` route
        'template': 'expe/expe.html',

        # javascript file used
        'javascript':[
            'loadImg.js',
            'keyEvents.js'
        ],
        'output_header': 
            "stimulus;name_stimulus;cropping_percentage;orientation;image_ref_position;answer;time_reaction;entropy;checkbox\n"
    }
}
