import napari
import imageio.v3 as imageio
import imageio
from skimage.data import cells3d

viewer, image_layer = napari.imshow(cells3d())

# print shape of image datas
print(image_layer.data.shape)

# start the event loop and show the viewer
napari.run()