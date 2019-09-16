
from PIL import Image
import os
import numpy as np
import random

def crop_images(img1, img2, per=None, orien=None, swap_img=None):
    '''
    crop and gather reference image and a noisy one randomly
    '''
    if per is None:
        per = random.choice([0.25, 0.5, 0.75])
    if orien is None:
        orien = random.choice([0, 1])
    if swap_img is None:
        swap_img = random.choice([0, 1])
    
    if swap_img:
        tmp_img = img1
        img1 = img2
        img2 = tmp_img
        
    img_merge = None

    #vertical
    if orien==0:
        width, height = img1.size
        left, top, right, bottom = 0, 0, per*width, height
        cropped1 = img1.crop( ( left, top, right, bottom ) )  
        
        left, top, right, bottom = per*width, 0, width, height
        cropped2 = img2.crop( ( left, top, right, bottom ) ) 

        crop1 =np.asarray(cropped1)
        crop2 = np.asarray(cropped2)
        img_merge = np.hstack((crop1,crop2))
        img_merge = Image.fromarray( img_merge)
    else:
        #horizontal
        width, height = img1.size
        left, top, right, bottom = 0, 0, width, per*height
        cropped1 = img1.crop( ( left, top, right, bottom ) )  
        left, top, right, bottom = 0, per*height, width, height
        cropped2 = img2.crop( ( left, top, right, bottom ) ) 
        crop1 =np.asarray(cropped1)
        crop2 = np.asarray(cropped2)
        img_merge = np.vstack((crop1,crop2))
        img_merge = Image.fromarray( img_merge)
    
    return img_merge, per, orien, swap_img