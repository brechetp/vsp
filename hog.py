# implements a SIFT detector based on opencv
import matplotlib.pyplot as plt

from skimage.feature import hog
from skimage import io, color, exposure
import myio
import pdb

filename = myio.random_image("../data/muct-master/jpg/")
image = color.rgb2gray(io.imread(filename))

fd, hog_image = hog(image, orientations=8, pixels_per_cell=(32,32),
        cells_per_block=(1,1), visualise=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8,4), sharex=True, sharey=True)

ax1.axis('off')
ax1.imshow(image, cmap=plt.cm.gray)
ax1.set_title('Input image')
ax1.set_adjustable('box-forced')

# rescale gradients for better display
hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 0.02))

ax2.axis('off')
ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
ax2.set_title('Histogram of Oriented Gradients')

ax1.set_adjustable('box-forced')

plt.show()


