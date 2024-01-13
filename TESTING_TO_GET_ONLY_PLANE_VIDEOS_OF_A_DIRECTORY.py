from PLANE_VIDEOS import *
import os
import napari
import imageio.v3 as imageio
import imageio
import numpy as np
import cv2

path = 'C:/Users/J_Hum/OneDrive/Documents/RATONES/'

image_directory = 'P10HET Axial'
output_path = 'C:/Users/J_Hum/OneDrive/Documents/RATONES/MODELOS_3D/REPLACEMENT_P10/'

factor = 4

image_files = [f for f in os.listdir(os.path.join(path,image_directory)) if f.endswith('.png')]
image_files.sort()
image_list = [imageio.imread(os.path.join(path,image_directory,img_file)) for img_file in image_files]
stack_array = np.stack(image_list, axis=0)

plane_videos(image_directory,output_path,stack_array,factor)