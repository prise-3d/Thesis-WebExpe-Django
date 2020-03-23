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
        'scenes':['contemporary', 'bathroom', 'p3d_kitchen_800_800'], 
        'expected_duration': 40,
        'text':{
            'presentation' : 
            {
                'fr': "presentation : TODO",
                'en': "The computer generated images are widely used nowadays. \n We have designed an experiment that will allow you to find out whether you are capable of detecting aberrations in computer generated images. \n \n We will show you some computer generated images. For each one we will ask you to report whether you think it comes from a single image, with the same quality everywhere, or whether you think it is in fact composed of two images with different qualities. \n \n The images were cut either horizontally or vertically (always side to side) and merged with a portion of another image that has either a different or the same quality. It is important to note that images are always cut from one side to the next.\n "
            },
            'question': {
                'fr': 'question : TODO',
                'en':"Do you think that you are viewing a single image with the same quality everywhere, or instead a composition of two images with different qualities?\n \n Please be aware that we do not ask you to report the overall quality of the image. None of the images you will see are perfect, and this is part of the difficulty of this task."
            },
            'indication': {
                'fr': 'indication : TODO',
                'en': "Press the LEFT key (&#8592;) if you think the image comes from a single one, or the RIGHT key (&#8594;) if you think the image is composed of two subparts with different qualities."
            },
            'end_text': {
                'fr': "end text : TODO",
                'en':"Experience is finished. Thanks for your participation!",
            },
            'examples': {
                'sentence': {
                    'fr': ["Let's see some examples to illustrate the task! \n Example 1 from 6 : ", 
                             "The image is composed of two subparts with different qualities! \n This image is cropped {0} with {1}% on the left coming from a low-quality image and the right part coming from a high quality image. \n So, here, you should press RIGHT.",
                             "Example 2 from 6 : ",
                             "The answer is \"a single image\"! \n This image is not cropped, the quality is the same everywhere. \n Please be aware that even if the image is not perfect, the overall quality is the same for the whole image!\n Pay attention to the details !\n Here, you should press LEFT.", 
                             "Example 3 from 6 : ",
                             "The image is composed of two subparts with different qualities! \n This image is cropped {0}. \n {1}% on the upper part comes from a low-quality image and the bottom part comes from a high quality image. \n So, here, you should press RIGHT.",
                             "Example 4 from 6 : ",
                             "The image is composed of two subparts with different qualities! \n This image is cropped {0}. \n {1}% on the upper part comes from a low-quality image and the bottom part comes from a high quality image. \n So, here, you should press RIGHT.",
                             "Example 5 from 6 : ",
                             "The image is composed of two subparts with different qualities! \n This image is cropped {0}. \n {1}% on the upper part comes from a high-quality image and the bottom part comes from a low-quality quality image.\n So, here, you should press RIGHT.",
                             "Example 6 from 6 : ",
                             "Even if it is more difficult to detect it, the images is composed of two subparts with different qualities! \n Pay attention to the details ! \n This image is cropped {0}. \n {1}% on the left comes from a low-quality image and the right part comes from a high quality image.\n  \n So, here, you should press RIGHT.",
                             ],
                    'en': ["Let's see some examples to illustrate the task! \n Example 1 from 6 : ", 
                             "The image is composed of two subparts with different qualities! \n This image is cropped {0} with {1}% on the left coming from a low-quality image and the right part coming from a high quality image. \n So, here, you should press RIGHT.",
                             "Example 2 from 6 : ",
                             "The answer is \"a single image\"! \n This image is not cropped, the quality is the same everywhere. \n Please be aware that even if the image is not perfect, the overall quality is the same for the whole image!\n Pay attention to the details !\n Here, you should press LEFT.", 
                             "Example 3 from 6 : ",
                             "The image is composed of two subparts with different qualities! \n This image is cropped {0}. \n {1}% on the upper part comes from a low-quality image and the bottom part comes from a high quality image. \n So, here, you should press RIGHT.",
                             "Example 4 from 6 : ",
                             "The image is composed of two subparts with different qualities! \n This image is cropped {0}. \n {1}% on the upper part comes from a low-quality image and the bottom part comes from a high quality image. \n So, here, you should press RIGHT.",
                             "Example 5 from 6 : ",
                             "The image is composed of two subparts with different qualities! \n This image is cropped {0}. \n {1}% on the upper part comes from a high-quality image and the bottom part comes from a low-quality quality image.\n So, here, you should press RIGHT.",
                             "Example 6 from 6 : ",
                             "Even if it is more difficult to detect it, the images is composed of two subparts with different qualities! \n Pay attention to the details ! \n This image is cropped {0}. \n {1}% on the left comes from a low-quality image and the right part comes from a high quality image.\n  \n So, here, you should press RIGHT.",
                             ]
                },          
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
            'min_iterations': 200,
            'max_iterations': 250,
            'max_time': 90, #minutes
            'entropy': 0.05,
            'thresholds':{
                'contemporary' : [50, 20000, 100], #start, stop (non inclusive), step
                'bathroom' : [10, 2000, 20], #start, stop, step
                'p3d_kitchen_800_800' : [20,10000,40],
            },
            'slopes':{
                'contemporary' : [0.0001, 0.001, 0.00003], #start, stop, step
                'bathroom' : [0.0005, 0.01, 0.0003], #start, stop, step
                'p3d_kitchen_800_800' : [0.00001, 0.001, 0.00003], #start, stop, step
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
            'text':  {
                'fr': 'checkbox : TODO',
                'en': 'check the box and continue the experiment'
            }
        },

        # template file used in django `expe` route
        'template': 'expe/expe.html',

        # javascript file used
        'javascript':[
            'loadImg.js',
            'keyEvents.js'
        ],
        'output_header': 
            "stimulus;name_stimulus;cropping_percentage;orientation;image_ref_position;answer;time_reaction;entropy;checkbox\n",
        'redirect' :
            "https://app.prolific.co/submissions/complete?cc=51785F52"
    }
}
