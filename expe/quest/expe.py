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
    return logistic(x , params ,  corr_at_thresh=threshold_prob, chance_level=chance_level )



#create results directory if not exist
if not os.path.exists(cfg.output_expe_folder):
    os.makedirs(cfg.output_expe_folder)
  
timestamp = datetime.strftime(datetime.utcnow(), "%Y-%m-%d_%Hh%Mm%Ss")
filename += "online_ans" + timestamp +".csv"
f = open(filename,"w")

#orientation : 0 = vertical, 1 = horizontal
#image_ref_position : 0 = right/bottom, 1 = left/up
#answer : left = 1, right = 0
f.write('stimulus' + ";" + "name_stimulus" + ";" + 'cropping_percentage' + ";" + 'orientation' + ';' 
         + 'image_ref_position' + ';' + 'answer' + ';' + 'time_reaction' + ';' + 'entropy' + '\n')
#k=np.linspace(50,20000,50)
#k=k.astype(int)
dd_sam=[]

for i in range(len(files)):
    ff = [int(s) for s in re.findall(r'\d+', files[i])]
    dd_sam.append(ff[0])


dd_sam=np.array(dd_sam)
    
    
thresholds = np.arange(50, 10000, 50)
stim_space=np.asarray(dd_sam)
slopes = np.arange(0.0001, 0.001, 0.00003)

#mywin = visual.Window([800,600], monitor="testMonitor", screen = 1, units="deg",fullscr=True)
qp = QuestPlus(stim_space, [thresholds, slopes], function=psychometric_fun)
answerTime=[]
r=[]

dataset = "contemporary"

#image_ref = Image.open(data_folder + files[-1])
image_ref = get_image(diran_domain_name, dataset, 10000)
for i in range(5):
    next_stim = qp.next_contrast()
    print(next_stim)
    #next_idx = np.where(dd_sam==next_stim)
    #print(files[next_idx[0][0]])
    #image_path = data_folder + files[next_idx[0][0]]
    #current_image = Image.open(image_path)
    current_image= get_image(diran_domain_name, dataset, next_stim)
    crop_image, percentage, orientation, position = crop_images(image_ref, current_image)

    answerTime.append(end-start)
    if key_answer == ['left']:
        answer = 1 #one image
    else: 
        answer = 0  #two images
    r.append(answer)
    qp.update(dd_sam[i], answer) 
    
    entropy = qp.get_entropy()

    print(entropy)
    
    f.write(str(next_stim) + ";" + dataset + ";" + str(percentage) + ";" + str(orientation) + ";" 
            + str(position) + ";" + str(answer) + ";" + str(answerTime[-1]) + ";" + str(entropy) +'\n')
    f.flush()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    