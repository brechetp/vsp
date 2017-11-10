## A collection of utility functions

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

def is_image(array):
    """ Checks if the array can be an image """
    return array.__class__ is np.ndarray and ((array.ndim == 2) or (array.ndim == 3 and array.shape[2] == 3))
