# implements a SIFT detector based on opencv
import matplotlib.pyplot as plt

from skimage.feature import hog as skimageHOG
from skimage.transform import resize
from skimage import io, color, exposure
import numpy as np
import utils
import pdb
import utils # utilities functions
import config # config parameters



class HOG(object):
    """ A class for the Histrogram of Gradients feature descriptor implementation """

    def __init__(self, config):
        """ Init method
        Input:
            config: (Config) a configuration object
        """
        self.config = config # we keep the config object

    @utils.check_image_input
    def compute(self, image=None, visualise=False):
        """ Computes the HOG from an image, rgb or gray, using the Scikit-image library
        We take care of having all images at the same resolution (given by the resolution of the training images)

        Input:
            image: (ndarray) an image in RGB or greyscale value (must be specified)
            visualise: (boolean) if we output the resultant visualisation image of the HOG
        Output:
            fd: the descriptor vector
            hog_image: (optional) the visualisation of the HOG
        """

        hog_image = None
        if (image.ndim == 3): # if we need to convert the input in gray scale
            image = color.rgb2gray(image)
        # we then resize the input image if necessary
        if (image.shape[0] != self.config.resize.height and image.shape[1] != self.config.resize.width): # if we need to scale the height and width
            image = resize(image, (self.config.resize.height, self.config.resize.width), mode=self.config.resize.mode)
        elif (image.shape[0] != self.config.resize.height): # only the height
            image = resize(image, (self.config.resize.height, image.shape[1]), mode=self.config.resize.mode)
        elif (image.shape[1] != self.config.resize.width): # only the width
            image = resize(image, (image.shape[0], self.config.resize.width), mode=self.config.resize.mode)
        # the actual computation of the HOG
        fd, hog_image = skimageHOG(image, orientations=self.config.HOG.orientations, pixels_per_cell=self.config.HOG.pixels_per_cell,
                    cells_per_block=self.config.HOG.cells_per_block, block_norm=self.config.HOG.block_norm, visualise=visualise) # we pass all arguments to the scikit function
        if hog_image is not None:
            hog_image = exposure.rescale_intensity(hog_image, in_range=(hog_image.min(), hog_image.max()))

        return fd, hog_image # war

@utils.check_image_input
def mySIFT(image):
    """ Computes the SIFT features inside the image
    Input:
        image: (ndarray) the input image
    Output:
        fd: the feature descriptors for the image
    """
    pass


if __name__ == "__main__": # if ran as a script

    for i in range(2):
        filename = utils.random_image("../data/muct-master/jpg/")
        image = color.rgb2gray(io.imread(filename))
        print("Size of the image number {}: {}x{}".format(i, image.shape[0], image.shape[1]))

        config = config.Config()
        myHOG = HOG(config)
        fd, hog_image = myHOG.compute(image, visualise=True)
        print("Size of the descriptor {}: {}".format(i, fd.shape))

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


