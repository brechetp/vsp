# encapsulates the different features extraction
import matplotlib.pyplot as plt

from skimage.feature import hog as skimageHOG
from skimage.transform import resize
from skimage import io, color, exposure
import cv2
import numpy as np
import utils
import pdb
import utils # utilities functions
import config # config parameters



class MyFeat(object):
    """ A class to encapsulate the feature detection and computation"""

    def __init__(self, config):
        """ Init method
        Input:
            config: (Config) a configuration object
        """
        self._config = config # we keep the config object
        self._fd = None # the feature descriptor that will be computed
        self._visu = None # the visualization of the resultant feature

    @property
    def config(self):
        """The config object associated with the descriptor"""
        return self._config

    @property
    def fd(self):
        """The file descriptor"""
        return self._fd

    @fd.setter
    def fd(self, newFd):
        self._fd = newFd
        return

    @property
    def visu(self):
        return self._visu

    @visu.setter
    def visu(self, newVisu):
        self._visu = newVisu

    @utils.check_image_input
    def compute(self, image=None, **kwargs):
        """An abstract method that will be overwritten by specific feature implementation"""
        raise NotImplementedError('{} inside {}'.format(__name__, str(self.__class__)))
        pass

    # def resize(self, image):
        # """Resize the image according to resize parameters

        # :image: (numpy.ndarray) the image to be resized
        # :returns: (numpy.ndarary) the resized image

        # """
        # if (image.shape[0] != self.config.resize.height and image.shape[1] != self.config.resize.width): # if we need to scale the height and width
            # image = resize(image, (self.config.resize.height, self.config.resize.width), mode=self.config.resize.mode)
        # elif (image.shape[0] != self.config.resize.height): # only the height
            # image = resize(image, (self.config.resize.height, image.shape[1]), mode=self.config.resize.mode)
        # elif (image.shape[1] != self.config.resize.width): # only the width
            # image = resize(image, (image.shape[0], self.config.resize.width), mode=self.config.resize.mode)
        # return image

    def save_visu(self, filename):
        """Saves the visualisation to the file specified by its filename

        :filename: TODO
        :returns: TODO

        """

        if self.visu is not None:
            io.imsave(filename, self.visu)
        return


class MyHOG(MyFeat):

    """Customized implementation of the HOG feature computation"""

    def __init__(self, config):
        """Init of the HOG feature computation

        :config: (Config) The configuration object

        """
        MyFeat.__init__(self, config)

    @property # we limit the configuation to the HOG config
    def config(self):
        return self._config.HOG

    def compute(self, image):
        """ Computes the HOG from an image, rgb or gray, using the Scikit-image library
        We take care of having all images at the same resolution (given by the resolution of the training images)

        Input:
            image: (ndarray) an image in RGB or greyscale value (must be specified)
            visualise: (boolean) if we output the resultant visualisation image of the HOG
        Output:
            fd: the descriptor vector
            hog_image: (optional) the visualisation of the HOG
        """

        hog_visu = None
        assert image.ndim == 2 # we want a grayscale image
        # the actual computation of the HOG
        if self.config.visualise:
            fd, hog_visu = skimageHOG(image, orientations=self.config.orientations, pixels_per_cell=self.config.pixels_per_cell,
                    cells_per_block=self.config.cells_per_block, block_norm=self.config.block_norm, visualise=self.config.visualise) # we pass all arguments to the scikit function
            hog_visu = exposure.rescale_intensity(hog_visu, in_range=(hog_visu.min(), hog_visu.max()))
        else:
            fd = skimageHOG(image, orientations=self.config.orientations, pixels_per_cell=self.config.pixels_per_cell,
                    cells_per_block=self.config.cells_per_block, block_norm=self.config.block_norm, visualise=self.config.visualise) # we pass all arguments to the scikit function

        self.fd = fd # we save the feature descriptor inside the object
        self.visu =  hog_visu # and we save the (possibly None) visualisation inside the object as well
        return


class MySIFT(MyFeat):

    """SIFT implementation"""

    def __init__(self, config):
        """TODO: to be defined1. """
        MyFeat.__init__(self, config)
        self._sift = cv2.xfeatures2d.SIFT_create() # the sift object TODO parameters?
        return

    @property
    def sift(self):
        return self._sift

    @property
    def config(self):
        """The local config object"""
        return self._config.SIFT


    @utils.isuint8
    def compute(self, image):
        """Computes the SIFT features for the image

        :image: TODO
        :returns: TODO

        """
        assert (image.ndim == 2) # we need a grayscale image as input
        assert (image.dtype == np.uint8) # we need a int image
        kp = self.sift.detect(image) # the keypoints of the image
        _,self.fd = self.sift.compute(image, kp) # we compute the descriptor at the keypoint locations
        if self.config.visualise:
            self.visu = cv2.drawKeypoints(image,kp,self.visu)

        pass

class MyAAM(MyFeat):

    """AAM features implementation"""

    def __init__(self, config):
        """Initialization of the AAM feature descriptor object

        :config: (Config) configuration object

        """
        MyFeat.__init__(self, config)

        return


    def compute(self, image):
        """Computes the AAM features for the input image

        :image: (np.ndarray) the input image on which to compute the features

        """
        pass

class MyDCT(MyFeat):

    """DCT features for images"""

    def __init__(self, config):
        """Initialization of the DCT features descriptor

        :config: TODO

        """
        MyFeat.__init__(self, config)
        self._mask = utils.create_zz_mask((self._config.std_dim, self._config.std_dim), self.config.ncoeff) # the mask
        return

    @property
    def config(self):
        """The local config object"""
        return self._config.DCT

    def compute(self, image):
        """Computes the DCT features for the input image

        :image: TODO
        :returns: TODO

        """
        dct = cv2.dct(image)
        self.fd = np.extract(self._mask, dct).reshape(-1)


        return


if __name__ == "__main__": # if ran as a script

    config = config.Config()
    myHOG = MyHOG(config)
    for i in range(2):
        filename = utils.random_image("../data/muct-master/jpg/")
        image = color.rgb2gray(io.imread(filename))
        print("Size of the image number {}: {}x{}".format(i, image.shape[0], image.shape[1]))

        fd, hog_visu = myHOG.compute(image)
        
        print("Size of the descriptor {}: {}".format(i, fd.shape))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8,4), sharex=True, sharey=True)

        ax1.axis('off')
        ax1.imshow(image, cmap=plt.cm.gray)
        ax1.set_title('Input image')
        ax1.set_adjustable('box-forced')

# rescale gradients for better display
        hog_visu_rescaled = exposure.rescale_intensity(hog_visu, in_range=(0, 0.02))

        ax2.axis('off')
        ax2.imshow(hog_visu_rescaled, cmap=plt.cm.gray)
        ax2.set_title('Histogram of Oriented Gradients')

        ax1.set_adjustable('box-forced')

        plt.show()


