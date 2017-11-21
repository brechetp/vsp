# HOG parameters
# the width and height are determined by the training instances
# we need to downsample the video image so that the dimensions are the same
class Config(object):
    """ A general class for configuration parameters """
    compute = ['SIFT', 'DCT']#, 'AAM', 'DCT']
    # compute = ['HOG']
    std_dim = 48 # the resize
    debug = False
    resize = True
    verbose = False

    class HOG():
        """ HOG parameters """
        width=640
        height= 400
        visualise = False
        orientations = 9
        cells_per_block= (1,1)
        pixels_per_cell= (8,8)
        block_norm= 'L2-Hys'

    HOG = HOG()

    class SIFT():
        visualise = True

    SIFT = SIFT()

    class AAM():
        visualise = True

    AAM = AAM()

    class DCT():
        visualise = True
        ncoeff = 10 # the number of coefficients to keep

    DCT = DCT()

    class Resize():
        """ Resize parameters """
        width = 640
        height = 400
        mode = 'constant'
        anti_aliasing = True
        do = False

    HOG.resize = Resize()
    # HOG.resize.do = False

