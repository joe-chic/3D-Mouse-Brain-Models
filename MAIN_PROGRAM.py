# The dimensions for Clean image are: 2655 x 2494 
# The dimensiones for Resize image are: 2655 x 2668

# The number of Clean images is: 190
# The number of Resized images is: 384

# Pendant modifications:
# - Hybrid application where core code is written in c++ and other tools with python.
# - Change a few things for optimization.
# - What if angle images are already done. [REVIEW] (HOW TO DO THAT EVALUATION IN THE MOST OPTIMAL WAY?)
# - How does QtApplications work?
# - Adjust parameters for models.
# - What if there is a video but there are no images done yet... review. You have to validate that there are no images.
# - Change os for pathlib. #ONLY IF IOS OR UBUNTU ARE GOING TO BE USED I THINK.
# - Github
# - Validate that only certain carpet names will be used, discard others.
# - Detection of a grayscale or color images.
# - Increase contrast in plane images.
# - Do a functional architecture.
# - Direct use of VisPy instead of napari.
# - Check how to avoid having problems with library dependencies.

# - Modify size of models, so that intersection is feasable.
# - For the oblique plane, maybe only rotating the final array will be necessary to render the plane images correctly. (???)

# - Oblicous images are gonna be like axial ones...

# - Napari is built on top of Qt (for the GUI), vispy (for performant GPU-based rendering), and the scientific Python stack (numpy, scipy).
# - For dominating VisPy, one needs to use OpenGL. 

# In[4]:

from PLANE_VIDEOS import *
import os
import napari
import imageio.v3 as imageio
import imageio
import numpy as np
import time
from PyQt5.QtWidgets import QApplication
import cv2
from PIL import Image

Image.MAX_IMAGE_PIXELS = 1000000000

# In[5]:
# Esta bien que se pudiera tener dos opciones, una en la que se selecciona el path destino y una predeterminada.
path = 'C:/Users/J_Hum/Downloads/New_Data/'
output_path = 'C:/Users/J_Hum/Downloads/New_Data/MODELOS_3D/' 

# GENERALIZE MAKING AN EXCEPTION FOR AN INSIDE FOLDER.
# WHAT IF THE OUTPUT FILE IS INSIDE OF MULTIPLE FOLDERS...

# In[10]:

# Save images and video in the same directory 
# What is the difference between makedirs and mkdir()?

if(path == output_path):
    print("El directorio para almacenar los documentos no puede estar ubicado en el mismo en donde se extraen las imagenes.")
else:
    # Para evitar que se considere el directorio con las modelos si se encuentra dentro del mismo folder con las imagenes.
    head = ''
    if(path in output_path):
        path_diff = output_path.replace(path,'')
        head, __, __ = path_diff.partition('/')

    for image_directory in os.listdir(path):
        if(not(image_directory==head)):
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
                    z_scaling = 2.5
                    viewer = None
                
                    # Se abre la aplicación GUI para visualizar el modelo 3D.
                    with napari.gui_qt():
                        # Se configura el modelo 3D para un mejor visualizado.  
                        viewer = napari.view_image(stack_array, scale=[z_scaling, 1, 1], ndisplay=3, channel_axis=-1, colormap=['gray', 'gray', 'blue'], name=['Axons','nt','Somata'])
                        z_axis, y_axis, x_axis = viewer.camera.angles
                        viewer.layers['Somata'].colormap = 'blue'

                        viewer.layers[0].rendering = 'average'
                        viewer.layers[0].gamma = 0.9
                        viewer.layers[0].contrast_limits = (0,40)

                        viewer.layers[2].rendering = 'average'
                        viewer.layers[2].gamma = 1.0
                        viewer.layers[2].contrast_limits = (0,10)
                        viewer.layers[0].contrast_limits = (0,40)
                        viewer.layers[2].colormap = 'gist_earth'

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
                            viewer.camera.angles = (z_axis + ang_z, y_axis + ang_y + angle, x_axis + ang_x)
                            QApplication.processEvents() # This method is for lengthy operations while using a GUI application, it allows interaction during the processing of information.
                            # Toma 3 imagenes para cada posicionamiento del modelo, de tal forma que el video aparezca más ralentizado.
                            for take in range(3):
                                #What does this thing do?
                                screenshot = viewer.screenshot()
                                frames.append(screenshot)
                                
                                # What if angle images are already done.  ????? [REVIEW]

                                if take == 1 :
                                    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                                    cv2.imwrite("".join([output_path,image_directory,'/Angle_',str(angle),'.png']),screenshot)

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

                # MAKE IMAGES OF SLICES OF DIFFERENT PLANES

                # These plane videos will only be made if the model video hasn't been made. This could be improved (GUI AUTOMATION).
                
                if(exists):
                    image_files = [f for f in os.listdir(os.path.join(path,image_directory)) if f.endswith('.png')]
                    image_files.sort()
                    image_list = [imageio.imread(os.path.join(path,image_directory,img_file)) for img_file in image_files]
                    stack_array = np.stack(image_list, axis=0)

                factor = 4

                # FROM PLANE_VIDEOS module, make the videos of different planes.
                plane_videos_BGR(image_directory,output_path,stack_array,factor) 

            else:
                print(f'El nombre del archivo falta la mencion del tipo de plano. Revisar: {image_directory}')
                # FIX LATER DIRECTORIES.
        
    # What are UI updates?