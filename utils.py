## A collection of utility functions
import pdb

import numpy as np
import os, random

def random_image(folder):
    """ Returns a random image from a folder
    Assumes all files in the foler are correct

    Input:
        folder: (string) the folder to pick the image from
    Output:
        image_path: the path oof the chosen image
    """
    if folder is None:
        folder='../data/muct-master/jpg/' # default folder

    name = random.choice(os.listdir(folder))
    return folder + name


def check_image_input(func):
    """ Decorator to check if the image given to func is indeed an image """
    def safe_func(*args, **kwargs): # we check if the input 
        if not is_image(args[0]) and not is_image(args[1]): # assumes 
            raise Exception("Wrong image type!")
        return func(*args, **kwargs)
    return safe_func

def isuint8(func):
    """Decorator to check if an image has integer values, convert it if not"""
    def safe_func(*args, **kwargs):
        if args[1].dtype == np.float: # if we have float values
            imuint8 = (255*args[1]).astype(np.uint8) # the correct image 
            return func(*((args[0],imuint8) + args[2:]), **kwargs)
        else:
            return func(*args, **kwargs)
    return safe_func

def is_image(array):
    """ Checks if the array can be an image """
    return array.__class__ is np.ndarray and ((array.ndim == 2) or (array.ndim == 3 and array.shape[2] == 3))


def create_zz_mask(size, n):
    """Creates a binary mask of size size[0] x size[1] with n first coefficients in zigzag selected"""
    (a, b) = size
    assert (n > 0)
    mask = np.zeros(size, dtype=np.int) # the mask, all zeros
    cnt = 0
    def idxlst(i, j, accu, cnt):
        """Returns the list of coordinates corresponding to the zigzag traversal

        :cnt: The remaining index to produce
        :accu: The parity of the current processed diagonal
        """
        if cnt == 0: # if we reached the end of the enumeration
            return []
        if accu % 2 == 0: # even, we increment the column
            if i == 0: # we need to increment the accu
                return [(i, j)] + idxlst(i, j+1, accu+1, cnt-1)
            else:
                return [(i, j)] + idxlst(i-1, j+1, accu, cnt-1)
        else:
            if j==0:
                return [(i, j)] + idxlst(i+1, j, accu+1, cnt-1)
            else:
                return [(i, j)] + idxlst(i+1, j-1, accu, cnt-1)
        return

    # indexing from a list of tuples https://stackoverflow.com/questions/42537956/slice-numpy-array-using-list-of-coordinates
    idx_tuple = idxlst(0, 0, 0, n) # the list of tuples to access
    idx_array = tuple(np.array(idx_tuple).T)
    mask[idx_array] = 1

    return mask

