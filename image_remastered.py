import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import glob
import cv2
import sys
from PIL import Image

img=mpimg.imread(sys.argv[1])

a = 20
b = 20


#########################
# REDIMENSIONNEMENT IMG #
#########################

w = (img.shape[0] // a) * a
h = (img.shape[1] // b) * b
img = img[:w, :h]

###########################################
# ajout des blocs de pixels dans la liste #
###########################################

pixel_box = [] #liste

for i in range(img.shape[0]//a):
    for j in range(img.shape[1]//b):
        pixel_box.append(img[a*i:a*(i+1),b*j:b*(j+1)])

###########################
# moyenne images originel #
###########################

mean_rgb = np.mean(pixel_box, (1, 2))

image_list = []

for filename in glob.glob(sys.argv[2] + '/*.jpg'): 
    im=Image.open(filename)
    image_list.append(np.asarray(im))

# print(image_list[0].shape)

###########################
# moyenne images database #
###########################

mean_rgb_imgs = [np.mean(imgk, (0, 1)) for imgk in image_list]

selected_imgs = []

print('ok')

###############
# algorithmie #
###############

for box_id, box in enumerate(pixel_box):
    best_img = None
    best_dist = np.inf
    best_id = 0
    for img_id, imgimgs in enumerate(image_list):
        d = np.sqrt(((mean_rgb[box_id]-mean_rgb_imgs[img_id])**2).sum())
        if d < best_dist:
            best_dist = d
            best_img = imgimgs
            best_id = img_id
    
    selected_imgs.append(best_img)

print('ok')

l = 60 #1000
selected_imgs = [cv2.resize(imgs, (l, l)) for imgs in selected_imgs]

print('ok')

final_image = np.zeros((l*(img.shape[0]//a), l*(img.shape[1]//b), 3))

print('ok')

for i in range(img.shape[0]//a):
    for j in range(img.shape[1]//b):
        final_image[l*i:l*(i+1),l*j:l*(j+1)] = selected_imgs[i*(img.shape[1]//b)+j]

print('ok')

plt.imsave(sys.argv[3] ,final_image/255)
