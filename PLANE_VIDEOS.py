import os
import imageio.v3 as imageio
import imageio
import numpy as np
import cv2

# Direction plane images:
# AXIAL PLANE:
#   Coronary: From the front to the back
#   Sagital: Head pointing right, doubt that direction of video progression matters now.
#   Axial: From bottom to top

def plane_videos_gray(image_directory,output_path,stack_array,factor):
    if('Coronal' in image_directory): 
        A_save = 'Axial_Slices.mp4'
        B_save = 'Coronal_Slices.mp4' # main
        C_save = 'Sagittal_Slices.mp4'
    elif('Sagital' in image_directory):
        A_save = 'Axial_Slices.mp4'
        B_save = 'Sagittal_Slices.mp4' # main
        C_save = 'Coronal_Slices.mp4'
    elif('Axial' in image_directory):
        A_save = 'Coronal_Slices.mp4'
        B_save = 'Axial_Slices.mp4' # main
        C_save = 'Sagittal_Slices.mp4'

    make = True
    for validate in os.listdir("".join([output_path,image_directory])):
        if(validate == A_save):
            make = False
            break

    if(make):
        try:
            #Takes only the width pixels, giving axial plane.
            axial_slices = []
            axial_stack_array = np.zeros([(factor+1)*stack_array.shape[0]-factor,stack_array.shape[1],stack_array.shape[2]],dtype=np.uint8) # CHANGE THIS.

            for i in range(stack_array.shape[0]): 
                axial_stack_array[(factor+1)*i,:,:] = stack_array[i, :, :] # Like if black images were stacked in between the good ones.
            
            axial_slices = [axial_stack_array[:,i,:] for i in range(stack_array.shape[1])]
                
            imageio.mimwrite("".join([output_path,image_directory,f'/{A_save}']), axial_slices,fps=80,quality=9)
        
        except Exception as f:
            print(f"Error al cargar las imagenes: {f}")


    make = True
    for validate in os.listdir("".join([output_path,image_directory])):
        if(validate == B_save):
            make = False
            break

    if(make):
        try:
            coronal_slices = [stack_array[slices,:,:] for slices in range(stack_array.shape[0])] 
            imageio.mimwrite("".join([output_path,image_directory,f'/{B_save}']), coronal_slices,fps=20,quality=9)
        except Exception as f:
            print(f"Error al cargar las imagenes: {f}")
    
    make = True
    for validate in os.listdir("".join([output_path,image_directory])):
        if(validate == C_save):
            make = False
            break
    
    if(make):
        try:
            # RESIZE ARRAY, ADD BLACK PIXELS N NUMBER OF TIMES AND COPY INFORMATION.
            sagittal_stack_array = np.zeros(((factor+1)*stack_array.shape[0]-factor,stack_array.shape[1],stack_array.shape[2]),dtype=np.uint8)
            
            for i in range(stack_array.shape[0]): 
                sagittal_stack_array[(factor+1)*i,:,:] = stack_array[i, :, :]
            
            if('Axial' in image_directory):
                sagittal_slices = [np.fliplr(sagittal_stack_array[:,:,i]) for i in range(stack_array.shape[2])] # Head always points to left.
            elif('Coronal' in image_directory or 'Sagital' in image_directory):
                sagittal_slices = [np.rot90(sagittal_stack_array[:,:,i],k=-1) for i in range(stack_array.shape[2])]
            
            imageio.mimwrite("".join([output_path,image_directory,f'/{C_save}']), sagittal_slices,fps=80,quality=9)                   
        except Exception as f:
            print(f"Error al cargar las imagenes: {f}")

def plane_videos_BGR(image_directory,output_path,stack_array,factor):
    if 'Coronal' in image_directory: 
        A_save = 'Axial_Slices.mp4'
        B_save = 'Coronal_Slices.mp4'  # main
        C_save = 'Sagittal_Slices.mp4'
    elif 'Sagital' in image_directory:
        A_save = 'Axial_Slices.mp4'
        B_save = 'Sagittal_Slices.mp4'  # main
        C_save = 'Coronal_Slices.mp4'
    elif 'Axial' in image_directory:
        A_save = 'Coronal_Slices.mp4'
        B_save = 'Axial_Slices.mp4'  # main
        C_save = 'Sagittal_Slices.mp4'

    # Axial Slices
    make = True
    for validate in os.listdir("".join([output_path, image_directory])):
        if validate == A_save:
            make = False
            break

    if make:
        try:
            # Axial slices: take only width pixels and handle the 3-channel BGR
            axial_stack_array = np.zeros([(factor + 1) * stack_array.shape[0] - factor, stack_array.shape[1], stack_array.shape[2], 3], dtype=np.uint8)  # Add channel dimension

            for i in range(stack_array.shape[0]): 
                axial_stack_array[(factor + 1) * i, :, :, :] = stack_array[i, :, :, :]  # Include the BGR channels

            axial_slices = [axial_stack_array[:, i, :, :] for i in range(stack_array.shape[1])]  # Slice along the height axis

            imageio.mimwrite("".join([output_path, image_directory, f'/{A_save}']), axial_slices, fps=80, quality=9)

        except Exception as f:
            print(f"Error al cargar las imagenes: {f}")

    # Coronal Slices
    make = True
    for validate in os.listdir("".join([output_path, image_directory])):
        if validate == B_save:
            make = False
            break

    if make:
        try:
            # Coronal slices: take slices along the depth axis
            coronal_slices = [stack_array[slices, :, :, :] for slices in range(stack_array.shape[0])]  # Slice along depth with BGR
            imageio.mimwrite("".join([output_path, image_directory, f'/{B_save}']), coronal_slices, fps=20, quality=9)
        except Exception as f:
            print(f"Error al cargar las imagenes: {f}")

    # Sagittal Slices
    make = True
    for validate in os.listdir("".join([output_path, image_directory])):
        if validate == C_save:
            make = False
            break

    if make:
        try:
            sagittal_stack_array = np.zeros(((factor + 1) * stack_array.shape[0] - factor, stack_array.shape[1], stack_array.shape[2], 3), dtype=np.uint8)  # Handle BGR

            for i in range(stack_array.shape[0]): 
                sagittal_stack_array[(factor + 1) * i, :, :, :] = stack_array[i, :, :, :]  # Include BGR

            if 'Axial' in image_directory:
                sagittal_slices = [np.fliplr(sagittal_stack_array[:, :, i, :]) for i in range(stack_array.shape[2])]  # Head points left
            elif 'Coronal' in image_directory or 'Sagital' in image_directory:
                sagittal_slices = [np.rot90(sagittal_stack_array[:, :, i, :], k=-1) for i in range(stack_array.shape[2])]  # Adjust rotation for different planes

            imageio.mimwrite("".join([output_path, image_directory, f'/{C_save}']), sagittal_slices, fps=80, quality=9)
        except Exception as f:
            print(f"Error al cargar las imagenes: {f}")