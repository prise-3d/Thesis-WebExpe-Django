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
label_expe_list                = {
                                    'fr' : 'Choisissez une expérience',
                                    'en' : 'Select an experiment'
                                }
submit_button                  = {
                                    'fr' : 'Valider',
                                    'en' : 'Submit'
                                }

expe_name_list                 = ["quest_one_image"]

# configure experiments labels
expes_configuration            = {

    # First experiments configuration
    'quest_one_image':{
        # do not forget to add slopes and new scenes is added for this experiment
        'scenes':['contemporary', 'bathroom', 'p3d_kitchen_800_800'], 
        'expected_duration': 40,
        'forms':{
            'end_form':{
                'fr': {
                    'button': 'Suivant',
                    'questions':[
                        {
                            'question': "Diriez-vous que vous avez passé cette expérience dans de bonnes conditions ? ",
                            'name': "condition",
                            'answers':[
                                {
                                    'label': 'Oui',
                                    'value': 'Yes'
                                },
                                {
                                    'label': 'Non',
                                    'value': 'No'
                                },
                            ]
                        },
                        {
                            'question': "Avez-vous passé cette expérience avec la lumière du jour ?",
                            'name': "dark",
                            'answers':[
                                {
                                    'label': 'Oui',
                                    'value': 'Yes'
                                },
                                {
                                    'label': 'Non',
                                    'value': 'No'
                                },
                            ]
                        },
                        {
                            'question': "Si vous portez d’habitude des lentilles ou des lunettes, les portiez-vous durant cette expérience ? ",
                            'name': "glasses",
                            'answers':[
                                {
                                    'label': 'Oui',
                                    'value': 'Yes'
                                },
                                {
                                    'label': 'Non',
                                    'value': 'No'
                                },
                                {
                                    'label': 'Je ne porte ni lentilles ni lunettes.',
                                    'value': 'Good'
                                }
                            ]
                        },
                        {
                            'question': "Pouvons-nous avoir confiance dans vos réponses ?",
                            'name': "trust",
                            'answers':[
                                {
                                    'label': 'Oui',
                                    'value': 'Yes'
                                },
                                {
                                    'label': 'Non',
                                    'value': 'No'
                                }
                            ]
                        },
                        {
                            'question': "Sur quelle flèche du clavier appuyez-vous lorsque vous pensez qu’il n’y a qu’une seule image ?",
                            'name': 'attention',
                            'answers':[
                                {
                                    'label': 'Gauche',
                                    'value': 'Left'
                                },
                                {
                                    'label': 'Droite',
                                    'value': 'Right'
                                }
                            ]
                        },
                    ]
                },
                            
                'en':{
                    'button': 'Next',
                    'questions':[
                        {
                            'question': "Did you carry out this experiment under good conditions?",
                            'name': "condition",
                            'answers':[
                                {
                                    'label': 'Yes',
                                    'value': 'Yes'
                                },
                                {
                                    'label': 'No',
                                    'value': 'No'
                                },
                            ]
                        },
                        {
                            'question': "Did you perform this experiment with daylight?",
                            'name': "dark",
                            'answers':[
                                {
                                    'label': 'Yes',
                                    'value': 'Yes'
                                },
                                {
                                    'label': 'No',
                                    'value': 'No'
                                },
                            ]
                        },
                        {
                            'question': "If you wear glasses/lenses, did you have them during the experiment?",
                            'name': "glasses",
                            'answers':[
                                {
                                    'label': 'Yes',
                                    'value': 'Yes'
                                },
                                {
                                    'label': 'No',
                                    'value': 'No'
                                },
                                {
                                    'label': 'I do not wear glasses/lenses',
                                    'value': 'Good'
                                }
                            ]
                        },
                        {
                            'question': "Should we trust your answers?",
                            'name': "trust",
                            'answers':[
                                {
                                    'label': 'Yes',
                                    'value': 'Yes'
                                },
                                {
                                    'label': 'No',
                                    'value': 'No'
                                }
                            ]
                        },
                        {
                            'question': "What is the answer when you see one image with the same quality everywhere?",
                            'name': 'attention',
                            'answers':[
                                {
                                    'label': 'Left',
                                    'value': 'Left'
                                },
                                {
                                    'label': 'Right',
                                    'value': 'Right'
                                }
                            ]
                        },
                    ]
                }
            }
        },
        'text':{
            'next' : {
                'fr': "Appuyer sur \"entrer\" pour continuer.",
                'en': "Please press enter to continue"
            },
            'presentation' : {
                'fr': "De nos jours, nous utilisons de plus en plus souvent des images générées par ordinateur. " +
                      "Mais ces images ne sont pas toujours parfaites. \n" +
                      "Nous avons conçu une expérience pour savoir si vous êtes capable de détecter des différences de qualité dans une image.",
                'en': "The computer generated images are widely used nowadays." +
                      "\n We have designed an experiment that will allow you to find out whether you are capable of detecting aberrations in computer generated images. " +
                      "\n \n We will show you some computer generated images." +
                      "For each one we will ask you to report whether you think it comes from a single image, " +
                      "with the same quality everywhere, or whether you think it is in fact composed of two images " +
                      "with different qualities. \n \n " +
                      "The images were cut either horizontally or vertically (always side to side) " +
                      "and merged with a portion of another image that has either a different or the same quality. " +
                      "It is important to note that images are always cut from one side to the next.\n "
            },
            'question': {
                'fr': "Voyez-vous une image ayant la même qualité partout ou une image composée de deux parties " +
                      "d’images de qualité différentes ? \n \n " +
                      "Attention, nous ne vous demandons pas de juger la qualité générale de l’image. " +
                      "Aucune image n’est parfaite et c’est ce qui fait la difficulté de la tâche.",
                'en':"Do you think that you are viewing a single image with the same quality everywhere, " +
                     "or instead a composition of two images with different qualities?\n \n " +
                     "Please be aware that we do not ask you to report the overall quality of the image. " +
                     "None of the images you will see are perfect, and this is part of the difficulty of this task."
            },
            'indication': {
                'fr': "Il faut appuyer sur la flèche de gauche (&#8592;) si vous pensez qu’il n’y a qu’une seule image " + 
                      "et sur la flèche de droite (&#8594;) si vous pensez que l’image est composée de deux parties de qualité différentes.",
                'en': "Press the LEFT key (&#8592;) if you think the image comes from a single one, or the RIGHT key (&#8594;) " +
                      "if you think the image is composed of two subparts with different qualities."
            },
            'beginning':{
                'fr': ["Nous arrivons au début de l’expérience. L’expérience dure environ {0} minutes. Vous ne pouvez pas dépasser {1} minutes.",
                       "Merci de nous indiquer votre genre (Femme, Homme, Autre), votre année de naissance, votre nationalité, et un code si vous en avez reçu un.",
                       "A la fin de l’expérience nous vous donnerons un identifiant qui vous permettra d’obtenir votre récompense."
                ],
                'en': ['This is the beginning of this study. The expected duration is about {0} minutes. The maximum duration to conclude the experiment is {1} minutes.',
                        'Please enter the following information before starting the experiment.',
                        'At the end of the experiment, you will be given an identifier. This identifier will allow you to receive your reward.'
                ]
            },
            'end_indication_note':{
                'fr': "Note : les informations fournies sont strictement anonymes et ne seront utilisés que dans le cadre de cette recherche.",
                'en': "Note: The information you provide during this experiment is strictly anonymous. It will only be used for this particular research."
            },
            'end_text': {
                'thanks': {
                        'fr': "L’expérience est terminée. Merci pour votre participation.",
                        'en':"Experience is finished. Thanks for your participation!",
                        },
                'results': {
                        'fr': ["Félicitations, vous faites partie des 25% de la population qui peut parfaitement voir les détails d’une image !",
                               "Bravo, vous êtes dans la moyenne de la population. La plupart des gens sont comme vous et peuvent voir les détails d’une image !",
                               "Vous faites parties des 25% de la population pour qui les images ont toujours l’air parfaites !"
                               ],
                        'en': ["Congratulations, you are part of the 25% of the population that can detect all the details in a scene and perceive perfectly the aberrations!",
                               "Bravo, you are part of the average population. Most people see as you do and you can detect details in a scene and perceive aberrations in an image.",
                               "You are part of the 25% of the population for whom the images always look perfect for you!"                               
                               ]
                },
                'reward':{
                        'prolific' : {
                                'fr' : "Ne quittez pas cette page, vous allez être redirigé vers Prolific dans : ",
                                'en' : "Please don't leave this page, you will be automatically redirect in : "
                                },
                        'default':
                            {
                                'fr' : 'Pour recevoir votre récompense notez bien votre identifiant : ',
                                'en' : 'To receive your reward, please make sure to note the following identifier :'
                            }
                            
                        }
            },
            
            'finished' : {
                    'fr' : "Vous avez déjà réalisé toutes les scènes disponibles. \n Merci de bien noter votre identifiant : ",
                    'en' : "You have already done all available experiments. \nPlease make sure to note the following identifier : "
            },
            
            'info_participant' : {
                    'gender' : {
                          'fr' : 'Genre',
                          'en' : 'Gender'    
                    },
                    'birth_year' : {
                          'fr' : 'Année de naissance',
                          'en' : 'Birth year'  
                    },
                    'nationality' : {
                          'fr' : 'Nationalité',
                          'en' : 'Nationality'  
                    },
                    'code' : {
                          'fr' : 'Code (facultatif)',
                          'en' : 'Code (optional)'  
                    }
            },
                    
            'examples': {
                'sentence': {
                    'fr': ["Voyons quelques exemples pour illustrer la tâche !\n Exemple 1 (sur 6) : ", 
                           
                           "La réponse est : deux parties de qualité différentes !  \n" +
                           "L’image est coupée {0}. La bande de gauche vient d’une image de basse qualité, " +
                           "la partie droite à une meilleure qualité. Il faut donc presser la flèche DROITE (&#8594;)",

                           "Exemple 2 (sur 6) : ",
                           
                           "La réponse est « une seule image » \n " +
                           "L’image n’a pas deux parties de qualité différentes. \n" +
                           "Attention, même si vous pensez que l’image n’est pas parfaite, " +
                           "ce qui compte c’est que la qualité soit la même partout. \n Il faut donc presser la flèche de GAUCHE (&#8592;)",

                           "Exemple 3 (sur 6) : ",
                           
                           "L’image est composée de deux images de qualité différentes ! \n" +
                           "L’image est coupée {0}. La partie haute vient d’une image de basse qualité, " +
                           "la partie basse a une meilleure qualité. \n Il faut donc presser la flèche DROITE (&#8594;)",
                           
                           "Exemple 4 (sur 6) : ",
                           
                           
                           "L’image est composée de deux images de qualité différentes ! \n" +
                           "L’image est coupée {0}. La partie haute vient d’une image de basse qualité, " +
                           "la partie basse a une meilleure qualité. \n Il faut donc presser la flèche DROITE (&#8594;)",
                           
                           "Exemple 5 (sur 6) : ",
                           
                           
                           "L’image est composée de deux images de qualité différentes ! \n" +
                           "L’image est coupée {0}. La partie basse vient d’une image de basse qualité, " +
                           "la partie haute a une meilleure qualité. \n Il faut donc presser la flèche DROITE (&#8594;)",
                           
                           "Exemple 6 (sur 6) : ",
                           
                           "Ici la différence entre les deux parties de l’image est plus difficile à détecter mais il y a bien deux parties de qualité différentes ! \n " +
                           "Il faut faire attention aux détails. \n L’image est coupée {0}. La bande de gauche est de basse qualité, " +
                           "la partie droite a une meilleure qualité. \n \n Il faut donc presser la flèche DROITE (&#8594;)",
                           ],
    
                    'en': ["Let's see some examples to illustrate the task! \n Example 1 from 6 : ", 
                           
                             "The image is composed of two subparts with different qualities! \n" +
                             "This image is cropped {0} with {1}% on the left coming from a low-quality image " +
                             "and the right part coming from a high quality image. \n So, here, you should press RIGHT (&#8594;).",
                             
                             "Example 2 from 6 : ",
                             
                             "The answer is \"a single image\"! \n " +
                             "This image is not cropped, the quality is the same everywhere. \n " +
                             "Please be aware that even if the image is not perfect, the overall quality "+
                             "is the same for the whole image!\n Pay attention to the details !\n Here, you should press LEFT (&#8592;).", 
                             
                             "Example 3 from 6 : ",
                             
                             "The image is composed of two subparts with different qualities! \n " +
                             "This image is cropped {0}. \n {1}% on the upper part comes from a low-quality image " +
                             "and the bottom part comes from a high quality image. \n So, here, you should press RIGHT (&#8594;).",
                             
                             "Example 4 from 6 : ",
                             
                             "The image is composed of two subparts with different qualities! \n " +
                             "This image is cropped {0}. \n {1}% on the upper part comes from a low-quality image " +
                             "and the bottom part comes from a high quality image. \n So, here, you should press RIGHT (&#8594;).",
                             
                             "Example 5 from 6 : ",
                             
                             "The image is composed of two subparts with different qualities! \n " +
                             "This image is cropped {0}. \n {1}% on the upper part comes from a high-quality image " +
                             "and the bottom part comes from a low-quality quality image.\n So, here, you should press RIGHT (&#8594;).",
                             
                             "Example 6 from 6 : ",
                             "Even if it is more difficult to detect it, the images is composed of two subparts with different qualities! \n " +
                             "Pay attention to the details ! \n This image is cropped {0}. \n {1}% on the left " +
                             "comes from a low-quality image and the right part comes from a high quality image.\n  \n " +
                             "So, here, you should press RIGHT (&#8594;).",
                             ]
                },  
                'cut_name' : {
                        'fr': ["verticalement", "horizontalement"],
                        'en': ["vertically", "horizontally"]
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
            'min_iterations': 2,
            'max_iterations': 5,
            'max_time': 105, #minutes
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
                'fr': "Cochez cette case pour continuer l'expérience",
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
