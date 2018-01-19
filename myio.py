# script for image input / output

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

def write_list(lst, fname):
    '''Write a list to a file'''
    with open(fname, 'w') as _file:
        _file.writelines([item+'\n' for item in lst])
    return


if __name__ == "__main__":
    write_list(['a', 'a g w', '.', '', 'w'], 'save.txt')
