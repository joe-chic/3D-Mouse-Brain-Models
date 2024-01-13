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
# - Validate that only certain carpet names are to be used, discard others.

# - Modify size of models, so that intersection is feasable.
# - For the oblique plane, maybe only rotating the final array will be necessary to render the plane images correctly. (???)

# - Oblicous images are gonna be like axial ones...

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

# In[5]:
# Esta bien que se pudiera tener dos opciones, una en la que se selecciona el path destino y una predeterminada.
path = 'C:/Users/J_Hum/OneDrive/Documents/RATONES/'
output_path = 'C:/Users/J_Hum/OneDrive/Documents/RATONES/MODELOS_3D/' 

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
                            viewer.camera.angles = (z_axis + ang_z, y_axis + ang_y + angle, x_axis + ang_x)
                            QApplication.processEvents() # This method is for lengthy operations while using a GUI application, it allows interaction during the processing of information.
                            # Toma 3 imagenes para cada posicionamiento del modelo, de tal forma que el video aparezca más ralentizado.
                            for take in range(3):
                                #What does this thing do?
                                screenshot = viewer.screenshot()
                                frames.append(screenshot)
                                
                                # What if angle images are already done.  ????? [REVIEW]

                                if take == 1 :
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

                    #images_angle = [f for f in os.listdir(os.path.join(output_path,image_directory)) if f.endswith('.png')]
                    #images_angle.sort()

                    #count = 0
                    #for check in images_angle:
                    #    if(check == f'Angle_{count}'):
                    #        count += 15
                    #    else:
                                
                    #        images_angle.append()
                    #        images_angle.sort()
            

                # MAKE IMAGES OF SLICES OF DIFFERENT PLANES

                # These plane videos will only be made if the model video hasn't been made. This could be improved (GUI AUTOMATION).

                if(exists):
                    image_files = [f for f in os.listdir(os.path.join(path,image_directory)) if f.endswith('.png')]
                    image_files.sort()
                    image_list = [imageio.imread(os.path.join(path,image_directory,img_file)) for img_file in image_files]
                    stack_array = np.stack(image_list, axis=0)

                factor = 4

                # FROM PLANE_VIDEOS module, make the videos of different planes.
                plane_videos(image_directory,output_path,stack_array,factor) 
            
            else:
                print(f'El nombre del archivo falta la mencion del tipo de plano. Revisar: {image_directory}')
                # FIX LATER DIRECTORIES.
        

    # What are UI updates?

# In[9]:


image_files = [f for f in os.listdir(image_directory) if f.endswith('.png')]
image_files.sort()
image_list = [imageio.v3.imread(os.path.join(image_directory, img_file)) for img_file in image_files]
stack_array = np.stack(image_list, axis=0)

frames = []
z_scaling = 5
viewer = None

with napari.gui_qt():
    viewer = napari.view_image(stack_array, scale=[z_scaling, 1, 1], ndisplay=3)
print(type(viewer))


# In[11]:


# Version antes de corroborar la existencia de videos

for image_directory in os.listdir(path):
    
        image_files = [f for f in os.listdir("".join([path,image_directory,'/'])) if f.endswith('.png')]
        image_files.sort()
        image_list = [imageio.imread(os.path.join("".join([path,image_directory,'/']), img_file)) for img_file in image_files]
        stack_array = np.stack(image_list, axis=0)

        frames = []
        z_scaling = 5
        viewer = None

        with napari.gui_qt():
            viewer = napari.view_image(stack_array, scale=[z_scaling, 1, 1], ndisplay=3)    
            viewer.camera.center = (0, 0, 0) 
            elev, azim, _ = viewer.camera.angles
            viewer.layers[0].rendering = 'average'
            viewer.layers[0].contrast_limits = (0, 20)
            viewer.layers[0].gamma = 0.7
            viewer.dims.order = [1, 2, 0]

            for angle in range(0, 360, 15):
                viewer.camera.angles = (elev + 180, azim + angle, 1)
                QApplication.processEvents()

                for _ in range(3):
                    screenshot = viewer.screenshot()
                    frames.append(screenshot)
                    time.sleep(0.5)

            # 
            
            imageio.mimwrite("".join([path,image_directory,'/',image_directory,'.mp4/']), frames, fps=30,quality=9)
            viewer.close()


# In[ ]:

# Debugging
for image_directory in os.listdir(path):
    
        image_files = [f for f in os.listdir(os.path.join(path,image_directory)) if f.endswith('.png')]
        image_files.sort()
        image_list = [imageio.v3.imread(os.path.join(path,image_directory,img_file)) for img_file in image_files]
        stack_array = np.stack(image_list, axis=0)

# %%
print(len(frames))
print(len(screenshot.shape))
print("Shape of first frame:", frames[0].shape)
print(screenshot)
# %%

# TESTING WHY ARE THERE SO MUCH IMAGES. BECAUSE OF WIDTH AND HEIGHT OF THE IMAGES.
# CHECK HOW TO SWAP INFORMATION BETWEEN DIMENSIONS. CHECK IF CONVERSION TO VIDEO IS FINE.
for image_directory in os.listdir(path):
    if(not(image_directory=='MODELOS_3D')):
        image_files = [f for f in os.listdir(os.path.join(path,image_directory)) if f.endswith('.png')]
        image_files.sort()
        image_list = [imageio.imread(os.path.join(path,image_directory,img_file)) for img_file in image_files]
        stack_array = np.stack(image_list, axis=0)
        print('Sagittal images are: ',range(stack_array.shape[2]))
        print('Coronal images are: ',range(stack_array.shape[0]))
        print('Axial images are: ',range(stack_array.shape[1]))
        print('\n')


# %%
# TESTING THE CONTENTS OF ARRAY
for image_directory in os.listdir(path):
    if(not(image_directory=='MODELOS_3D')):
        image_files = [f for f in os.listdir(os.path.join(path,image_directory)) if f.endswith('.png')]
        image_files.sort()
        image_list = [imageio.imread(os.path.join(path,image_directory,img_file)) for img_file in image_files]
        stack_array = np.stack(image_list, axis=0)
        print(stack_array.shape,'\n')
        print(stack_array[0,0,1],'\n')
        print(stack_array[:,:,stack_array.shape[2]-1]) # returns a 3d array
        print(stack_array.shape[2])
        print(np.zeros((2,3)))


# %%
print( os.listdir("".join([output_path,'Clean'])) )

# %%
# VALIDANDO EL PASO DE INFORMACION.

factor = 4

for image_directory in os.listdir(path):
    if(not(image_directory=='MODELOS_3D')):
        image_files = [f for f in os.listdir(os.path.join(path,image_directory)) if f.endswith('.png')]
        image_files.sort()
        image_list = [imageio.v2.imread(os.path.join(path,image_directory,img_file)) for img_file in image_files]
        stack_array = np.stack(image_list, axis=0)
       
        try:
            #Takes only the length pixels, giving axial plane.
            axial_slices = []
            axial_stack_array = np.zeros([(factor+1)*stack_array.shape[0]-factor,stack_array.shape[1],stack_array.shape[2]],dtype=np.uint8) # CHANGE THIS.
    
            for i in range(stack_array.shape[0]): 
                axial_stack_array[(factor+1)*i,:,:] = stack_array[i, :, :] # Like if black images were stacked in between the good ones.
            
            # is row by row, then the limit should be height, then .shape[2] (original stack.)
            # CLEAN: SECTIONAL CUT (190,2655) #THIS TELLS YOU NUMBER OF ELEMENTS, WIDTH (SECOND SHAPE, NUMBER OF COLUMNS) AND HEIGHT (FIRST SHAPE, NUMBER OF ROWS).
            # SCALED: SECTIOANL CUT (1140,2655)

            for i in range(stack_array.shape[1]): 
                slice_2d = axial_stack_array[:,i,:]
                axial_slices.append(slice_2d)
                    
            imageio.mimwrite("".join([output_path,image_directory,'/Axial_Slices.mp4']), axial_slices,fps=70,quality=9)
            break

        except Exception as f:
            print(f"Error al cargar las imagenes: {f}")



# %%
for image_directory in os.listdir(path):
    if(not(image_directory=='MODELOS_3D')):
        image_files = [f for f in os.listdir(os.path.join(path,image_directory)) if f.endswith('.png')]
        image_files.sort()
        image_list = [imageio.v3.imread(os.path.join(path,image_directory,img_file)) for img_file in image_files]
        stack_array = np.stack(image_list, axis=0)
        
        #Takes only the length pixels, giving axial plane.
        
        axial_slices = []
        axial_stack_array = np.zeros([(factor+1)*stack_array.shape[0]-factor,stack_array.shape[2]],dtype=np.uint8) # CHANGE THIS.
        
        b = np.zeros([(factor+1)*stack_array.shape[0]-factor,stack_array.shape[2]],dtype=np.int8)
        b.fill(3)

        print(axial_stack_array[0*(factor+1),:])
        axial_stack_array[0*(factor+1),:] = b[0*(factor+1),:] #it wasnt faulty.
        print(axial_stack_array[0*(factor+1),:])
        # TOO SLOW YET.         

    break

# %%
