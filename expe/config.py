# api variables
DIRAN_DOMAIN_NAME           = "https://diran.univ-littoral.fr/"
GET_SCENE_QUALITIES_API_URL = DIRAN_DOMAIN_NAME + "api/listSceneQualities?sceneName={0}"
GET_SCENE_IMAGE_API_URL     = DIRAN_DOMAIN_NAME + "api/getImage?sceneName={0}&imageQuality={1}"
GET_SCENES_API_URL          = DIRAN_DOMAIN_NAME + "api/listScenes"

# folder variables
model_expe_folder           = "expes_models/{0}/"
output_expe_folder          = "expes_results/{0}/"
output_tmp_folder           = "tmp"

# expes list
expe_name_list              = ["quest_one_image"]

# configure experiences labels
expe_questions              = {
    'quest_one_image':{
        'question': "Do you see one image or a composition of more than one?",
        'indication': "press left if you see one image, right if not"
    }
}