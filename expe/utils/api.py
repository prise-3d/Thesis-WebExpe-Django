# main imports 
import os
import requests
import json

# image processing imports
from io import BytesIO
from PIL import Image 

# import config variables
from ..config import GET_SCENE_IMAGE_API_URL, GET_SCENE_QUALITIES_API_URL, GET_SCENES_API_URL
from ..config import DIRAN_DOMAIN_NAME

def get_image(scene, img_quality):
    '''
    Return specific image of scene dataset with quality
    '''
    if not type(img_quality) == str:
        img_quality = str(img_quality)

    # get URL to contact
    url = GET_SCENE_IMAGE_API_URL.format(scene, img_quality)
    # Make a get request to get information of scene image with quality of 200
    response = requests.get(url)
    # Print the content of the response formatted into JSON
    content_json = json.loads(response.content)
    
    # Access to link of image using 'key' (data & link) from json data
    api_link = content_json['data']['link']
    image_url = DIRAN_DOMAIN_NAME + api_link
    print(image_url)
    
    # Ask API to get acess to image
    response_img = requests.get(image_url)
    
    # Convert content of the response (the whole image) and parse it using BytesIO
    print("Access to image located at : ", image_url)
    return Image.open(BytesIO(response_img.content))   


def get_scene_qualities(scene):
    '''
    Return all qualities known from scene
    '''

    # construct `url` to get qualities
    url = GET_SCENE_QUALITIES_API_URL.format(scene)

    response = requests.get(url)
    # Print the content of the response formatted into JSON
    content_json = json.loads(response.content)

    # return list of qualities
    return content_json['data']


def get_scenes():
    '''
    Return list of scenes available into dataset
    '''

    url = GET_SCENES_API_URL

    # get scene list
    response = requests.get(url)

    # Print the content of the response formatted into JSON
    content_json = json.loads(response.content)

    # return list of scenes
    return content_json['data']
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    