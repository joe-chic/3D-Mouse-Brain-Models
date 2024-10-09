# This used the napari version 0.4.18, now being upgraded to 0.5.3
# pydantic remains as 2.7.4
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
output_path = 'C:/Users/J_Hum//Documents/RATONES/TESTING_ZONE/'

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
        if(not(image_directory==head) and image_directory == 'P10HET Axial'):
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

                        if(('Coronal' or 'Sagital') in image_directory): 
                            ang_z = 0
                            ang_y = 0
                            ang_x = 0
                        elif('Axial' in image_directory):
                            ang_z = 0
                            ang_y = 0
                            ang_x = 90
                        
                        # Se hace un for loop que tome una captura del modelo cada 15 grados.
                        for angle in range(0, 360, 15):                  
                            viewer.camera.angles = (z_axis + ang_z + angle, y_axis + ang_y + 90, x_axis + ang_x + angle) # IT IS MODEL DEPENDENT !!!  ??? .
                            QApplication.processEvents() # This method is for lengthy operations while using a GUI application, it allows interaction during the processing of information.
                            # Toma 3 imagenes para cada posicionamiento del modelo, de tal forma que el video aparezca más ralentizado.
                            for take in range(3):
                                #What does this thing do?
                                screenshot = viewer.screenshot()
                                frames.append(screenshot)
                        
                        try:
                            imageio.mimwrite("".join([output_path,image_directory,'/',image_directory,'.mp4']), frames, fps=30,quality=9)
                            print("Video ha sido guardado exitosamente.")
                        except Exception as e:
                            print(f"Error al guardar el video: {e}")

                        viewer.close() 
                else:
                    # YA HAY UN VIDEO HECHO, LUEGO SE CORROBORA QUE LAS IMAGENES HAYAN SIDO HECHAS O NO.
                    # What if there is a video but there are no images done yet... review. You have to validate that there are no images.
                    # If i can avoid opening the GUI everytime, then I can defintely automatize this. As for now, the only proper way to 
                    # make the angle images, is by first intiating the creation of the model video.

                    print(f'Ya hay video en el directorio {image_directory}.') 
