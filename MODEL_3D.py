from PLANE_VIDEOS import *
import os
import napari
import imageio.v3 as imageio
import imageio
import numpy as np
import time
from PyQt5.QtWidgets import QApplication
import cv2

path = 'C:/Users/J_Hum/Documents/RATONES'
output_path = 'C:/Users/J_Hum/Documents/RATONES/TESTING_ZONE'

Ry = [[]]

if(path == output_path):
    print("El directorio para almacenar los documentos no puede estar ubicado en el mismo en donde se extraen las imagenes.")
else:
    # Para evitar que se considere el directorio con las modelos si se encuentra dentro del mismo folder con las imagenes.
    head = ''
    if(path in output_path):
        path_diff = output_path.replace(path,'')
        head, __, __ = path_diff.partition('/')

    for image_directory in os.listdir(path):
        if(('Coronal' in image_directory) or ('Sagital' in image_directory) or ('Axial' in image_directory)):
        #Change order with the above if else.
            
            # Crea un archivo destino para cada archivo con un stack de imagenes
            try:
                os.mkdir("".join([output_path,image_directory]))
            except:
                print(f"El directorio {image_directory} no fue hecho.")
            
            # Se corrobora que no exista el video, para no tener que repetir el proceso nuevamente para los stacks de imagenes ya procesados.
            exists = False
            
            for i in os.listdir("".join([output_path,image_directory])):
                if i.endswith("".join([image_directory,'.mp4'])):
                    exists = True
                    break
            
            if(not(exists)):
                image_files = [f for f in os.listdir(os.path.join(path,image_directory)) if f.endswith('.png')]
                image_files.sort()
                image_list = [imageio.imread(os.path.join(path,image_directory,img_file)) for img_file in image_files]
                stack_array = np.stack(image_list, axis=0)
                
                frames = []
                z_scaling = 5
                viewer = None
            
                # Se abre la aplicación GUI para visualizar el modelo 3D.
                with napari.gui_qt():
                    # Se configura el modelo 3D para un mejor visualizado.
                    viewer = napari.view_image(stack_array, scale=[z_scaling, 1, 1], ndisplay=3)    
                    z_axis, y_axis, x_axis = viewer.camera.angles
                    viewer.layers[0].rendering = 'average'
                    viewer.layers[0].contrast_limits = (0, 20)
                    viewer.layers[0].gamma = 0.7