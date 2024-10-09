

image_files = [f for f in os.listdir(image_directory) if f.endswith('.png')]
image_files.sort()
image_list = [imageio.v3.imread(os.path.join(image_directory, img_file)) for img_file in image_files]
stack_array = np.stack(image_list, axis=0)

frames = []
z_scaling = 2.5
viewer = None

with napari.gui_qt(force=True):
    viewer = napari.view_image(stack_array, scale=[z_scaling, 1, 1], ndisplay=3, channel_axis=-1, colormap=['gray', 'gray', 'blue'], name=['Axons','nt','Somata'])
    viewer.layers[0].rendering = 'average'
    viewer.layers[0].gamma = 0.9
    viewer.layers[0].contrast_limits = (0,40)

    viewer.layers[2].rendering = 'average'
    viewer.layers[2].gamma = 1.0
    viewer.layers[2].contrast_limits = (0,10)
    viewer.layers[2].colormap = 'gist_earth'
print(type(viewer))


# In[11]:


# Version antes de corroborar la existencia de videos
for image_directory in os.listdir(path):
    
        image_files = [f for f in os.listdir("".join([path,image_directory,'/'])) if f.endswith('.png')]
        image_files.sort()
        image_list = [imageio.imread(os.path.join("".join([path,image_directory,'/']), img_file)) for img_file in image_files]
        stack_array = np.stack(image_list, axis=0)

        frames = []
        z_scaling = 2.5
        viewer = None

        with napari.gui_qt(force=True):
            viewer = napari.view_image(stack_array, scale=[z_scaling, 1, 1], ndisplay=3, channel_axis=-1, colormap=['gray', 'gray', 'blue'], name=['Axons','nt','Somata'])    
            viewer.camera.center = (0, 0, 0) 
            #azimuth, elevation, and tilt
            elev, azim, _ = viewer.camera.angles
            viewer.layers[0].rendering = 'average'
            viewer.layers[0].gamma = 0.9
            viewer.layers[0].contrast_limits = (0,40)

            viewer.layers[2].rendering = 'average'
            viewer.layers[2].gamma = 1.0
            viewer.layers[2].contrast_limits = (0,10)
            viewer.layers[2].colormap = 'gist_earth'
            viewer.dims.order = [1, 2, 0]                                                     

            for angle in range(0, 360, 15):
                viewer.camera.angles = (elev + 180, azim + angle, 1)
                QApplication.processEvents()

                for _ in range(3):
                    screenshot = viewer.screenshot()
                    frames.append(screenshot)
                    time.sleep(0.5)

            # 
            #out = cv2.VideoWriter("".join([output_path,image_directory]),cv2.VideoWriter_fourcc('M','P','V','4'), 30, ((stack_array.shape[2],stack_array.shape[1])))
            #for frame in frames:
            #    out.write(frame)

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
            
            #out = cv2.VideoWriter("".join([output_path,image_directory]),cv2.VideoWriter_fourcc('M','P','V','4'), 30, (stack_array.shape[2],stack_array.shape[1]))
            #for frame in frames:
            #    out.write(frame)

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
        axial_stack_array[0*(factor+1),:] = b[0*(factor+1),:]
        print(axial_stack_array[0*(factor+1),:])
        # TOO SLOW YET.         

    break

# %%
