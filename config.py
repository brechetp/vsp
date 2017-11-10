# HOG parameters
# the width and height are determined by the training instances
# we need to downsample the video image so that the dimensions are the same
class Config(object):
    """ A general class for configuration parameters """
    class HOG():
        """ HOG parameters """
        width=640
        height= 400
        orientations = 9
        cells_per_block= (3,3)
        pixels_per_cell= (8,8)
        block_norm= 'L2-Hys'

    HOG = HOG()

    class Resize():
        """ Resize parameters """
        width = 640
        height = 400
        mode = 'constant'
        anti_aliasing = True

    resize = Resize()


