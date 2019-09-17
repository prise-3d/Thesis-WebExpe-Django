# main imports 
import numpy as np
import os
import time
from datetime import datetime
import re

# image processing imports
from .processing import crop_images

# expe imports
from .quest_plus import QuestPlus

# load `config` variables
from .. import config as cfg

# PARAMETERS of the psychometric function
chance_level = 0 #e.g. chance_level should be 0.5 for 2AFC (Two-alternative forced choice) procedure
threshold_prob = 1.-(1.-chance_level)/2.0 #the probability level at the threshold

# quest_plus.py comes also with psychometric.py wich includes the definition of the weibull and weibull_db function
# here I define the logistic function using the same template that works with the quest_plus implementation
def logistic(x, params, corr_at_thresh=threshold_prob, chance_level=chance_level):
        # unpack params
        if len(params) == 3:
            THRESHOLD, SLOPE, lapse = params
        else:
            THRESHOLD, SLOPE = params
            lapse = 0.

        b = 4 * SLOPE
        a = -b * THRESHOLD

        return chance_level + (1 - lapse - chance_level) / (1 + np.exp(-(a + b*x)))
    

# that's a wrapper function to specify wich  psychometric function one we want to use for the QUEST procedure
def psychometric_fun( x , params ):
    return logistic(x , params ,  corr_at_thresh=threshold_prob, chance_level=chance_level)